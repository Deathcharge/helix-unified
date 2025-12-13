/** @type {import('next-i18next').UserConfig} */
module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr', 'de', 'hi', 'sa', 'zh-CN', 'ar', 'pt', 'bn', 'ru', 'ja', 'ko', 'it', 'tr', 'vi'], // Top 15 languages by speakers
    localeDetection: true,
  },
  fallbackLng: {
    default: ['en'],
  },
  localePath: typeof window === 'undefined' ? require('path').resolve('./public/locales') : '/locales',
  reloadOnPrerender: process.env.NODE_ENV === 'development',
};
