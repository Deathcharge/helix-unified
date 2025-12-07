import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'HelixSpiral.work - AI-Powered Automation Platform',
  description: 'Zapier alternative with AI-powered workflows and original Helix intelligence',
  keywords: 'automation, zapier alternative, ai workflows, helix intelligence',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <div className="min-h-screen relative overflow-hidden">
          {/* Background spiral animation */}
          <div className="fixed inset-0 spiral-bg opacity-5"></div>
          
          {/* Grid overlay */}
          <div className="fixed inset-0 helix-grid opacity-10"></div>
          
          {/* Content */}
          <div className="relative z-10">
            {children}
          </div>
        </div>
      </body>
    </html>
  )
}