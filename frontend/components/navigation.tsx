'use client';

import React from 'react';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import { CompactLanguageSelector } from './language-selector';
import { Button } from './ui/button';
import { Home, Store, BookOpen } from 'lucide-react';

export function Navigation() {
  const { t } = useTranslation();

  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent">
              {t('app.name')}
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            <Link href="/" className="flex items-center space-x-2 text-sm font-medium transition-colors hover:text-primary">
              <Home className="h-4 w-4" />
              <span>{t('nav.home')}</span>
            </Link>
            <Link href="/marketplace" className="flex items-center space-x-2 text-sm font-medium transition-colors hover:text-primary">
              <Store className="h-4 w-4" />
              <span>Marketplace</span>
            </Link>
            <Link href="/learn-sanskrit" className="flex items-center space-x-2 text-sm font-medium transition-colors hover:text-primary">
              <BookOpen className="h-4 w-4" />
              <span>{t('nav.learnSanskrit')}</span>
            </Link>
          </div>

          {/* Language Selector & Auth */}
          <div className="flex items-center space-x-4">
            <CompactLanguageSelector />
            <Button variant="ghost" size="sm">
              {t('nav.login')}
            </Button>
            <Button size="sm">
              {t('nav.signup')}
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
