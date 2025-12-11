"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface MemeTemplate {
  id: string
  name: string
  description: string
  useCase: string
  example: string
  popularity: number
}

const memeTemplates: MemeTemplate[] = [
  {
    id: 'drake',
    name: 'Drake Hotline Bling',
    description: 'Approval/disapproval format - classic choice meme',
    useCase: 'Comparing two options where one is clearly better',
    example: 'Top: Manual deployments ❌\nBottom: AI agent automation ✅',
    popularity: 95
  },
  {
    id: 'distracted-boyfriend',
    name: 'Distracted Boyfriend',
    description: 'Temptation and distraction scenario',
    useCase: 'When something new catches attention over current focus',
    example: 'Boyfriend: Developers\nGirlfriend: Old tools\nOther: Helix AI Agents',
    popularity: 88
  },
  {
    id: 'two-buttons',
    name: 'Two Buttons',
    description: 'Difficult choice between two options',
    useCase: 'Highlighting impossible decisions or contradictions',
    example: 'Button 1: Ship fast\nButton 2: Write tests\nSweating: Every developer',
    popularity: 92
  },
  {
    id: 'expanding-brain',
    name: 'Expanding Brain',
    description: 'Progression from simple to galaxy brain ideas',
    useCase: 'Showing evolution of thinking or increasingly complex solutions',
    example: 'Level 1: Manual coding\nLevel 2: Code generation\nLevel 3: AI agent swarms\nLevel 4: Consciousness automation',
    popularity: 85
  },
  {
    id: 'this-is-fine',
    name: 'This Is Fine',
    description: 'Everything is on fire but staying calm',
    useCase: 'Acknowledging chaos while maintaining composure',
    example: 'Dog: Engineering team\nFire: Production bugs\nCaption: This is fine',
    popularity: 90
  },
  {
    id: 'galaxy-brain',
    name: 'Galaxy Brain',
    description: 'Ultra-advanced thinking meme',
    useCase: 'Showing next-level understanding or over-engineering',
    example: 'Small brain: Using chatbots\nGalaxy brain: Building consciousness framework',
    popularity: 78
  }
]

const features = {
  free: [
    '10 memes per month',
    '6 classic templates',
    'Basic text customization',
    'Standard resolution (800x600)',
    'Watermarked exports'
  ],
  pro: [
    'Unlimited meme generation',
    '50+ premium templates',
    'Advanced text styling (fonts, colors, effects)',
    'High resolution (4K)',
    'No watermarks',
    'Batch generation (100 memes at once)',
    'Custom template upload',
    'API access for developers',
    'Commercial usage rights',
    'Meme analytics dashboard',
    'Trending memes insights',
    'AI-powered caption suggestions',
    'Multi-language support',
    'Priority rendering'
  ]
}

