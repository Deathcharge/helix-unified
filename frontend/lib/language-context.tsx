'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import i18n from './i18n';

interface LanguageContextType {
  currentLanguage: string;
  changeLanguage: (lang: string) => Promise<void>;
  availableLanguages: { code: string; name: string; nativeName: string }[];
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const availableLanguages = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'zh-CN', name: 'Chinese (Simplified)', nativeName: '简体中文' },
  { code: 'es', name: 'Spanish', nativeName: 'Español' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية' },
  { code: 'pt', name: 'Portuguese', nativeName: 'Português' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  { code: 'ru', name: 'Russian', nativeName: 'Русский' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語' },
  { code: 'fr', name: 'French', nativeName: 'Français' },
  { code: 'de', name: 'German', nativeName: 'Deutsch' },
  { code: 'ko', name: 'Korean', nativeName: '한국어' },
  { code: 'it', name: 'Italian', nativeName: 'Italiano' },
  { code: 'tr', name: 'Turkish', nativeName: 'Türkçe' },
  { code: 'vi', name: 'Vietnamese', nativeName: 'Tiếng Việt' },
  { code: 'sa', name: 'Sanskrit', nativeName: 'संस्कृतम्' },
];

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const { i18n: i18nInstance } = useTranslation();
  const [currentLanguage, setCurrentLanguage] = useState(i18nInstance.language || 'en');

  useEffect(() => {
    // Initialize i18n
    i18n.changeLanguage(currentLanguage);
  }, []);

  const changeLanguage = async (lang: string) => {
    await i18nInstance.changeLanguage(lang);
    setCurrentLanguage(lang);

    // Store in localStorage
    localStorage.setItem('i18nextLng', lang);

    // Update user preference in backend if logged in
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/me/preferences`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ language: lang }),
        });
        if (!response.ok) {
          console.error('Failed to update language preference');
        }
      }
    } catch (error) {
      console.error('Failed to update language preference:', error);
    }
  };

  return (
    <LanguageContext.Provider
      value={{
        currentLanguage,
        changeLanguage,
        availableLanguages
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
