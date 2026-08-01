'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { Activity, AlertTriangle } from 'lucide-react';

export default function RealtimeIndicator() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      const { error } = await supabase.from('assets').select('id').limit(1);
      setIsConnected(!error);
    };
    checkConnection();
    
    const channel = supabase.channel('system_health')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'transactions_log' }, () => {
         setIsConnected(true);
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  // Following Krug's 3rd Law (Omit Needless Words) and 1st Law (Don't Make Me Think):
  // Removed the text "System Status:". A pill badge is a universally understood convention for system health.
  return (
    <div className="flex items-center text-sm font-bold tracking-wide uppercase">
      {isConnected ? (
        <span className="flex items-center bg-green-100 text-green-800 px-3 py-1 rounded-full border border-green-200">
          <Activity className="w-4 h-4 mr-2" /> Live Connection
        </span>
      ) : (
        <span className="flex items-center bg-red-100 text-red-800 px-3 py-1 rounded-full border border-red-200">
          <AlertTriangle className="w-4 h-4 mr-2" /> Disconnected
        </span>
      )}
    </div>
  );
}