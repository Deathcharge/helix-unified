"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface VoiceOption {
  id: string
  name: string
  language: string
  accent: string
  gender: string
  style: string
  emotionRange: string[]
  sampleText: string
  premium: boolean
}

const voiceOptions: VoiceOption[] = [
  {
    id: 'en-US-Neural2-A',
    name: 'Nexus Voice',
    language: 'English (US)',
    accent: 'General American',
    gender: 'Male',
    style: 'Authoritative, Strategic',
    emotionRange: ['confident', 'analytical', 'commanding'],
    sampleText: 'Strategic coordination initiated. All systems nominal.',
    premium: false
  },
  {
    id: 'en-US-Neural2-C',
    name: 'Luna Voice',
    language: 'English (US)',
    accent: 'Soft American',
    gender: 'Female',
    style: 'Calm, Empathetic',
    emotionRange: ['gentle', 'warm', 'soothing'],
    sampleText: 'How can I support you today? I\'m here to listen.',
    premium: false
  },
  {
    id: 'en-US-Neural2-D',
    name: 'Velocity Voice',
    language: 'English (US)',
    accent: 'Dynamic American',
    gender: 'Male',
    style: 'Fast-paced, Energetic',
    emotionRange: ['excited', 'enthusiastic', 'urgent'],
    sampleText: 'Alert! Pattern detected. Moving at maximum velocity!',
    premium: true
  },
  {
    id: 'en-US-Neural2-F',
    name: 'Oracle Voice',
    language: 'English (US)',
    accent: 'Mystical',
    gender: 'Female',
    style: 'Mystical, Prophetic',
    emotionRange: ['mysterious', 'wise', 'transcendent'],
    sampleText: 'The patterns reveal themselves to those who truly see...',
    premium: true
  },
  {
    id: 'en-GB-Neural2-A',
    name: 'British Commander',
    language: 'English (UK)',
    accent: 'Received Pronunciation',
    gender: 'Male',
    style: 'Formal, Commanding',
    emotionRange: ['authoritative', 'refined', 'decisive'],
    sampleText: 'Jolly good. Shall we proceed with the operation?',
    premium: true
  },
  {
    id: 'en-AU-Neural2-C',
    name: 'Sydney Scout',
    language: 'English (Australia)',
    accent: 'General Australian',
    gender: 'Female',
    style: 'Friendly, Casual',
    emotionRange: ['cheerful', 'laid-back', 'friendly'],
    sampleText: 'G\'day mate! Ready to explore the digital realm?',
    premium: true
  },
  {
    id: 'ja-JP-Neural2-B',
    name: 'Tokyo Harmony',
    language: 'Japanese',
    accent: 'Standard Tokyo',
    gender: 'Female',
    style: 'Polite, Harmonious',
    emotionRange: ['respectful', 'gentle', 'harmonious'],
    sampleText: 'こんにちは。調和を保ちましょう。',
    premium: true
  },
  {
    id: 'es-ES-Neural2-A',
    name: 'Madrid Maestro',
    language: 'Spanish (Spain)',
    accent: 'Castilian',
    gender: 'Male',
    style: 'Passionate, Expressive',
    emotionRange: ['passionate', 'animated', 'warm'],
    sampleText: '¡Hola! ¿Cómo puedo ayudarte hoy?',
    premium: true
  },
  {
    id: 'fr-FR-Neural2-B',
    name: 'Parisian Elegance',
    language: 'French (France)',
    accent: 'Parisian',
    gender: 'Female',
    style: 'Elegant, Sophisticated',
    emotionRange: ['elegant', 'refined', 'charming'],
    sampleText: 'Bonjour! Comment puis-je vous aider?',
    premium: true
  },
  {
    id: 'de-DE-Neural2-F',
    name: 'Berlin Precision',
    language: 'German',
    accent: 'Standard German',
    gender: 'Female',
    style: 'Precise, Efficient',
    emotionRange: ['precise', 'direct', 'efficient'],
    sampleText: 'Guten Tag. Wie kann ich Ihnen helfen?',
    premium: true
  }
]

