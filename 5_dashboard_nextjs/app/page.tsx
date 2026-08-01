import RealtimeIndicator from './components/RealtimeIndicator';
import ActiveLoansTable from './components/ActiveLoansTable';
import TransactionLog from './components/TransactionLog';
import { ShieldCheck } from 'lucide-react';

export default function CommandCenter() {
  return (
    <main className="max-w-7xl mx-auto p-4 sm:p-8 lg:p-12">
      
      {/* 
        Following Krug's Rule 4 (Trunk Test) & Rule 6 (Omit Needless Words):
        Removed marketing speak ("Enterprise Hybrid-Mesh System").
        Replaced with a descriptive, obvious title. 
      */}
      <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 pb-6 border-b border-gray-300">
        <div className="flex items-center space-x-4 mb-4 sm:mb-0">
          <div className="p-3 bg-blue-700 text-white rounded-md shadow-sm">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-gray-900">LoRaVault</h1>
            <p className="text-gray-600 font-medium">Security Dashboard</p>
          </div>
        </div>
        <RealtimeIndicator />
      </header>

      {/* 
        Following Krug's Rule 8 (Visual Hierarchy) & Rule 9 (Mobile & Touch): 
        Changed grid mapping to allow vertical stacking on smaller screens. 
      */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left/Main Column: Human-readable business state */}
        <section className="lg:col-span-2 flex flex-col space-y-4">
          <h2 className="text-lg font-bold text-gray-900">
            Currently Borrowed Assets
          </h2>
          <ActiveLoansTable />
        </section>

        {/* 
          Right Column: Raw system telemetry 
          Following Rule 1 (Clarity over Cleverness): Renamed "Hardware Telemetry stream" to "System Log".
        */}
        <section className="flex flex-col space-y-4">
          <h2 className="text-lg font-bold text-gray-900">
            System Log
          </h2>
          <TransactionLog />
        </section>
        
      </div>
    </main>
  );
}