import { createClient } from '@supabase/supabase-js';

// Pragmatic: Design by Contract. Fail fast and loudly if the environment is misconfigured.
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error("CRITICAL: Missing Supabase Environment Variables.");
}

// SICP: Singleton abstraction for the data layer transport.
export const supabase = createClient(supabaseUrl, supabaseKey);