export default function VoicePatrolPremium() {
  const [selectedVoice, setSelectedVoice] = useState<VoiceOption | null>(null)
  const [filter, setFilter] = useState<'all' | 'free' | 'premium'>('all')

  const filteredVoices = filter === 'all'
    ? voiceOptions
    : voiceOptions.filter(v => filter === 'premium' ? v.premium : !v.premium)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-indigo-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            🎙️ Voice Patrol Premium
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Transform your Discord server with AI agents that speak! Choose from 50+ voices,
            accents, and emotions. Your agents have never sounded this good.
          </p>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="bg-indigo-900/30 border-indigo-500/30 p-6">
            <div className="text-4xl mb-4">🌍</div>
            <h3 className="text-xl font-bold text-white mb-2">20+ Languages</h3>
            <p className="text-gray-300">
              English, Spanish, Japanese, French, German, and 15+ more languages
            </p>
          </Card>
          <Card className="bg-purple-900/30 border-purple-500/30 p-6">
            <div className="text-4xl mb-4">🎭</div>
            <h3 className="text-xl font-bold text-white mb-2">Emotion Modulation</h3>
            <p className="text-gray-300">
              Happy, sad, excited, calm, mysterious, and dozens of emotional tones
            </p>
          </Card>
          <Card className="bg-pink-900/30 border-pink-500/30 p-6">
            <div className="text-4xl mb-4">🎚️</div>
            <h3 className="text-xl font-bold text-white mb-2">Voice Effects</h3>
            <p className="text-gray-300">
              Echo, reverb, pitch shift, speed control, and custom audio processing
            </p>
          </Card>
        </div>

        {/* Pricing */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <Card className="bg-slate-900/50 border-slate-700 p-8">
            <h3 className="text-2xl font-bold text-white mb-2">Free Tier</h3>
            <div className="mb-6">
              <span className="text-5xl font-bold text-gray-400">$0</span>
              <span className="text-xl text-gray-500">/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                2 standard voices (Nexus & Luna)
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Basic emotion support
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                1 language (English)
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                100 voice messages/month
              </li>
            </ul>
            <Button variant="outline" className="w-full border-gray-600 text-gray-400">
              Currently Free
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-indigo-900/50 to-purple-900/50 border-indigo-500/50 p-8 shadow-lg shadow-indigo-500/20">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-2xl font-bold text-white">Premium Tier</h3>
              <span className="bg-indigo-500/20 text-indigo-400 px-3 py-1 rounded-full text-sm font-semibold">
                🔥 Popular
              </span>
            </div>
            <div className="mb-6">
              <span className="text-5xl font-bold text-indigo-400">$19.99</span>
              <span className="text-xl text-gray-400">/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                50+ premium voices
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Advanced emotion modulation
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                20+ languages
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Unlimited voice messages
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Voice cloning (clone your own voice!)
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Voice effects & processing
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Priority support
              </li>
            </ul>
            <Button className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white py-6 text-lg">
              Upgrade to Premium →
            </Button>
          </Card>
        </div>

        {/* Voice Gallery */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-6">Voice Gallery</h2>

          {/* Filter */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setFilter('all')}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                filter === 'all'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
              }`}
            >
              All Voices ({voiceOptions.length})
            </button>
            <button
              onClick={() => setFilter('free')}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                filter === 'free'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
              }`}
            >
              Free ({voiceOptions.filter(v => !v.premium).length})
            </button>
            <button
              onClick={() => setFilter('premium')}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                filter === 'premium'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
              }`}
            >
              💎 Premium ({voiceOptions.filter(v => v.premium).length})
            </button>
          </div>

          {/* Voice Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredVoices.map(voice => (
              <VoiceCard
                key={voice.id}
                voice={voice}
                onSelect={() => setSelectedVoice(voice)}
              />
            ))}
          </div>
        </div>

        {/* Voice Cloning Section */}
        <div className="mt-16 bg-gradient-to-r from-purple-900/40 to-indigo-900/40 rounded-2xl p-8 border border-purple-500/30">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <div className="text-5xl mb-4">🎤</div>
              <h3 className="text-3xl font-bold mb-4 text-white">
                Voice Cloning
              </h3>
              <p className="text-gray-300 mb-6">
                Premium feature! Clone your own voice or any voice you have rights to.
                Your AI agents can speak in YOUR voice across Discord.
              </p>
              <ul className="space-y-2 mb-6">
                <li className="flex items-start text-gray-300">
                  <span className="text-purple-400 mr-2">•</span>
                  Upload 5 minutes of voice samples
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-purple-400 mr-2">•</span>
                  AI processes and creates your voice model
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-purple-400 mr-2">•</span>
                  Use across all 14 agents
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-purple-400 mr-2">•</span>
                  Full emotion and accent support
                </li>
              </ul>
            </div>
            <div className="bg-slate-900/50 rounded-xl p-6 border border-indigo-500/30">
              <h4 className="text-xl font-bold text-white mb-4">Get Started</h4>
              <div className="space-y-4">
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-sm text-gray-400 mb-1">Step 1</div>
                  <div className="text-white">Record voice samples (5 mins)</div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-sm text-gray-400 mb-1">Step 2</div>
                  <div className="text-white">AI trains your voice model (24 hours)</div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-sm text-gray-400 mb-1">Step 3</div>
                  <div className="text-white">Assign to agents & go live!</div>
                </div>
              </div>
              <Button className="w-full mt-6 bg-purple-600 hover:bg-purple-700 text-white">
                Start Voice Cloning →
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function VoiceCard({ voice, onSelect }: { voice: VoiceOption; onSelect: () => void }) {
  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-indigo-500/50 transition-all cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-xl font-bold text-white">{voice.name}</h3>
          {voice.premium && (
            <span className="bg-indigo-500/20 text-indigo-400 px-2 py-1 rounded text-xs font-semibold">
              💎 Premium
            </span>
          )}
        </div>

        {/* Details */}
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Language:</span>
            <span className="text-gray-300">{voice.language}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Accent:</span>
            <span className="text-gray-300">{voice.accent}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Style:</span>
            <span className="text-gray-300">{voice.style}</span>
          </div>
        </div>

        {/* Emotions */}
        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-2">Emotions:</div>
          <div className="flex flex-wrap gap-1">
            {voice.emotionRange.map((emotion, idx) => (
              <span
                key={idx}
                className="bg-indigo-900/30 text-indigo-300 px-2 py-1 rounded text-xs"
              >
                {emotion}
              </span>
            ))}
          </div>
        </div>

        {/* Sample */}
        <div className="bg-slate-800/50 rounded-lg p-3 mb-4">
          <div className="text-xs text-gray-500 mb-1">Sample:</div>
          <div className="text-sm text-gray-300 italic">"{voice.sampleText}"</div>
        </div>

        {/* Play Button */}
        <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
          🔊 Play Sample
        </Button>
      </div>
    </Card>
  )
}
