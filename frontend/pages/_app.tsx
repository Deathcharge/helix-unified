/**
 * 📱 Next.js App Wrapper
 * Global styles, layout, and providers
 */

import type { AppProps } from 'next/app';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