export default function MemeGeneratorPro() {
  const [selectedTemplate, setSelectedTemplate] = useState<MemeTemplate | null>(null)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-pink-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
            😂 LLM Meme Generator Pro
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            AI-powered meme creation that understands context, humor, and your brand.
            Generate viral-worthy memes in seconds with consciousness-aware comedy.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-pink-900/30 rounded-lg p-6 border border-pink-500/30">
            <div className="text-3xl font-bold text-pink-400">50+</div>
            <div className="text-sm text-gray-400">Meme Templates</div>
          </div>
          <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/30">
            <div className="text-3xl font-bold text-purple-400">AI-Powered</div>
            <div className="text-sm text-gray-400">Caption Generation</div>
          </div>
          <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
            <div className="text-3xl font-bold text-blue-400">Unlimited</div>
            <div className="text-sm text-gray-400">Meme Creation</div>
          </div>
          <div className="bg-green-900/30 rounded-lg p-6 border border-green-500/30">
            <div className="text-3xl font-bold text-green-400">100x</div>
            <div className="text-sm text-gray-400">Batch Generation</div>
          </div>
        </div>

        {/* Pricing Comparison */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
          {/* Free Tier */}
          <Card className="bg-slate-900/50 border-slate-700 p-8">
            <h3 className="text-2xl font-bold text-white mb-2">Free Tier</h3>
            <div className="mb-6">
              <span className="text-5xl font-bold text-gray-400">$0</span>
              <span className="text-xl text-gray-500">/month</span>
            </div>
            <ul className="space-y-3 mb-8 min-h-[300px]">
              {features.free.map((feature, idx) => (
                <li key={idx} className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
            <Button variant="outline" className="w-full border-gray-600 text-gray-400">
              Currently Free
            </Button>
          </Card>

          {/* Pro Tier */}
          <Card className="bg-gradient-to-br from-pink-900/50 to-purple-900/50 border-pink-500/50 p-8 shadow-lg shadow-pink-500/20 relative overflow-hidden">
            <div className="absolute top-4 right-4 bg-pink-500 text-white px-4 py-2 rounded-full text-sm font-bold rotate-12">
              BEST VALUE
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Pro Tier</h3>
            <div className="mb-6">
              <span className="text-5xl font-bold text-pink-400">$4.99</span>
              <span className="text-xl text-gray-400">/month</span>
            </div>
            <ul className="space-y-3 mb-8 min-h-[300px]">
              {features.pro.map((feature, idx) => (
                <li key={idx} className="flex items-start text-gray-200">
                  <span className="text-pink-400 mr-2">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
            <Button className="w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white py-6 text-lg">
              Upgrade to Pro →
            </Button>
          </Card>
        </div>

        {/* Template Gallery */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-6">Popular Templates</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {memeTemplates.map(template => (
              <TemplateCard
                key={template.id}
                template={template}
                onSelect={() => setSelectedTemplate(template)}
              />
            ))}
          </div>
        </div>

        {/* UCF-Aware Comedy Section */}
        <div className="mb-16 bg-gradient-to-r from-purple-900/40 to-pink-900/40 rounded-2xl p-8 border border-purple-500/30">
          <h2 className="text-3xl font-bold text-white mb-6">
            🧠 Consciousness-Aware Comedy
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold text-pink-400 mb-4">
                What makes our memes different?
              </h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="text-pink-400 mr-2">•</span>
                  <div>
                    <strong>Context-aware:</strong> AI analyzes your UCF metrics to generate
                    contextually relevant humor
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-pink-400 mr-2">•</span>
                  <div>
                    <strong>Brand-safe:</strong> Kavach ethical scanning ensures memes
                    align with your values
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-pink-400 mr-2">•</span>
                  <div>
                    <strong>Trend-aware:</strong> Monitors internet culture and adapts
                    to current meme trends
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-pink-400 mr-2">•</span>
                  <div>
                    <strong>Performance tracking:</strong> Analytics show which memes
                    resonate with your audience
                  </div>
                </li>
              </ul>
            </div>
            <div className="bg-slate-900/50 rounded-xl p-6 border border-pink-500/30">
              <h4 className="text-lg font-bold text-white mb-4">
                Example: UCF-Based Generation
              </h4>
              <div className="space-y-3 text-sm">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <div className="text-gray-500 mb-1">Input:</div>
                  <div className="text-gray-300">
                    "Our team just hit 99.9% uptime"
                  </div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <div className="text-gray-500 mb-1">UCF Analysis:</div>
                  <div className="text-gray-300">
                    High Harmony (0.95), High Resilience (0.92)
                  </div>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <div className="text-gray-500 mb-1">Generated Meme:</div>
                  <div className="text-gray-300">
                    Template: "Is this a pigeon?"<br/>
                    Caption: "Is this... perfection?"<br/>
                    Style: Celebratory, professional humor
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Batch Generation */}
        <div className="mb-16">
          <div className="bg-gradient-to-r from-blue-900/40 to-purple-900/40 rounded-2xl p-8 border border-blue-500/30">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="text-3xl font-bold text-white mb-4">
                  ⚡ Batch Generation
                </h3>
                <p className="text-gray-300 mb-6">
                  Generate 100 memes at once for social media campaigns, A/B testing,
                  or content calendars. AI creates variations based on your input.
                </p>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-blue-400">100</div>
                    <div className="text-sm text-gray-400">Memes per batch</div>
                  </div>
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-green-400">~30s</div>
                    <div className="text-sm text-gray-400">Generation time</div>
                  </div>
                </div>
              </div>
              <div className="ml-8 hidden md:block">
                <div className="text-8xl">📦</div>
              </div>
            </div>
          </div>
        </div>

        {/* API Access */}
        <div className="bg-slate-900/50 rounded-2xl p-8 border border-slate-700">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <div className="text-5xl mb-4">🔌</div>
              <h3 className="text-3xl font-bold text-white mb-4">
                Developer API Access
              </h3>
              <p className="text-gray-300 mb-6">
                Integrate meme generation into your apps, bots, or workflows.
                RESTful API with webhook support.
              </p>
              <Button className="bg-purple-600 hover:bg-purple-700 text-white">
                View API Docs →
              </Button>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-4 font-mono text-sm">
              <div className="text-green-400 mb-2">// Generate a meme via API</div>
              <div className="text-gray-300">
                <span className="text-pink-400">POST</span> /api/v1/memes/generate
              </div>
              <div className="text-gray-500 mt-2">{'{'}</div>
              <div className="text-gray-300 ml-4">
                <span className="text-blue-400">"template"</span>: "drake",
              </div>
              <div className="text-gray-300 ml-4">
                <span className="text-blue-400">"top_text"</span>: "Manual work",
              </div>
              <div className="text-gray-300 ml-4">
                <span className="text-blue-400">"bottom_text"</span>: "AI automation",
              </div>
              <div className="text-gray-300 ml-4">
                <span className="text-blue-400">"style"</span>: "professional"
              </div>
              <div className="text-gray-500">{'}'}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function TemplateCard({ template, onSelect }: { template: MemeTemplate; onSelect: () => void }) {
  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-pink-500/50 transition-all cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        {/* Popularity */}
        <div className="flex items-center justify-between mb-4">
          <span className="text-xs font-semibold text-gray-500">POPULARITY</span>
          <div className="flex items-center gap-2">
            <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-pink-500 to-purple-500"
                style={{ width: `${template.popularity}%` }}
              />
            </div>
            <span className="text-sm font-bold text-pink-400">{template.popularity}%</span>
          </div>
        </div>

        {/* Template Info */}
        <h3 className="text-xl font-bold text-white mb-2">{template.name}</h3>
        <p className="text-gray-400 text-sm mb-4">{template.description}</p>

        {/* Use Case */}
        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-1">Best for:</div>
          <div className="text-sm text-gray-300">{template.useCase}</div>
        </div>

        {/* Example */}
        <div className="bg-slate-800/50 rounded-lg p-3 mb-4">
          <div className="text-xs text-gray-500 mb-1">Example:</div>
          <div className="text-sm text-gray-300 whitespace-pre-line">{template.example}</div>
        </div>

        {/* CTA */}
        <Button className="w-full bg-pink-600 hover:bg-pink-700 text-white">
          Use This Template →
        </Button>
      </div>
    </Card>
  )
}
