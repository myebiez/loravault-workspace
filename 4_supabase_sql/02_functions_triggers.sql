-- SICP: Procedural Abstraction. 
-- This function encapsulates the complex logic of the "Indiana Jones" vulnerability check.
-- It automatically translates a raw weight delta into a physical borrow or return event.

CREATE OR REPLACE FUNCTION process_vault_transaction()
RETURNS TRIGGER AS $$
DECLARE
    matched_user users%ROWTYPE;
    matched_asset assets%ROWTYPE;
    abs_delta NUMERIC;
BEGIN
    -- 1. Identify User (\mathcal{O}(\log N) lookup) menggunakan rfid_uid
    SELECT * INTO matched_user FROM users WHERE rfid_uid = NEW.rfid_uid;
    
    IF NOT FOUND THEN
        -- Pragmatic: Silent failure is unacceptable. We let the transaction log, 
        -- but we do not process loans for unknown RFIDs. The Pi 3 GUI will flag this.
        RETURN NEW;
    END IF;

    abs_delta := ABS(NEW.weight_delta);

    -- 2. Filter noise (DOET: Ignorable variations)
    IF abs_delta < 15 THEN
        RETURN NEW; -- Door was opened and closed, but nothing was taken.
    END IF;

    -- 3. Find the matching asset by weight (\mathcal{O}(\log N) via index scan)
    -- We look for an asset whose baseline weight matches the delta within its specific tolerance.
    SELECT * INTO matched_asset 
    FROM assets 
    WHERE baseline_weight_g >= (abs_delta - tolerance_g) 
      AND baseline_weight_g <= (abs_delta + tolerance_g)
    LIMIT 1;

    IF NOT FOUND THEN
        -- Anomaly: Weight change doesn't match any known asset.
        -- (e.g., The Indiana Jones rock-swap trick failed).
        RETURN NEW;
    END IF;

    -- 4. State Machine: Borrow vs. Return (DIPERBARUI MENGGUNAKAN rfid_uid)
    IF NEW.weight_delta < -15 THEN
        -- Weight decreased -> Asset Taken
        -- Upsert into active loans to prevent duplicates if system desyncs
        INSERT INTO active_loans (rfid_uid, asset_id) 
        VALUES (matched_user.rfid_uid, matched_asset.id)
        ON CONFLICT (asset_id) DO UPDATE SET rfid_uid = EXCLUDED.rfid_uid, borrowed_at = NOW();

    ELSIF NEW.weight_delta > 15 THEN
        -- Weight increased -> Asset Returned
        DELETE FROM active_loans 
        WHERE asset_id = matched_asset.id 
          AND rfid_uid = matched_user.rfid_uid;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Bind the procedural abstraction to the data layer
CREATE TRIGGER trigger_process_vault_transaction
AFTER INSERT ON transactions_log
FOR EACH ROW
EXECUTE FUNCTION process_vault_transaction();