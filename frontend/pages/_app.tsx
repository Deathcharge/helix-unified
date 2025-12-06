/**
 * 📱 Next.js App Wrapper
 * Global styles, layout, and providers
 */

import type { AppProps } from 'next/app';
import { useRouter } from 'next/router';
import Navigation from '@/components/Navigation';
import { ToastProvider } from '@/components/ui/Toast';
import '../styles/globals.css';

// Pages that should NOT show navigation (full-screen experiences)
const PAGES_WITHOUT_NAV = ['/os'];

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();
  const showNav = !PAGES_WITHOUT_NAV.includes(router.pathname);

  return (
    <ToastProvider>
      {showNav && <Navigation />}
      <Component {...pageProps} />
    </ToastProvider>
  );
}
