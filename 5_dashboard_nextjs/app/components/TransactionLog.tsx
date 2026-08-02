'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export default function TransactionLog() {
  const [logs, setLogs] = useState<any[]>([]);

  const fetchLogs = async () => {
    const { data, error } = await supabase
      .from('transactions_log')
      .select(`
        id, created_at, rfid_uid, weight_delta,
        users (
          nik,
          hr_employees ( full_name )
        )
      `)
      .order('created_at', { ascending: false })
      .limit(10);
    if (!error && data) setLogs(data);
  };

  useEffect(() => {
    fetchLogs();
    const channel = supabase.channel('realtime_logs')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'transactions_log' }, () => {
        fetchLogs(); // Re-fetch to get relational HR data on new insert
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden text-sm flex flex-col h-full">
      <div className="px-5 py-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
        <h3 className="font-bold text-slate-800 tracking-tight">Audit Trail</h3>
        <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">10 Aktivitas Terakhir</span>
      </div>
      
      <ul className="divide-y divide-slate-100 flex-grow">
        {logs.map((log) => {
          const isTaken = log.weight_delta < -15;
          const isReturned = log.weight_delta > 15;
          
          // Krug's Law: Don't make me guess what the numbers mean.
          let actionText = 'Guncangan / Akses Ditolak';
          let badgeColor = 'bg-slate-100 text-slate-600 ring-slate-200';
          
          if (isTaken) {
            actionText = 'Aset Keluar';
            badgeColor = 'bg-rose-50 text-rose-700 ring-rose-200/60';
          } else if (isReturned) {
            actionText = 'Aset Masuk';
            badgeColor = 'bg-emerald-50 text-emerald-700 ring-emerald-200/60';
          }

          // SSOT Identity resolution
          const employeeName = log.users?.hr_employees?.full_name;
          const displayName = employeeName || 'Kartu Tidak Terdaftar';
          const isUnregistered = !employeeName;

          return (
            <li key={log.id} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-slate-50 transition-colors">
              <div className="flex flex-col mb-3 sm:mb-0">
                <span className={`font-bold ${isUnregistered ? 'text-rose-600' : 'text-slate-900'} truncate max-w-[200px]`}>
                  {displayName}
                </span>
                <div className="flex items-center space-x-2 mt-1">
                  <span className="text-xs font-mono text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                    UID: {log.rfid_uid}
                  </span>
                  <span className="text-xs font-medium text-slate-500 tabular-nums">
                    {new Date(log.created_at).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-end space-x-3">
                <span className="text-slate-500 font-mono text-xs tabular-nums w-16 text-right">
                  {log.weight_delta > 0 ? '+' : ''}{log.weight_delta}g
                </span>
                {/* DOET Signifier: Badge with strict, unmissable semantic color */}
                <span className={`px-2.5 py-1 text-xs font-bold rounded-md ring-1 ring-inset ${badgeColor} w-24 text-center`}>
                  {actionText}
                </span>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}