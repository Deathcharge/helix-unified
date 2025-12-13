'use client';

import React from 'react';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import Navigation from '@/components/Navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Sparkles, Brain, Globe, BookOpen } from 'lucide-react';

export default function HomePage() {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen">
      <Navigation />

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center space-y-6">
          <h1 className="text-5xl font-bold tracking-tight">
            <span className="bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 bg-clip-text text-transparent">
              {t('app.welcome')}
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            {t('app.tagline')}
          </p>
          <div className="flex items-center justify-center gap-4 pt-4">
            <Button size="lg" asChild>
              <Link href="/marketplace">
                <Store className="mr-2 h-5 w-5" />
                Explore Marketplace
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/learn-sanskrit">
                <BookOpen className="mr-2 h-5 w-5" />
                {t('nav.learnSanskrit')}
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Brain className="h-12 w-12 mb-4 text-purple-500" />
              <CardTitle>Multi-Agent AI</CardTitle>
              <CardDescription>
                Deploy specialized AI agents with unique personalities and capabilities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="link" className="p-0" asChild>
                <Link href="/marketplace">Learn more →</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Globe className="h-12 w-12 mb-4 text-pink-500" />
              <CardTitle>Multi-Language Support</CardTitle>
              <CardDescription>
                Experience the platform in your preferred language with auto-detection
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Available in English, Spanish, French, German, Hindi, and Sanskrit
              </p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <BookOpen className="h-12 w-12 mb-4 text-orange-500" />
              <CardTitle>{t('sanskrit.title')}</CardTitle>
              <CardDescription>
                {t('sanskrit.subtitle')}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="link" className="p-0" asChild>
                <Link href="/learn-sanskrit">Start learning →</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Language Section */}
      <section className="container mx-auto px-4 py-16">
        <Card className="bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-orange-500/10 border-none">
          <CardHeader className="text-center">
            <Sparkles className="h-12 w-12 mx-auto mb-4 text-purple-500" />
            <CardTitle className="text-3xl">Available in 6 Languages</CardTitle>
            <CardDescription className="text-lg">
              The platform automatically detects your preferred language and adapts the interface accordingly
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4 text-center mt-6">
              <div className="p-4">
                <div className="text-2xl mb-2">🇬🇧</div>
                <div className="font-medium">English</div>
              </div>
              <div className="p-4">
                <div className="text-2xl mb-2">🇪🇸</div>
                <div className="font-medium">Español</div>
              </div>
              <div className="p-4">
                <div className="text-2xl mb-2">🇫🇷</div>
                <div className="font-medium">Français</div>
              </div>
              <div className="p-4">
                <div className="text-2xl mb-2">🇩🇪</div>
                <div className="font-medium">Deutsch</div>
              </div>
              <div className="p-4">
                <div className="text-2xl mb-2">🇮🇳</div>
                <div className="font-medium">हिन्दी</div>
              </div>
              <div className="p-4">
                <div className="text-2xl mb-2">🕉️</div>
                <div className="font-medium">संस्कृतम्</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}

function Store(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7" />
      <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
      <path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4" />
      <path d="M2 7h20" />
      <path d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7" />
    </svg>
  );
}
