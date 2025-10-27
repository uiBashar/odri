import React, { useEffect, useMemo, useState } from 'react'
import { Card } from './components/ui/Card'
import { Button } from './components/ui/Button'
import { Input } from './components/ui/Input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/Tabs'
import { UserPlus, ArrowDownCircle, ArrowUpCircle, X } from 'lucide-react'
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts'
import { motion, AnimatePresence } from 'framer-motion'

type TransactionType = 'take' | 'give'

interface Client {
  id: number
  name: string
  phone: string
  balance: number
}

interface Transaction {
  id: number
  client: string
  type: TransactionType
  amount: number
  date: string
}

export default function App() {
  const [currencySymbol, setCurrencySymbol] = useState<string>('৳')

  const [clients, setClients] = useState<Client[]>(() => {
    const saved = localStorage.getItem('clients')
    return saved
      ? JSON.parse(saved)
      : [
          { id: 1, name: 'Umair Abubakkar', phone: '03331652551', balance: 500 },
          { id: 2, name: 'Ali Khan', phone: '03331567890', balance: -1200 },
        ]
  })

  const [transactions, setTransactions] = useState<Transaction[]>(() => {
    const saved = localStorage.getItem('transactions')
    return saved
      ? JSON.parse(saved)
      : [
          { id: 1, client: 'Umair Abubakkar', type: 'take', amount: 500, date: '24 Jun 2025' },
          { id: 2, client: 'Ali Khan', type: 'give', amount: 1200, date: '22 Jun 2025' },
        ]
  })

  useEffect(() => localStorage.setItem('clients', JSON.stringify(clients)), [clients])
  useEffect(() => localStorage.setItem('transactions', JSON.stringify(transactions)), [transactions])
  useEffect(() => {
    const saved = localStorage.getItem('currencySymbol')
    if (saved) setCurrencySymbol(saved)
  }, [])
  useEffect(() => localStorage.setItem('currencySymbol', currencySymbol), [currencySymbol])

  const [newClient, setNewClient] = useState<{ name: string; phone: string }>({ name: '', phone: '' })
  const [modal, setModal] = useState<{ open: boolean; type: TransactionType; clientId: number | null; amount: string }>({ open: false, type: 'take', clientId: null, amount: '' })

  const totalGet = useMemo(() => clients.filter(c => c.balance > 0).reduce((sum, c) => sum + c.balance, 0), [clients])
  const totalGive = useMemo(() => clients.filter(c => c.balance < 0).reduce((sum, c) => sum + Math.abs(c.balance), 0), [clients])

  const COLORS = ['#167678', '#D13264']
  const chartData = [
    { name: 'Get', value: totalGet },
    { name: 'Give', value: totalGive },
  ]

  const formatDate = (date: Date = new Date()) =>
    date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

  const formatMoney = (n: number) => `${currencySymbol}${Math.abs(n).toLocaleString()}`

  const handleAddClient = () => {
    if (!newClient.name.trim()) return
    setClients([...clients, { id: Date.now(), name: newClient.name.trim(), phone: newClient.phone.trim(), balance: 0 }])
    setNewClient({ name: '', phone: '' })
  }

  const handleTransaction = () => {
    if (!modal.clientId) return
    const amountNum = Number(modal.amount)
    if (!Number.isFinite(amountNum) || amountNum <= 0) return

    const client = clients.find(c => c.id === modal.clientId)!
    const type = modal.type

    setTransactions([
      ...transactions,
      { id: Date.now(), client: client.name, type, amount: amountNum, date: formatDate(new Date()) },
    ])

    setClients(
      clients.map(c =>
        c.id === modal.clientId ? { ...c, balance: type === 'take' ? c.balance + amountNum : c.balance - amountNum } : c,
      ),
    )

    setModal({ open: false, type: 'take', clientId: null, amount: '' })
  }

  return (
    <div className="p-4 max-w-5xl mx-auto font-sans">
      <motion.h1 initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-2xl font-bold mb-4">
        BizFlow — Money Tracker
      </motion.h1>

      <Tabs defaultValue="dashboard" className="space-y-4">
        <TabsList>
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="clients">Clients</TabsTrigger>
          <TabsTrigger value="transactions">Transactions</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="dashboard">
          <div className="grid md:grid-cols-3 gap-4">
            <Card className="bg-[#167678]/10 p-4">
              <p className="text-sm text-gray-600">You’ll Get</p>
              <h2 className="text-2xl font-bold text-[#167678]">{formatMoney(totalGet)}</h2>
            </Card>

            <Card className="bg-[#D13264]/10 p-4">
              <p className="text-sm text-gray-600">You’ll Give</p>
              <h2 className="text-2xl font-bold text-[#D13264]">{formatMoney(totalGive)}</h2>
            </Card>

            <Card className="p-4">
              <p className="text-sm text-gray-600 mb-2">Money Flow</p>
              <ResponsiveContainer width="100%" height={120}>
                <PieChart>
                  <Pie data={chartData} dataKey="value" nameKey="name" innerRadius={35} outerRadius={50} label>
                    {chartData.map((_, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>
          </div>

          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Recent Transactions</h2>
            <div className="space-y-2">
              {transactions.slice(0, 3).map(tx => (
                <Card key={tx.id} className="p-4 flex justify-between">
                  <div>
                    <p className="font-medium">{tx.client}</p>
                    <p className="text-sm text-gray-500">{tx.date}</p>
                  </div>
                  <p className={`font-bold ${tx.type === 'take' ? 'text-[#167678]' : 'text-[#D13264]'}`}>
                    {tx.type === 'take' ? `+${formatMoney(tx.amount)}` : `-${formatMoney(tx.amount)}`}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="clients">
          <div className="space-y-4">
            <div className="flex gap-2">
              <Input placeholder="Client Name" value={newClient.name} onChange={e => setNewClient({ ...newClient, name: e.target.value })} />
              <Input placeholder="Phone" value={newClient.phone} onChange={e => setNewClient({ ...newClient, phone: e.target.value })} />
              <Button onClick={handleAddClient}><UserPlus className="w-4 h-4 mr-1" /> Add</Button>
            </div>

            <div className="grid md:grid-cols-2 gap-3">
              {clients.map(client => (
                <Card key={client.id} className="p-4 flex justify-between items-center">
                  <div>
                    <p className="font-semibold">{client.name}</p>
                    <p className="text-sm text-gray-500">{client.phone}</p>
                  </div>
                  <p className={`font-bold ${client.balance >= 0 ? 'text-[#167678]' : 'text-[#D13264]'}`}>
                    {client.balance >= 0 ? `+${formatMoney(client.balance)}` : `-${formatMoney(client.balance)}`}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="transactions">
          <div className="space-y-3">
            {transactions.map(tx => (
              <Card key={tx.id} className="p-4 flex justify-between">
                <div>
                  <p className="font-medium">{tx.client}</p>
                  <p className="text-sm text-gray-500">{tx.date}</p>
                </div>
                <p className={`font-bold ${tx.type === 'take' ? 'text-[#167678]' : 'text-[#D13264]'}`}>
                  {tx.type === 'take' ? `+${formatMoney(tx.amount)}` : `-${formatMoney(tx.amount)}`}
                </p>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="settings">
          <Card className="p-4 space-y-3">
            <div>
              <p className="text-sm font-medium">Currency</p>
              <Input placeholder="৳ / $ / ₹" value={currencySymbol} onChange={e => setCurrencySymbol(e.target.value || '৳')} />
            </div>
            <div>
              <p className="text-sm font-medium">Language</p>
              <Input placeholder="English / বাংলা" />
            </div>
            <div>
              <p className="text-sm font-medium">Notifications</p>
              <Button variant="outline">Enable</Button>
            </div>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="fixed bottom-6 right-6 flex gap-3">
        <Button
          className="bg-[#167678] hover:bg-[#125d5f] text-white shadow-lg rounded-full px-4 py-2 flex items-center"
          onClick={() => clients.length && setModal({ open: true, type: 'take', clientId: clients[0]?.id ?? null, amount: '' })}
          disabled={!clients.length}
        >
          <ArrowDownCircle className="w-5 h-5 mr-1" /> Take Money
        </Button>
        <Button
          className="bg-[#D13264] hover:bg-[#a5284f] text-white shadow-lg rounded-full px-4 py-2 flex items-center"
          onClick={() => clients.length && setModal({ open: true, type: 'give', clientId: clients[0]?.id ?? null, amount: '' })}
          disabled={!clients.length}
        >
          <ArrowUpCircle className="w-5 h-5 mr-1" /> Give Money
        </Button>
      </div>

      <AnimatePresence>
        {modal.open && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <motion.div initial={{ scale: 0.8 }} animate={{ scale: 1 }} exit={{ scale: 0.8 }} className="bg-white rounded-lg p-6 w-80 space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold">{modal.type === 'take' ? 'Take Money' : 'Give Money'}</h2>
                <Button variant="ghost" onClick={() => setModal({ ...modal, open: false })}><X /></Button>
              </div>
              <div className="space-y-2">
                <p className="text-sm font-medium">Select Client</p>
                <select className="w-full border px-3 py-2 rounded" value={modal.clientId ?? ''} onChange={e => setModal({ ...modal, clientId: Number(e.target.value) || null })}>
                  {!clients.length && <option value="" disabled>No clients available</option>}
                  {clients.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <p className="text-sm font-medium">Amount</p>
                <Input type="number" placeholder="Enter amount" value={modal.amount} onChange={e => setModal({ ...modal, amount: e.target.value })} />
              </div>
              <Button className="w-full" onClick={handleTransaction}>Submit</Button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

