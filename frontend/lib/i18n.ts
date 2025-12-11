import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import enCommon from '@/public/locales/en/common.json';
import esCommon from '@/public/locales/es/common.json';
import frCommon from '@/public/locales/fr/common.json';
import deCommon from '@/public/locales/de/common.json';
import hiCommon from '@/public/locales/hi/common.json';
import saCommon from '@/public/locales/sa/common.json';

const resources = {
  en: { common: enCommon },
  es: { common: esCommon },
  fr: { common: frCommon },
  de: { common: deCommon },
  hi: { common: hiCommon },
  sa: { common: saCommon },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    defaultNS: 'common',
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',

    detection: {
      // Order of detection methods
      order: ['localStorage', 'cookie', 'navigator', 'htmlTag'],
      caches: ['localStorage', 'cookie'],
      lookupLocalStorage: 'i18nextLng',
      lookupCookie: 'i18next',
    },

    interpolation: {
      escapeValue: false, // React already escapes
    },

    react: {
      useSuspense: false,
    },
  });

export default i18n;
