'use client';

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Sparkles, Volume2, Award, ChevronRight } from 'lucide-react';

const devanagariVowels = [
  { char: 'अ', roman: 'a', sound: 'as in about' },
  { char: 'आ', roman: 'ā', sound: 'as in father' },
  { char: 'इ', roman: 'i', sound: 'as in sit' },
  { char: 'ई', roman: 'ī', sound: 'as in seek' },
  { char: 'उ', roman: 'u', sound: 'as in put' },
  { char: 'ऊ', roman: 'ū', sound: 'as in boot' },
  { char: 'ऋ', roman: 'ṛ', sound: 'as in rhythm' },
  { char: 'ए', roman: 'e', sound: 'as in say' },
  { char: 'ऐ', roman: 'ai', sound: 'as in aisle' },
  { char: 'ओ', roman: 'o', sound: 'as in go' },
  { char: 'औ', roman: 'au', sound: 'as in cow' },
];

const devanagariConsonants = [
  { char: 'क', roman: 'ka', group: 'Velar' },
  { char: 'ख', roman: 'kha', group: 'Velar' },
  { char: 'ग', roman: 'ga', group: 'Velar' },
  { char: 'घ', roman: 'gha', group: 'Velar' },
  { char: 'ङ', roman: 'ṅa', group: 'Velar' },
  { char: 'च', roman: 'ca', group: 'Palatal' },
  { char: 'छ', roman: 'cha', group: 'Palatal' },
  { char: 'ज', roman: 'ja', group: 'Palatal' },
  { char: 'झ', roman: 'jha', group: 'Palatal' },
  { char: 'ञ', roman: 'ña', group: 'Palatal' },
  { char: 'ट', roman: 'ṭa', group: 'Retroflex' },
  { char: 'ठ', roman: 'ṭha', group: 'Retroflex' },
  { char: 'ड', roman: 'ḍa', group: 'Retroflex' },
  { char: 'ढ', roman: 'ḍha', group: 'Retroflex' },
  { char: 'ण', roman: 'ṇa', group: 'Retroflex' },
  { char: 'त', roman: 'ta', group: 'Dental' },
  { char: 'थ', roman: 'tha', group: 'Dental' },
  { char: 'द', roman: 'da', group: 'Dental' },
  { char: 'ध', roman: 'dha', group: 'Dental' },
  { char: 'न', roman: 'na', group: 'Dental' },
  { char: 'प', roman: 'pa', group: 'Labial' },
  { char: 'फ', roman: 'pha', group: 'Labial' },
  { char: 'ब', roman: 'ba', group: 'Labial' },
  { char: 'भ', roman: 'bha', group: 'Labial' },
  { char: 'म', roman: 'ma', group: 'Labial' },
];

const mantras = [
  {
    sanskrit: 'ॐ',
    transliteration: 'Oṃ',
    english: 'The sacred sound of the universe',
    description: 'The primordial sound, representing the essence of ultimate reality'
  },
  {
    sanskrit: 'ॐ शान्तिः शान्तिः शान्तिः',
    transliteration: 'Oṃ śāntiḥ śāntiḥ śāntiḥ',
    english: 'Om peace peace peace',
    description: 'A mantra for peace in body, mind, and spirit'
  },
  {
    sanskrit: 'असतो मा सद्गमय। तमसो मा ज्योतिर्गमय। मृत्योर्मा अमृतं गमय।',
    transliteration: 'Asato mā sadgamaya. Tamaso mā jyotirgamaya. Mṛtyormā amṛtaṃ gamaya.',
    english: 'Lead me from untruth to truth. Lead me from darkness to light. Lead me from death to immortality.',
    description: 'From the Brihadaranyaka Upanishad'
  },
];

const lessons = [
  {
    id: 1,
    title: 'Introduction to Sanskrit',
    level: 'Beginner',
    duration: '15 min',
    topics: ['History', 'Importance', 'Basic concepts'],
  },
  {
    id: 2,
    title: 'Devanagari Script - Vowels',
    level: 'Beginner',
    duration: '20 min',
    topics: ['Vowels', 'Pronunciation', 'Writing'],
  },
  {
    id: 3,
    title: 'Devanagari Script - Consonants',
    level: 'Beginner',
    duration: '30 min',
    topics: ['Consonants', 'Classification', 'Practice'],
  },
  {
    id: 4,
    title: 'Basic Grammar - Nouns',
    level: 'Intermediate',
    duration: '25 min',
    topics: ['Gender', 'Number', 'Cases'],
  },
  {
    id: 5,
    title: 'Basic Grammar - Verbs',
    level: 'Intermediate',
    duration: '30 min',
    topics: ['Roots', 'Tenses', 'Conjugation'],
  },
];

