-- SICP: Procedural Abstraction. 
-- This function encapsulates the complex logic of the "Indiana Jones" vulnerability check.

CREATE OR REPLACE FUNCTION process_vault_transaction()
RETURNS TRIGGER AS $$
DECLARE
    matched_user users%ROWTYPE;
    matched_asset assets%ROWTYPE;
    abs_delta NUMERIC;
BEGIN
    -- 1. Identify User (O(log N) lookup)
    SELECT * INTO matched_user FROM users WHERE rfid_uid = NEW.rfid_uid;
    
    IF NOT FOUND THEN
        -- Anomaly Tap: Biarkan masuk ke transactions_log untuk audit, tapi jangan proses aset.
        RETURN NEW;
    END IF;

    abs_delta := ABS(NEW.weight_delta);

    -- 2. Filter noise (DOET: Ignorable variations)
    IF abs_delta < 15 THEN
        RETURN NEW; -- Pintu dibuka-tutup tapi tidak ada barang yang diambil.
    END IF;

    -- 3. Pencocokan Aset Berdasarkan Berat (O(log N) scan)
    SELECT * INTO matched_asset 
    FROM assets 
    WHERE baseline_weight_g >= (abs_delta - tolerance_g) 
      AND baseline_weight_g <= (abs_delta + tolerance_g)
    LIMIT 1;

    IF NOT FOUND THEN
        -- Indiana Jones Vulnerability Check: Berat tidak cocok dengan aset manapun.
        RETURN NEW;
    END IF;

    -- 4. State Machine Mutator
    IF NEW.weight_delta < -15 THEN
        -- Aset Diambil
        INSERT INTO active_loans (rfid_uid, asset_id) 
        VALUES (matched_user.rfid_uid, matched_asset.id)
        ON CONFLICT (asset_id) DO UPDATE SET rfid_uid = EXCLUDED.rfid_uid, borrowed_at = NOW();

    ELSIF NEW.weight_delta > 15 THEN
        -- Aset Dikembalikan
        DELETE FROM active_loans 
        WHERE asset_id = matched_asset.id 
          AND rfid_uid = matched_user.rfid_uid;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_process_vault_transaction
AFTER INSERT ON transactions_log
FOR EACH ROW
EXECUTE FUNCTION process_vault_transaction();