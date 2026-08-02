import RealtimeIndicator from './components/RealtimeIndicator';
import ActiveLoansTable from './components/ActiveLoansTable';
import TransactionLog from './components/TransactionLog';

export default function CommandCenter() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 pb-12">
      {/* 
        Krug's Rule 4 (Trunk Test): User immediately knows where they are. 
        Executive Dashboard Header with deliberate whitespace.
      */}
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6 flex flex-col sm:flex-row justify-between items-start sm:items-center">
          <div className="mb-4 sm:mb-0">
            <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 flex items-center">
              <span className="text-blue-600 mr-2">LoRa</span>Vault
            </h1>
            <p className="text-sm font-medium text-slate-500 mt-1">Executive Security & Asset Monitor</p>
          </div>
          <RealtimeIndicator />
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 lg:px-8 mt-8">
        {/* 
          Krug's Rule 8 (Visual Hierarchy): The most important data (Missing Assets) takes up 2/3 of the screen width.
        */}
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