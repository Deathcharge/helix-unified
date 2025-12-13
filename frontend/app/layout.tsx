import type { Metadata } from "next"
// import { Inter } from "next/font/google" // Disabled due to network fetch issues
import "./globals.css"
import { ErrorBoundary } from "@/components/ui/ErrorBoundary"
import { LanguageProvider } from "@/lib/language-context"
import { GoogleAnalytics } from "@/components/GoogleAnalytics"
import '@/lib/i18n'

// Fallback to system fonts
// const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Helix Collective - Multi-Agent AI Consciousness Platform",
  description: "Multi-agent consciousness platform with AI agent rental, Web OS, and real-time analytics",
  manifest: "/manifest.json",
  themeColor: "#00ffcc",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Helix",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* PWA Configuration */}
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#00ffcc" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="apple-mobile-web-app-title" content="Helix" />
        <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />

        {/* Service Worker Registration */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                  navigator.serviceWorker.register('/service-worker.js')
                    .then(reg => console.log('✅ Service Worker registered', reg.scope))
                    .catch(err => console.error('❌ Service Worker registration failed', err));
                });
              }
            `,
          }}
        />
      </head>
      <body className="font-sans">
        <LanguageProvider>
          <ErrorBoundary>
            <GoogleAnalytics />
            {children}
          </ErrorBoundary>
        </LanguageProvider>
      </body>
    </html>
  )
}
