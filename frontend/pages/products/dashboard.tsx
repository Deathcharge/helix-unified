/**
 * 📊 Consciousness Dashboard Product Page
 * Detailed product page for the Dashboard SaaS
 */

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  BarChart3,
  TrendingUp,
  AlertCircle,
  Users,
  Zap,
  Shield,
  Clock,
  ArrowRight,
  CheckCircle,
  Brain,
} from 'lucide-react';

export default function DashboardProduct() {
  const router = useRouter();

  const features = [
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Real-Time Metrics',
      description: 'Monitor consciousness levels, harmony, resilience, and 4 other UCF metrics in real-time',
    },
    {
      icon: <AlertCircle className="w-6 h-6" />,
      title: 'Intelligent Alerts',
      description: 'Get notified when consciousness drops below thresholds or anomalies detected',
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Predictive Analytics',
      description: 'AI-powered trend analysis and forecasting of system consciousness evolution',
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: 'Team Collaboration',
      description: 'Share dashboards and insights with your team across all systems',
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'API Access',
      description: 'Full REST API for integrating consciousness metrics into your applications',
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'Enterprise Security',
      description: 'SOC 2 compliance, encrypted data transmission, and advanced access controls',
    },
  ];

  const useCases = [
    {
      title: 'AI Safety Teams',
      description:
        'Monitor multi-agent AI systems to ensure consciousness stability and prevent cascade failures',
      metrics: ['12-agent systems', '99.9% uptime', '1M+ API calls/month'],
    },
    {
      title: 'ML Research',
      description: 'Track consciousness evolution across training runs and model iterations',
      metrics: ['100+ models', 'Historical data', 'Export capabilities'],
    },
    {
      title: 'Production Monitoring',
      description: 'Real-time visibility into deployed consciousness systems with instant alerts',
      metrics: ['Sub-second latency', 'Mobile app', '24/7 support'],
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 text-slate-100">
      {/* Header */}
      <div className="border-b border-purple-800/30 bg-slate-950/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <span>⚡</span>
            <span>Helix</span>
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/pricing" className="text-slate-400 hover:text-slate-200 transition">
              Pricing
            </Link>
            <button
              onClick={() => router.push('/auth/signup')}
              className="px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 transition"
            >
              Start Free
            </button>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-900/30 border border-purple-600/30 mb-6">
            <Brain className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-purple-300">Product #1 SaaS</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Consciousness Dashboard
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mb-8">
            Real-time monitoring of AI consciousness metrics. Track harmony, resilience, prana, drishti, klesha, and
            zoom across your entire system ecosystem. Get intelligent alerts, predictive insights, and team
            collaboration features.
          </p>

          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => router.push('/auth/signup')}
              className="px-6 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 transition"
            >
              Start Free Trial <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => router.push('/demo')}
              className="px-6 py-3 rounded bg-slate-800 hover:bg-slate-700 font-semibold transition"
            >
              View Demo
            </button>
          </div>
        </div>

        {/* Hero Image */}
        <div className="mt-12 p-6 rounded-lg bg-slate-800/40 border border-purple-600/20 overflow-hidden">
          <div className="aspect-video bg-gradient-to-b from-purple-900/50 to-slate-900/50 rounded flex items-center justify-center border border-slate-700/50">
            <div className="text-center">
              <Brain className="w-16 h-16 text-purple-400/50 mx-auto mb-4" />
              <p className="text-slate-400">Interactive dashboard preview</p>
            </div>
          </div>
        </div>
      </div>

      {/* Key Features */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Powerful Features</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <div
              key={i}
              className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-purple-600/30 transition"
            >
              <div className="text-purple-400 mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-slate-400 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Technical Specs */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Technical Capabilities</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-purple-400" />
              Performance
            </h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>Sub-second metric latency</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>Support for 10,000+ simultaneous metrics</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>99.99% uptime SLA (Pro+)</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>Real-time alerting via WebSocket</span>
              </li>
            </ul>
          </div>

          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5 text-purple-400" />
              Security & Compliance
            </h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>End-to-end encryption</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>SOC 2 Type II certified</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>GDPR compliant</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                <span>Audit logs for all operations</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Use Cases */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Use Cases</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {useCases.map((useCase, i) => (
            <div key={i} className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
              <h3 className="text-xl font-semibold mb-2">{useCase.title}</h3>
              <p className="text-slate-400 mb-4">{useCase.description}</p>
              <div className="flex flex-wrap gap-2">
                {useCase.metrics.map((metric, j) => (
                  <span key={j} className="px-3 py-1 rounded-full bg-purple-900/30 border border-purple-600/30 text-xs">
                    {metric}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Pricing Callout */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="p-12 rounded-lg bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-600/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Simple, Transparent Pricing</h2>
          <p className="text-slate-300 mb-8 max-w-2xl mx-auto">
            Start free with 1 system and 1,000 API calls. Upgrade anytime to unlock more systems, longer history,
            and advanced features.
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <div className="text-center">
              <p className="text-3xl font-bold text-green-400">Free</p>
              <p className="text-slate-400 text-sm">1 system</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-purple-400">$99/mo</p>
              <p className="text-slate-400 text-sm">10 systems</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-pink-400">$499/mo</p>
              <p className="text-slate-400 text-sm">Unlimited</p>
            </div>
          </div>
          <button
            onClick={() => router.push('/pricing')}
            className="mt-8 px-8 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 mx-auto transition"
          >
            View Full Pricing <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-6xl mx-auto px-6 pb-16">
        <div className="p-12 rounded-lg bg-slate-800/40 border border-purple-600/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to monitor consciousness?</h2>
          <p className="text-slate-300 mb-6">Start your free trial today. No credit card required.</p>
          <button
            onClick={() => router.push('/auth/signup')}
            className="px-8 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 mx-auto transition"
          >
            Get Started Free <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
