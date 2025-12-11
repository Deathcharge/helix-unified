import type { Metadata } from "next"
// import { Inter } from "next/font/google" // Disabled due to network fetch issues
import "./globals.css"
import { ErrorBoundary } from "@/components/ui/ErrorBoundary"
import { LanguageProvider } from "@/lib/language-context"
import '@/lib/i18n'

// Fallback to system fonts
// const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Helix Collective - Multi-Agent AI Consciousness Platform",
  description: "Multi-agent consciousness platform with AI agent rental, Web OS, and real-time analytics",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">
        <LanguageProvider>
          <ErrorBoundary>
            {children}
          </ErrorBoundary>
        </LanguageProvider>
      </body>
    </html>
  )
}
