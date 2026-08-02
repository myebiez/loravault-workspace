'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export default function ActiveLoansTable() {
  const [loans, setLoans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLoans = async () => {
    // DOET: Conceptual Model - We pull the exact truth from the SSOT relational database.
    const { data, error } = await supabase
      .from('active_loans')
      .select(`
        id,
        borrowed_at,
        assets ( name ),
        users (
          nik,
          hr_employees ( full_name, department )
        )
      `)
      .order('borrowed_at', { ascending: false });

    if (!error && data) setLoans(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchLoans();
    const channel = supabase.channel('realtime_loans')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'active_loans' }, () => {
        fetchLoans();
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  // Krug's Law: Obvious System Status. Minimalist loading state.
  if (loading) {
    return (
      <div className="p-8 text-slate-500 font-medium animate-pulse flex items-center justify-center bg-white border border-slate-200 rounded-xl">
        Memuat status aset...
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
          <tr>
            <th className="p-4 font-semibold tracking-tight">Nama Aset</th>
            <th className="p-4 font-semibold tracking-tight">Peminjam</th>
            <th className="p-4 font-semibold tracking-tight">Departemen</th>
            <th className="p-4 font-semibold tracking-tight text-right">Waktu Peminjaman</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {loans.length === 0 ? (
            <tr>
              {/* DOET Feedback: Explicitly state when system is perfectly secure. */}
              <td colSpan={4} className="p-10 text-center text-slate-500 font-medium">
                Semua aset aman di dalam brankas. Tidak ada peminjaman aktif.
              </td>
            </tr>
          ) : (
            loans.map((loan) => {
              // Safe navigation for relational data
              const employee = loan.users?.hr_employees;
              const fullName = employee?.full_name || 'Unknown (Unregistered)';
              const dept = employee?.department || '-';
              
              return (
                <tr key={loan.id} className="hover:bg-slate-50 transition-colors duration-150">
                  <td className="p-4 font-bold text-slate-900">{loan.assets?.name}</td>
                  <td className="p-4">
                    <span className="block font-semibold text-slate-800">{fullName}</span>
                    <span className="block text-xs font-mono text-slate-400 mt-0.5">NIK: {loan.users?.nik}</span>
                  </td>
                  <td className="p-4 text-slate-600 font-medium">{dept}</td>
                  <td className="p-4 text-slate-500 tabular-nums text-right">
                    {new Date(loan.borrowed_at).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })}
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}