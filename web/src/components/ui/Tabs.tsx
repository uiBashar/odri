import React, { useState } from 'react'

interface TabsProps {
  defaultValue: string
  className?: string
  children: React.ReactNode
}

interface TabsContextValue {
  value: string
  setValue: (v: string) => void
}

const TabsContext = React.createContext<TabsContextValue | null>(null)

export function Tabs({ defaultValue, className = '', children }: TabsProps) {
  const [value, setValue] = useState(defaultValue)
  return (
    <TabsContext.Provider value={{ value, setValue }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  )
}

export function TabsList({ children }: { children: React.ReactNode }) {
  return <div className="inline-flex rounded-md border border-gray-200 overflow-hidden">{children}</div>
}

export function TabsTrigger({ value, children }: { value: string; children: React.ReactNode }) {
  const ctx = React.useContext(TabsContext)!
  const active = ctx.value === value
  return (
    <button
      className={`px-4 py-2 text-sm font-medium ${active ? 'bg-gray-900 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'} border-r last:border-r-0`}
      onClick={() => ctx.setValue(value)}
    >
      {children}
    </button>
  )
}

export function TabsContent({ value, children }: { value: string; children: React.ReactNode }) {
  const ctx = React.useContext(TabsContext)!
  if (ctx.value !== value) return null
  return <div>{children}</div>
}

