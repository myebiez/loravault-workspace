'use client';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

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

  // DOET: Immediate visual feedback. Clean, professional beacon.
  return (
    <div className="flex items-center">
      {isConnected ? (
        <div className="flex items-center space-x-2 bg-emerald-50 text-emerald-700 px-3 py-1.5 rounded-full ring-1 ring-inset ring-emerald-500/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-bold uppercase tracking-wider">System Live</span>
        </div>
      ) : (
        <div className="flex items-center space-x-2 bg-rose-50 text-rose-700 px-3 py-1.5 rounded-full ring-1 ring-inset ring-rose-500/20">
          <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
          <span className="text-xs font-bold uppercase tracking-wider">Disconnected</span>
        </div>
      )}
    </div>
  );
}