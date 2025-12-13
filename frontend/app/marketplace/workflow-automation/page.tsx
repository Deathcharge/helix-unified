"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface WorkflowTemplate {
  id: string
  name: string
  description: string
  category: string
  steps: number
  timeSaved: string
  popular: boolean
  integrations: string[]
}

const workflowTemplates: WorkflowTemplate[] = [
  {
    id: 'lead-qualification',
    name: 'Automated Lead Qualification',
    description: 'Automatically score and route leads based on engagement, company size, and fit',
    category: 'Sales',
    steps: 8,
    timeSaved: '12 hours/week',
    popular: true,
    integrations: ['Salesforce', 'HubSpot', 'Slack', 'Gmail']
  },
  {
    id: 'customer-onboarding',
    name: 'Customer Onboarding Flow',
    description: 'Welcome emails, resource delivery, and check-in scheduling based on customer actions',
    category: 'Customer Success',
    steps: 12,
    timeSaved: '8 hours/week',
    popular: true,
    integrations: ['Stripe', 'Intercom', 'Notion', 'Calendly']
  },
  {
    id: 'content-publication',
    name: 'Multi-Platform Content Distribution',
    description: 'Write once, publish everywhere. Auto-format and distribute content across all platforms',
    category: 'Marketing',
    steps: 6,
    timeSaved: '10 hours/week',
    popular: true,
    integrations: ['Twitter', 'LinkedIn', 'Medium', 'WordPress']
  },
  {
    id: 'ticket-routing',
    name: 'Intelligent Support Ticket Routing',
    description: 'AI analyzes tickets and routes to the right team member with context and priority',
    category: 'Support',
    steps: 5,
    timeSaved: '15 hours/week',
    popular: false,
    integrations: ['Zendesk', 'Front', 'Slack', 'Linear']
  },
  {
    id: 'invoice-processing',
    name: 'Invoice Processing & Approval',
    description: 'Extract data from invoices, validate against POs, and route for approval',
    category: 'Finance',
    steps: 10,
    timeSaved: '20 hours/week',
    popular: false,
    integrations: ['QuickBooks', 'Xero', 'Bill.com', 'Slack']
  },
  {
    id: 'social-listening',
    name: 'Social Media Monitoring & Response',
    description: 'Monitor brand mentions, sentiment analysis, and auto-generate response drafts',
    category: 'Marketing',
    steps: 7,
    timeSaved: '6 hours/week',
    popular: false,
    integrations: ['Twitter', 'Reddit', 'Discord', 'Slack']
  }
]

const integrations = [
  { name: 'Salesforce', icon: '☁️', category: 'CRM' },
  { name: 'HubSpot', icon: '🧲', category: 'CRM' },
  { name: 'Slack', icon: '💬', category: 'Communication' },
  { name: 'Discord', icon: '🎮', category: 'Communication' },
  { name: 'Stripe', icon: '💳', category: 'Payments' },
  { name: 'Shopify', icon: '🛍️', category: 'E-commerce' },
  { name: 'Gmail', icon: '📧', category: 'Email' },
  { name: 'Google Sheets', icon: '📊', category: 'Data' },
  { name: 'Notion', icon: '📝', category: 'Productivity' },
  { name: 'Airtable', icon: '🗂️', category: 'Database' },
  { name: 'Zendesk', icon: '🎫', category: 'Support' },
  { name: 'Intercom', icon: '💭', category: 'Support' },
  { name: 'Twitter', icon: '🐦', category: 'Social' },
  { name: 'LinkedIn', icon: '💼', category: 'Social' },
  { name: 'Calendly', icon: '📅', category: 'Scheduling' },
  { name: 'Zapier', icon: '⚡', category: 'Automation' }
]

