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
import zhCNCommon from '@/public/locales/zh-CN/common.json';
import arCommon from '@/public/locales/ar/common.json';
import ptCommon from '@/public/locales/pt/common.json';
import bnCommon from '@/public/locales/bn/common.json';
import ruCommon from '@/public/locales/ru/common.json';
import jaCommon from '@/public/locales/ja/common.json';
import koCommon from '@/public/locales/ko/common.json';
import itCommon from '@/public/locales/it/common.json';
import trCommon from '@/public/locales/tr/common.json';
import viCommon from '@/public/locales/vi/common.json';

const resources = {
  en: { common: enCommon },
  es: { common: esCommon },
  fr: { common: frCommon },
  de: { common: deCommon },
  hi: { common: hiCommon },
  sa: { common: saCommon },
  'zh-CN': { common: zhCNCommon },
  ar: { common: arCommon },
  pt: { common: ptCommon },
  bn: { common: bnCommon },
  ru: { common: ruCommon },
  ja: { common: jaCommon },
  ko: { common: koCommon },
  it: { common: itCommon },
  tr: { common: trCommon },
  vi: { common: viCommon },
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
