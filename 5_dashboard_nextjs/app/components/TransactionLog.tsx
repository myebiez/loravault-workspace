'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export default function TransactionLog() {
  const [logs, setLogs] = useState<any[]>([]);

  const fetchLogs = async () => {
    const { data, error } = await supabase
      .from('transactions_log')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(10);
    if (!error && data) setLogs(data);
  };

  useEffect(() => {
    fetchLogs();
    const channel = supabase.channel('realtime_logs')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'transactions_log' }, (payload) => {
        setLogs((current) => [payload.new, ...current].slice(0, 10));
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  return (
    <div className="bg-white border border-gray-300 rounded-md shadow-sm overflow-hidden text-sm">
      <div className="p-4 bg-gray-50 border-b border-gray-300 font-bold text-gray-900">
        Recent Activity (Last 10)
      </div>
      <ul className="divide-y divide-gray-200">
        {logs.map((log) => {
          const isNegative = log.weight_delta < 0;
          
          // Following Krug's 1st Law (Don't Make Me Think) & 5th Law (Mindless Choices):
          // Users should not have to guess what -500g means. We explicitly state the action.
          const actionText = isNegative ? 'Taken' : 'Returned';
          const actionColor = isNegative ? 'text-red-700 bg-red-50' : 'text-green-700 bg-green-50';

          return (
            <li key={log.id} className="p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center hover:bg-gray-50 transition-colors">
              <div className="mb-2 sm:mb-0">
                <span className="font-semibold text-gray-900 block sm:inline mr-3">UID: {log.rfid_uid}</span>
                <span className="text-gray-500 text-xs sm:text-sm">
                  {new Date(log.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </span>
              </div>
              
              {/* Semantic formatting over raw technical data */}
              <div className="flex items-center space-x-2">
                <span className="text-gray-500 tabular-nums">({log.weight_delta > 0 ? '+' : ''}{log.weight_delta}g)</span>
                <span className={`font-bold px-2 py-1 rounded border ${actionColor} border-opacity-20`}>
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