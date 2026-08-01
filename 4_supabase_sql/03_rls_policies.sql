-- Pragmatic Programmer: Security by Default.
-- We do not trust the client. The ESP32 is only granted exact, minimal privileges.

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE active_loans ENABLE ROW LEVEL SECURITY;

-- 1. Transactions Log: The ESP32 (using the Anon Key) can ONLY insert. 
-- It cannot read, update, or delete history.
CREATE POLICY "ESP32 can insert transactions" 
ON transactions_log FOR INSERT 
TO anon 
WITH CHECK (true);

-- 2. Read Access: The Next.js Command Center (using Service Role or Authenticated User) 
-- can read everything.
CREATE POLICY "Command Center can read users" ON users FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center can read assets" ON assets FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center can read transactions" ON transactions_log FOR SELECT TO authenticated USING (true);
CREATE POLICY "Command Center can read loans" ON active_loans FOR SELECT TO authenticated USING (true);

-- Note: In Supabase, the 'service_role' key bypasses RLS automatically. 
-- We will use the service_role key in the Next.js server-side environment for full admin CRUD.