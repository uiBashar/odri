import React from 'react'

type Variant = 'default' | 'outline' | 'ghost'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
}

export function Button({ className = '', variant = 'default', ...props }: ButtonProps) {
  const base = 'inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
  const styles: Record<Variant, string> = {
    default: 'bg-gray-900 text-white hover:bg-gray-800 focus:ring-gray-400',
    outline: 'border border-gray-300 text-gray-900 hover:bg-gray-50 focus:ring-gray-300',
    ghost: 'text-gray-600 hover:bg-gray-100 focus:ring-gray-200',
  }
  return <button className={`${base} ${styles[variant]} ${className}`} {...props} />
}

