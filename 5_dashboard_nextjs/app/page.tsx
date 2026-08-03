'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import RealtimeIndicator from './components/RealtimeIndicator';
import ActiveLoansTable from './components/ActiveLoansTable';
import TransactionLog from './components/TransactionLog';

export default function CommandCenter() {
  const [session, setSession] = useState<any>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Otentikasi: Cek apakah pengguna sudah login
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setError('Kredensial tidak valid. Akses ditolak.');
    setLoading(false);
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  // State 1: Memuat
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-slate-400 font-mono text-sm tracking-widest uppercase">Memverifikasi Otorisasi Jaringan...</div>;

  // State 2: Belum Login (Tampilkan Layar Login Eksekutif)
  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4">
        <div className="max-w-md w-full bg-slate-800 rounded-2xl shadow-2xl overflow-hidden border border-slate-700/50">
          <div className="px-8 pt-10 pb-8 text-center border-b border-slate-700/50">
            <h1 className="text-3xl font-extrabold tracking-tight text-white flex items-center justify-center">
              <span className="text-blue-500 mr-2">LoRa</span>Vault
            </h1>
            <p className="text-sm font-medium text-slate-400 mt-2">Sistem Audit & Forensik Kritis</p>
          </div>
          <form onSubmit={handleLogin} className="p-8 space-y-6">
            {error && (
              <div className="bg-rose-500/10 border border-rose-500/50 text-rose-400 text-sm font-bold p-3 rounded-lg text-center">
                {error}
              </div>
            )}
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">ID Pengguna (Email)</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" placeholder="admin@perusahaan.com" />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Kata Sandi Akses</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" placeholder="••••••••" />
            </div>
            <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-800 focus:ring-blue-500 disabled:opacity-50">
              {loading ? 'Mengautentikasi...' : 'Inisiasi Koneksi Aman'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // State 3: Sudah Login (Tampilkan Dasbor Eksekutif)
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-5 flex flex-col sm:flex-row justify-between items-start sm:items-center">
          <div className="mb-4 sm:mb-0">
            <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 flex items-center">
              <span className="text-blue-600 mr-2">LoRa</span>Vault
            </h1>
            <p className="text-sm font-medium text-slate-500 mt-1">Executive Security & Asset Monitor</p>
          </div>
          <div className="flex items-center space-x-6">
            <RealtimeIndicator />
            <div className="h-8 w-px bg-slate-200"></div>
            <div className="flex items-center space-x-3">
              <span className="text-xs font-bold text-slate-500 hidden md:block">{session.user.email}</span>
              <button onClick={handleLogout} className="text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 px-3 py-1.5 rounded-md transition-colors ring-1 ring-inset ring-rose-200">
                Log Out
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 lg:px-8 mt-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <section className="lg:col-span-2 flex flex-col">
            <div className="mb-4">
              <h2 className="text-lg font-bold text-slate-800 tracking-tight">Status Aset Berjalan</h2>
              <p className="text-sm text-slate-500">Pantauan real-time inventaris yang sedang digunakan di luar brankas.</p>
            </div>
            <ActiveLoansTable />
          </section>

          <section className="flex flex-col">
            <div className="mb-4">
              <h2 className="text-lg font-bold text-slate-800 tracking-tight">Log Transaksi</h2>
              <p className="text-sm text-slate-500">Jejak audit fisik pintu brankas.</p>
            </div>
            <TransactionLog />
          </section>
        </div>
      </div>
    </main>
  );
}