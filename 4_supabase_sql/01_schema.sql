-- Pragmatic Programmer: Design by Contract. 
-- We enforce data integrity at the lowest level. No nulls, strict types, and clear relationships.

-- 1. Users Table (Maps RFID UIDs to Human Identities)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rfid_uid VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR NOT NULL,
    department VARCHAR NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Assets Table (The Vault's Inventory)
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    baseline_weight_g NUMERIC NOT NULL,
    tolerance_g NUMERIC NOT NULL DEFAULT 15, -- DOET: Error Recovery. Load cells drift; we allow a margin of error.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Transactions Log (Immutable Ledger inserted by ESP32)
CREATE TABLE transactions_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rfid_uid VARCHAR NOT NULL, -- Not a strict FK to allow unregistered anomaly taps
    weight_delta NUMERIC NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Active Loans (State derived from Transactions)
CREATE TABLE active_loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    borrowed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(asset_id) -- An asset can only be borrowed by one person at a time
);

-- CLRS: Asymptotic Efficiency. 
-- B-Tree indexes ensure \mathcal{O}(\log N) time complexity for range scans and exact matches.
CREATE INDEX idx_users_rfid ON users USING btree(rfid_uid);
CREATE INDEX idx_transactions_created ON transactions_log USING btree(created_at DESC);
CREATE INDEX idx_assets_weight ON assets USING btree(baseline_weight_g);