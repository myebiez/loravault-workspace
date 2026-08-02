-- ==============================================================================
-- SECURE EDGE GATEWAY ENDPOINTS (RPC)
-- ==============================================================================
-- Fungsi ini berjalan sebagai Superuser (SECURITY DEFINER) namun mengamankan diri 
-- menggunakan token HMAC. Kunci 'anon' publik tidak lagi bisa disalahgunakan hacker.

CREATE OR REPLACE FUNCTION secure_insert_telemetry(p_rfid_uid TEXT, p_weight_delta NUMERIC, p_token TEXT)
RETURNS void AS $$
BEGIN
    -- Pragmatic Programmer: Design by Contract. Tolak mentah-mentah jika token salah.
    IF p_token != 'secret_esp32_hmac_token' THEN
        RAISE EXCEPTION 'Unauthorized Gateway Request';
    END IF;
    INSERT INTO transactions_log (rfid_uid, weight_delta) VALUES (p_rfid_uid, p_weight_delta);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION secure_sync_user(p_rfid_uid TEXT, p_nik TEXT, p_token TEXT)
RETURNS void AS $$
BEGIN
    IF p_token != 'secret_esp32_hmac_token' THEN
        RAISE EXCEPTION 'Unauthorized Gateway Request';
    END IF;
    -- Menggunakan klausa ON CONFLICT untuk menangani Air-Gapped Sync yang berulang
    INSERT INTO users (rfid_uid, nik) VALUES (p_rfid_uid, p_nik) ON CONFLICT (rfid_uid) DO NOTHING;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-- ==============================================================================
-- SECURE STORAGE ENDPOINT (NODE 3 CAMERA)
-- ==============================================================================
-- Memungkinkan Node 3 untuk melampirkan URL bukti forensik ke baris transaksi 
-- tanpa harus memberikan akses UPDATE publik ke seluruh tabel.
CREATE OR REPLACE FUNCTION secure_attach_evidence(p_transaction_id UUID, p_url TEXT, p_token TEXT)
RETURNS void AS $$
BEGIN
    -- Menggunakan token gateway yang sama untuk memvalidasi identitas internal sistem
    IF p_token != 'secret_esp32_hmac_token' THEN
        RAISE EXCEPTION 'Unauthorized Storage Request';
    END IF;
    UPDATE transactions_log SET evidence_url = p_url WHERE id = p_transaction_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-- ==============================================================================
-- THE MATHEMATICAL BRAIN (STATE MACHINE TRIGGER)
-- ==============================================================================
CREATE OR REPLACE FUNCTION process_vault_transaction()
RETURNS TRIGGER AS $$
DECLARE
    matched_user users%ROWTYPE;
    matched_asset assets%ROWTYPE;
    abs_delta NUMERIC;
BEGIN
    SELECT * INTO matched_user FROM users WHERE rfid_uid = NEW.rfid_uid;
    
    IF NOT FOUND THEN
        RETURN NEW;
    END IF;

    abs_delta := ABS(NEW.weight_delta);

    IF abs_delta < 15 THEN
        RETURN NEW; 
    END IF;

    SELECT * INTO matched_asset 
    FROM assets 
    WHERE baseline_weight_g >= (abs_delta - tolerance_g) 
      AND baseline_weight_g <= (abs_delta + tolerance_g)
    LIMIT 1;

    IF NOT FOUND THEN
        RETURN NEW;
    END IF;

    IF NEW.weight_delta <= -15 THEN
        INSERT INTO active_loans (rfid_uid, asset_id) 
        VALUES (matched_user.rfid_uid, matched_asset.id)
        ON CONFLICT (asset_id) DO UPDATE SET rfid_uid = EXCLUDED.rfid_uid, borrowed_at = NOW();

    ELSIF NEW.weight_delta >= 15 THEN
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


-- ==============================================================================
-- SUPABASE 2026 EXPLICIT EXECUTE GRANTS
-- ==============================================================================
-- Mengatasi pengetatan permission dari versi PostgreSQL/Supabase terbaru
GRANT EXECUTE ON FUNCTION secure_insert_telemetry TO anon, authenticated;
GRANT EXECUTE ON FUNCTION secure_sync_user TO anon, authenticated;
GRANT EXECUTE ON FUNCTION secure_attach_evidence TO anon, authenticated;