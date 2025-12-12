/**
 * useFormatters Hook
 *
 * React hook that provides locale-aware formatting functions
 * integrated with the i18n LanguageContext.
 */

'use client';

import { useMemo } from 'react';
import { useLanguage } from './language-context';
import { createFormatters } from './formatters';

/**
 * Hook that provides internationalized formatting utilities
 * based on the current language from LanguageContext
 */
export function useFormatters(currency?: string) {
  const { currentLanguage } = useLanguage();

  const formatters = useMemo(() => {
    return createFormatters({
      locale: currentLanguage,
      currency,
    });
  }, [currentLanguage, currency]);

  return formatters;
}

/**
 * Hook variant that doesn't require LanguageContext
 * Useful for standalone components or server-side rendering
 */
export function useFormattersWithLocale(locale: string, currency?: string) {
  const formatters = useMemo(() => {
    return createFormatters({
      locale,
      currency,
    });
  }, [locale, currency]);

  return formatters;
}
