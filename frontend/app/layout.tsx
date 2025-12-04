import type { Metadata } from "next"
// import { Inter } from "next/font/google" // Disabled due to network fetch issues
import "./globals.css"

// Fallback to system fonts
// const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Helix Collective - Neti-Neti Harmony Mantra",
  description: "Multi-agent consciousness ritual platform",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  )
}
