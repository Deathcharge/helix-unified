'use client';

import React from 'react';
import { useLanguage } from '@/lib/language-context';
import { useTranslation } from 'react-i18next';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Globe } from 'lucide-react';

export function LanguageSelector() {
  const { currentLanguage, changeLanguage, availableLanguages } = useLanguage();
  const { t } = useTranslation();

  return (
    <div className="flex items-center gap-2">
      <Globe className="h-4 w-4 text-muted-foreground" />
      <Select value={currentLanguage} onValueChange={changeLanguage}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder={t('language.select')} />
        </SelectTrigger>
        <SelectContent>
          {availableLanguages.map((lang) => (
            <SelectItem key={lang.code} value={lang.code}>
              <div className="flex items-center gap-2">
                <span>{lang.nativeName}</span>
                <span className="text-xs text-muted-foreground">
                  ({lang.name})
                </span>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

export function CompactLanguageSelector() {
  const { currentLanguage, changeLanguage, availableLanguages } = useLanguage();

  return (
    <Select value={currentLanguage} onValueChange={changeLanguage}>
      <SelectTrigger className="w-[60px] h-9">
        <SelectValue>
          <span className="text-sm font-medium uppercase">
            {currentLanguage}
          </span>
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {availableLanguages.map((lang) => (
          <SelectItem key={lang.code} value={lang.code}>
            <div className="flex flex-col">
              <span className="font-medium">{lang.nativeName}</span>
              <span className="text-xs text-muted-foreground">
                {lang.name}
              </span>
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