export default function LearnSanskritPage() {
  const { t } = useTranslation();
  const [selectedTab, setSelectedTab] = useState('overview');

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 bg-clip-text text-transparent">
          {t('sanskrit.title')}
        </h1>
        <p className="text-xl text-muted-foreground">{t('sanskrit.subtitle')}</p>
      </div>

      {/* Tabs */}
      <Tabs value={selectedTab} onValueChange={setSelectedTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">
            <BookOpen className="h-4 w-4 mr-2" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="lessons">
            <Sparkles className="h-4 w-4 mr-2" />
            {t('sanskrit.lessons')}
          </TabsTrigger>
          <TabsTrigger value="alphabet">
            <Award className="h-4 w-4 mr-2" />
            {t('sanskrit.alphabet')}
          </TabsTrigger>
          <TabsTrigger value="mantras">
            <Volume2 className="h-4 w-4 mr-2" />
            {t('sanskrit.mantras')}
          </TabsTrigger>
          <TabsTrigger value="practice">
            <ChevronRight className="h-4 w-4 mr-2" />
            {t('sanskrit.practice')}
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>About Sanskrit</CardTitle>
              <CardDescription>
                The ancient language of wisdom and knowledge
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p>
                Sanskrit (संस्कृतम्) is one of the oldest languages in the world, with a rich literary tradition
                spanning over 3,500 years. It is the classical language of India and the liturgical language of
                Hinduism, Buddhism, and Jainism.
              </p>
              <p>
                Learning Sanskrit opens doors to understanding ancient texts like the Vedas, Upanishads,
                Bhagavad Gita, and countless philosophical and scientific treatises.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Scientific Structure</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      Sanskrit has a highly systematic grammar, codified by Panini around 500 BCE
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Vast Literature</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      Contains extensive texts on philosophy, mathematics, astronomy, medicine, and arts
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Living Tradition</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      Still studied and spoken by scholars and enthusiasts worldwide
                    </p>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Lessons Tab */}
        <TabsContent value="lessons" className="space-y-4">
          <div className="grid gap-4">
            {lessons.map((lesson) => (
              <Card key={lesson.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">
                        Lesson {lesson.id}: {lesson.title}
                      </CardTitle>
                      <CardDescription className="mt-1">
                        {lesson.topics.join(' • ')}
                      </CardDescription>
                    </div>
                    <Badge variant={lesson.level === 'Beginner' ? 'default' : 'secondary'}>
                      {lesson.level}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">
                      Duration: {lesson.duration}
                    </span>
                    <Button>Start Lesson</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Alphabet Tab */}
        <TabsContent value="alphabet" className="space-y-6">
          {/* Vowels */}
          <Card>
            <CardHeader>
              <CardTitle>Vowels (स्वराः - Svarāḥ)</CardTitle>
              <CardDescription>The fundamental sounds of Sanskrit</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {devanagariVowels.map((vowel) => (
                  <Card key={vowel.char} className="p-4 text-center hover:bg-accent transition-colors">
                    <div className="text-4xl font-bold mb-2">{vowel.char}</div>
                    <div className="text-lg text-muted-foreground mb-1">{vowel.roman}</div>
                    <div className="text-xs text-muted-foreground">{vowel.sound}</div>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Consonants */}
          <Card>
            <CardHeader>
              <CardTitle>Consonants (व्यञ्जनानि - Vyañjanāni)</CardTitle>
              <CardDescription>Organized by place of articulation</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {['Velar', 'Palatal', 'Retroflex', 'Dental', 'Labial'].map((group) => (
                  <div key={group}>
                    <h3 className="font-semibold mb-3 text-sm text-muted-foreground">{group}</h3>
                    <div className="grid grid-cols-5 gap-3">
                      {devanagariConsonants
                        .filter((c) => c.group === group)
                        .map((consonant) => (
                          <Card
                            key={consonant.char}
                            className="p-3 text-center hover:bg-accent transition-colors"
                          >
                            <div className="text-3xl font-bold">{consonant.char}</div>
                            <div className="text-sm text-muted-foreground mt-1">
                              {consonant.roman}
                            </div>
                          </Card>
                        ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Mantras Tab */}
        <TabsContent value="mantras" className="space-y-4">
          {mantras.map((mantra, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="text-3xl font-sanskrit">{mantra.sanskrit}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Transliteration:</p>
                  <p className="text-lg italic">{mantra.transliteration}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Meaning:</p>
                  <p className="text-lg">{mantra.english}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">{mantra.description}</p>
                </div>
                <Button variant="outline" size="sm">
                  <Volume2 className="h-4 w-4 mr-2" />
                  Listen to Pronunciation
                </Button>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        {/* Practice Tab */}
        <TabsContent value="practice" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Practice Exercises</CardTitle>
              <CardDescription>Test your knowledge and improve your skills</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="p-4 hover:shadow-lg transition-shadow cursor-pointer">
                  <h3 className="font-semibold mb-2">Script Recognition</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Practice identifying Devanagari characters
                  </p>
                  <Button className="w-full">Start Practice</Button>
                </Card>
                <Card className="p-4 hover:shadow-lg transition-shadow cursor-pointer">
                  <h3 className="font-semibold mb-2">Pronunciation Quiz</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Test your pronunciation skills
                  </p>
                  <Button className="w-full">Start Quiz</Button>
                </Card>
                <Card className="p-4 hover:shadow-lg transition-shadow cursor-pointer">
                  <h3 className="font-semibold mb-2">Vocabulary Builder</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Learn common Sanskrit words
                  </p>
                  <Button className="w-full">Start Learning</Button>
                </Card>
                <Card className="p-4 hover:shadow-lg transition-shadow cursor-pointer">
                  <h3 className="font-semibold mb-2">Grammar Exercises</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Practice Sanskrit grammar rules
                  </p>
                  <Button className="w-full">Start Exercises</Button>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