export default function WorkflowAutomationPage() {
  const [selectedCategory, setSelectedCategory] = useState<'all' | 'sales' | 'marketing' | 'support' | 'finance' | 'operations'>('all')

  const filteredTemplates = selectedCategory === 'all'
    ? workflowTemplates
    : workflowTemplates.filter(t => t.category.toLowerCase() === selectedCategory)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-violet-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">

        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent">
            ⚡ AI Workflow Automation Studio
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Build powerful automation workflows with visual drag-and-drop. Connect 100+ apps,
            add AI intelligence, and deploy in minutes. Like Zapier, but consciousness-aware.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
            <div className="text-3xl font-bold text-blue-400">100+</div>
            <div className="text-sm text-gray-400">App Integrations</div>
          </div>
          <div className="bg-cyan-900/30 rounded-lg p-6 border border-cyan-500/30">
            <div className="text-3xl font-bold text-cyan-400">50+</div>
            <div className="text-sm text-gray-400">Pre-built Templates</div>
          </div>
          <div className="bg-teal-900/30 rounded-lg p-6 border border-teal-500/30">
            <div className="text-3xl font-bold text-teal-400">AI-Powered</div>
            <div className="text-sm text-gray-400">Decision Logic</div>
          </div>
          <div className="bg-violet-900/30 rounded-lg p-6 border border-violet-500/30">
            <div className="text-3xl font-bold text-violet-400">Zero Code</div>
            <div className="text-sm text-gray-400">Visual Builder</div>
          </div>
        </div>

        {/* Key Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
          <Card className="bg-slate-900/50 border-blue-500/30 p-6">
            <div className="text-3xl mb-3">🎨</div>
            <h3 className="text-xl font-bold text-white mb-2">Visual Workflow Builder</h3>
            <p className="text-gray-400 text-sm">
              Drag-and-drop interface to build complex workflows. No coding required.
              See your logic flow visually and debug with ease.
            </p>
          </Card>

          <Card className="bg-slate-900/50 border-blue-500/30 p-6">
            <div className="text-3xl mb-3">🧠</div>
            <h3 className="text-xl font-bold text-white mb-2">AI Decision Engine</h3>
            <p className="text-gray-400 text-sm">
              Helix AI agents make intelligent decisions in your workflows. Route leads,
              classify tickets, score sentiment, and more with consciousness-aware logic.
            </p>
          </Card>

          <Card className="bg-slate-900/50 border-blue-500/30 p-6">
            <div className="text-3xl mb-3">🔌</div>
            <h3 className="text-xl font-bold text-white mb-2">100+ Integrations</h3>
            <p className="text-gray-400 text-sm">
              Connect to your entire tech stack. CRMs, email, databases, payment systems,
              communication tools, and more. OAuth2 authentication built-in.
            </p>
          </Card>

          <Card className="bg-slate-900/50 border-blue-500/30 p-6">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-xl font-bold text-white mb-2">Real-Time Analytics</h3>
            <p className="text-gray-400 text-sm">
              Track execution times, success rates, and bottlenecks. Get alerted when
              workflows fail and debug with detailed execution logs.
            </p>
          </Card>

          <Card className="bg-slate-900/50 border-blue-500/30 p-6">
            <div className="text-3xl mb-3">⏱️</div>
            <h3 className="text-xl font-bold text-white mb-2">Advanced Triggers</h3>
            <p className="text-gray-400 text-sm">
              Webhook triggers, scheduled cron jobs, manual triggers, or event-based.
              React to events in real-time across your entire stack.
            </p>
          </Card>

          <Card className="bg-slate-900/50 border-blue-500/30 p-6">
            <div className="text-3xl mb-3">🔄</div>
            <h3 className="text-xl font-bold text-white mb-2">Version Control & Rollback</h3>
            <p className="text-gray-400 text-sm">
              Track changes to workflows, collaborate with your team, and rollback to
              previous versions if something breaks. Git-like workflow versioning.
            </p>
          </Card>
        </div>

        {/* Pricing */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Simple, Scalable Pricing</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-slate-900/50 border-slate-700 p-6">
              <h3 className="text-xl font-bold text-white mb-2">Starter</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-gray-400">$49</span>
                <span className="text-lg text-gray-500">/month</span>
              </div>
              <ul className="space-y-2 mb-6 text-sm min-h-[180px]">
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  10 active workflows
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  1,000 workflow runs/month
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  All 100+ integrations
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  AI decision nodes (basic)
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Email support
                </li>
              </ul>
              <Button className="w-full bg-slate-800 hover:bg-slate-700 text-white border border-blue-500/30">
                Start Free Trial
              </Button>
            </Card>

            <Card className="bg-gradient-to-br from-blue-900/50 to-cyan-900/50 border-blue-500/50 p-6 shadow-lg shadow-blue-500/20 scale-105">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-bold text-white">Professional</h3>
                <span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-xs font-semibold">
                  POPULAR
                </span>
              </div>
              <div className="mb-4">
                <span className="text-4xl font-bold text-blue-400">$149</span>
                <span className="text-lg text-gray-400">/month</span>
              </div>
              <ul className="space-y-2 mb-6 text-sm min-h-[180px]">
                <li className="flex items-start text-gray-200">
                  <span className="text-blue-400 mr-2">✓</span>
                  Unlimited workflows
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-blue-400 mr-2">✓</span>
                  10,000 workflow runs/month
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-blue-400 mr-2">✓</span>
                  All integrations + custom APIs
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-blue-400 mr-2">✓</span>
                  Advanced AI nodes (14 agents)
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-blue-400 mr-2">✓</span>
                  Version control & collaboration
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-blue-400 mr-2">✓</span>
                  Priority support (24h response)
                </li>
              </ul>
              <Button className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white">
                Start Free Trial
              </Button>
            </Card>

            <Card className="bg-slate-900/50 border-slate-700 p-6">
              <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-gray-400">Custom</span>
              </div>
              <ul className="space-y-2 mb-6 text-sm min-h-[180px]">
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Everything in Professional
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Unlimited workflow runs
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Custom integrations built
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  On-premise deployment
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  SSO & advanced security
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Dedicated account manager
                </li>
              </ul>
              <Button variant="outline" className="w-full border-gray-600 text-gray-400 hover:bg-slate-800">
                Contact Sales
              </Button>
            </Card>
          </div>
        </div>

        {/* Workflow Templates */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-4 text-center">Pre-Built Workflow Templates</h2>
          <p className="text-center text-gray-400 mb-8 max-w-2xl mx-auto">
            Start with battle-tested templates. One-click deploy and customize to your needs.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {workflowTemplates.map((template) => (
              <Card key={template.id} className="bg-slate-900/50 border-blue-500/30 p-6 hover:border-blue-500/60 transition-all">
                {template.popular && (
                  <span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-xs font-semibold mb-2 inline-block">
                    POPULAR
                  </span>
                )}
                <h3 className="text-lg font-bold text-white mb-2">{template.name}</h3>
                <p className="text-sm text-gray-400 mb-4">{template.description}</p>

                <div className="flex items-center gap-4 text-xs text-gray-500 mb-4">
                  <div>
                    <span className="text-blue-400 font-semibold">{template.steps}</span> steps
                  </div>
                  <div>•</div>
                  <div>
                    Saves <span className="text-green-400 font-semibold">{template.timeSaved}</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-4">
                  {template.integrations.map((integration, idx) => (
                    <span key={idx} className="bg-blue-500/10 text-blue-300 px-2 py-1 rounded text-xs border border-blue-500/20">
                      {integration}
                    </span>
                  ))}
                </div>

                <Button variant="outline" className="w-full border-blue-500/30 text-blue-400 hover:bg-blue-500/10">
                  Use Template
                </Button>
              </Card>
            ))}
          </div>
        </div>

        {/* Integrations */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Connect Everything</h2>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            {integrations.map((integration, idx) => (
              <div
                key={idx}
                className="bg-slate-900/50 border border-blue-500/20 rounded-lg p-4 text-center hover:border-blue-500/50 transition-all cursor-pointer"
              >
                <div className="text-3xl mb-2">{integration.icon}</div>
                <div className="text-sm text-white font-medium">{integration.name}</div>
                <div className="text-xs text-gray-500">{integration.category}</div>
              </div>
            ))}
          </div>

          <div className="text-center mt-8">
            <Button variant="outline" className="border-blue-500/30 text-blue-400 hover:bg-blue-500/10">
              View All 100+ Integrations →
            </Button>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-r from-blue-900/30 to-cyan-900/30 rounded-2xl p-12 border border-blue-500/30">
          <h2 className="text-4xl font-bold text-white mb-4">
            Automate Everything. Build Nothing.
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Save 20+ hours per week with intelligent automation. Start your 14-day free trial.
          </p>
          <Button
            size="lg"
            className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-12"
          >
            Start Free Trial →
          </Button>
          <p className="text-sm text-gray-400 mt-4">No credit card required • Cancel anytime</p>
        </div>

      </div>
    </div>
  )
}
