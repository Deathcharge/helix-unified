/**
 * Internationalized Formatting Utilities
 *
 * Provides locale-aware formatting for dates, numbers, and currencies
 * using the Intl API with i18n context integration.
 */

export interface FormattersConfig {
  locale: string;
  currency?: string;
  timeZone?: string;
}

/**
 * Locale to currency mapping
 * Maps language codes to their primary currencies
 */
const LOCALE_CURRENCY_MAP: Record<string, string> = {
  'en': 'USD',
  'en-US': 'USD',
  'en-GB': 'GBP',
  'en-CA': 'CAD',
  'en-AU': 'AUD',
  'es': 'EUR',
  'es-ES': 'EUR',
  'es-MX': 'MXN',
  'fr': 'EUR',
  'de': 'EUR',
  'it': 'EUR',
  'pt': 'EUR',
  'pt-BR': 'BRL',
  'zh-CN': 'CNY',
  'ja': 'JPY',
  'ko': 'KRW',
  'ru': 'RUB',
  'ar': 'SAR',
  'ar-SA': 'SAR',
  'ar-AE': 'AED',
  'hi': 'INR',
  'bn': 'BDT',
  'tr': 'TRY',
  'vi': 'VND',
  'sa': 'INR', // Sanskrit -> INR (India)
};

/**
 * Get currency for locale
 */
function getCurrencyForLocale(locale: string): string {
  return LOCALE_CURRENCY_MAP[locale] || LOCALE_CURRENCY_MAP[locale.split('-')[0]] || 'USD';
}

/**
 * Create formatters for a specific locale
 */
export function createFormatters(config: FormattersConfig) {
  const { locale, currency = getCurrencyForLocale(locale), timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone } = config;

  return {
    /**
     * Format a date in short format (e.g., "12/31/2023" or "31/12/2023")
     */
    formatDate: (date: Date | string | number): string => {
      const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
      return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      }).format(d);
    },

    /**
     * Format a date in long format (e.g., "December 31, 2023")
     */
    formatDateLong: (date: Date | string | number): string => {
      const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
      return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }).format(d);
    },

    /**
     * Format a date with time (e.g., "12/31/2023, 3:45 PM")
     */
    formatDateTime: (date: Date | string | number): string => {
      const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
      return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZone,
      }).format(d);
    },

    /**
     * Format a date with full time (e.g., "December 31, 2023 at 3:45:30 PM UTC")
     */
    formatDateTimeLong: (date: Date | string | number): string => {
      const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
      return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short',
        timeZone,
      }).format(d);
    },

    /**
     * Format time only (e.g., "3:45 PM")
     */
    formatTime: (date: Date | string | number): string => {
      const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
      return new Intl.DateTimeFormat(locale, {
        hour: '2-digit',
        minute: '2-digit',
        timeZone,
      }).format(d);
    },

    /**
     * Format a relative time (e.g., "2 days ago", "in 3 hours")
     */
    formatRelativeTime: (date: Date | string | number): string => {
      const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date;
      const now = new Date();
      const diffMs = d.getTime() - now.getTime();
      const diffSeconds = Math.round(diffMs / 1000);
      const diffMinutes = Math.round(diffSeconds / 60);
      const diffHours = Math.round(diffMinutes / 60);
      const diffDays = Math.round(diffHours / 24);
      const diffMonths = Math.round(diffDays / 30);
      const diffYears = Math.round(diffDays / 365);

      const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

      if (Math.abs(diffSeconds) < 60) {
        return rtf.format(diffSeconds, 'second');
      } else if (Math.abs(diffMinutes) < 60) {
        return rtf.format(diffMinutes, 'minute');
      } else if (Math.abs(diffHours) < 24) {
        return rtf.format(diffHours, 'hour');
      } else if (Math.abs(diffDays) < 30) {
        return rtf.format(diffDays, 'day');
      } else if (Math.abs(diffMonths) < 12) {
        return rtf.format(diffMonths, 'month');
      } else {
        return rtf.format(diffYears, 'year');
      }
    },

    /**
     * Format a number (e.g., "1,234.56" or "1.234,56")
     */
    formatNumber: (value: number, options?: Intl.NumberFormatOptions): string => {
      return new Intl.NumberFormat(locale, options).format(value);
    },

    /**
     * Format a currency amount (e.g., "$1,234.56" or "€1.234,56")
     */
    formatCurrency: (
      value: number,
      currencyCode: string = currency,
      options?: Intl.NumberFormatOptions
    ): string => {
      return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currencyCode,
        ...options,
      }).format(value);
    },

    /**
     * Format a percentage (e.g., "45%" or "45,5%")
     */
    formatPercent: (value: number, options?: Intl.NumberFormatOptions): string => {
      return new Intl.NumberFormat(locale, {
        style: 'percent',
        ...options,
      }).format(value);
    },

    /**
     * Format a compact number (e.g., "1.2K", "3.4M")
     */
    formatCompact: (value: number): string => {
      return new Intl.NumberFormat(locale, {
        notation: 'compact',
        compactDisplay: 'short',
      }).format(value);
    },

    /**
     * Format a file size (bytes to human readable)
     */
    formatFileSize: (bytes: number): string => {
      const units = ['B', 'KB', 'MB', 'GB', 'TB'];
      let size = bytes;
      let unitIndex = 0;

      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
      }

      return `${new Intl.NumberFormat(locale, {
        maximumFractionDigits: 2,
      }).format(size)} ${units[unitIndex]}`;
    },

    /**
     * Format duration in seconds to human readable
     */
    formatDuration: (seconds: number): string => {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);

      const parts: string[] = [];
      if (hours > 0) parts.push(`${hours}h`);
      if (minutes > 0) parts.push(`${minutes}m`);
      if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);

      return parts.join(' ');
    },

    /**
     * Get locale info
     */
    getLocale: () => locale,
    getCurrency: () => currency,
    getTimeZone: () => timeZone,
  };
}

/**
 * Default formatters (English/USD)
 */
export const defaultFormatters = createFormatters({ locale: 'en-US' });
