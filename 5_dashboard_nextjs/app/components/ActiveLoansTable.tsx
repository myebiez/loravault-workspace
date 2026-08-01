'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export default function ActiveLoansTable() {
  const [loans, setLoans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLoans = async () => {
    const { data, error } = await supabase
      .from('active_loans')
      .select(`
        id,
        borrowed_at,
        users ( full_name, department ),
        assets ( name )
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

  // Following Krug's Rule 1 (Clarity over Cleverness) & Rule 6 (Omit Needless Words):
  // Changed "Synchronizing with Cloud Brain..." to standard, expected terminology.
  if (loading) return <div className="p-4 text-gray-700 font-medium animate-pulse">Loading active loans...</div>;

  return (
    <div className="bg-white border border-gray-300 rounded-md shadow-sm overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead className="bg-gray-50 text-gray-900 border-b border-gray-300">
          <tr>
            {/* Following Krug's Rule 2: Design for Scanning. Strong visual hierarchy on headers. */}
            <th className="p-4 font-bold">Asset Name</th>
            <th className="p-4 font-bold">Borrower</th>
            <th className="p-4 font-bold">Department</th>
            <th className="p-4 font-bold">Date & Time</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {loans.length === 0 ? (
            <tr>
              {/* Omit needless words / happy talk: Straight to the point. */}
              <td colSpan={4} className="p-8 text-center text-gray-600 bg-gray-50 font-medium">
                No active loans. All assets are in the vault.
              </td>
            </tr>
          ) : (
            loans.map((loan) => (
              <tr key={loan.id} className="hover:bg-blue-50 transition-colors">
                {/* Visual Hierarchy: The item missing is the most critical piece of info. */}
                <td className="p-4 font-bold text-gray-900">{loan.assets.name}</td>
                <td className="p-4 text-gray-800">{loan.users.full_name}</td>
                <td className="p-4 text-gray-600">{loan.users.department}</td>
                <td className="p-4 text-gray-600 tabular-nums">
                  {new Date(loan.borrowed_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}