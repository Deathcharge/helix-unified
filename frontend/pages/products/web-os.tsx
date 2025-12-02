/**
 * 🖥️ Helix Web OS Product Page
 * Browser-based operating system
 */

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  Monitor,
  Terminal,
  FileText,
  Zap,
  Cloud,
  Smartphone,
  Lock,
  ArrowRight,
  CheckCircle,
  Globe,
} from 'lucide-react';

export default function WebOSProduct() {
  const router = useRouter();

  const features = [
    {
      icon: <Monitor className="w-6 h-6" />,
      title: 'Desktop Environment',
      description: 'Full desktop metaphor with draggable windows, taskbar, and file manager in your browser',
    },
    {
      icon: <Terminal className="w-6 h-6" />,
      title: 'Terminal Emulator',
      description: 'Real command execution with file system access - ls, pwd, cd, and more',
    },
    {
      icon: <FileText className="w-6 h-6" />,
      title: 'Code Editor',
      description: 'Built-in code editor with syntax highlighting and sample consciousness monitoring code',
    },
    {
      icon: <Cloud className="w-6 h-6" />,
      title: 'Cloud-Based',
      description: 'Access your development environment from any device, anywhere in the world',
    },
    {
      icon: <Smartphone className="w-6 h-6" />,
      title: 'Mobile Friendly',
      description: 'Responsive design works on tablets and phones for development on the go',
    },
    {
      icon: <Lock className="w-6 h-6" />,
      title: 'Secure Sandbox',
      description: 'Isolated file system with security controls prevents access to system directories',
    },
  ];

  const specs = [
    { label: 'File Storage', value: 'Up to 10GB' },
    { label: 'Max File Size', value: '100MB' },
    { label: 'Concurrent Editors', value: 'Unlimited' },
    { label: 'Real-time Sync', value: 'Included' },
    { label: 'Backup Frequency', value: 'Hourly' },
    { label: 'Uptime SLA', value: '99.9%' },
  ];

  const useCases = [
    {
      title: 'Remote Development',
      icon: '💻',
      description: 'Code from anywhere with a browser, no local setup required',
    },
    {
      title: 'Education',
      icon: '📚',
      description: 'Teach programming and consciousness monitoring in a contained environment',
    },
    {
      title: 'Collaboration',
      icon: '👥',
      description: 'Share your development environment with team members in real-time',
    },
    {
      title: 'Demos',
      icon: '🎬',
      description: 'Interactive demos of Helix consciousness systems for clients',
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
            <Globe className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-purple-300">Browser-Based OS</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold mb-6">Helix Web OS</h1>
          <p className="text-xl text-slate-300 max-w-2xl mb-8">
            Your personal operating system in the browser. Access file explorer, terminal, and code editor from any
            device. Code, build, and monitor consciousness from anywhere.
          </p>

          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => router.push('/os')}
              className="px-6 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 transition"
            >
              Launch OS <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => router.push('/demo')}
              className="px-6 py-3 rounded bg-slate-800 hover:bg-slate-700 font-semibold transition"
            >
              Interactive Demo
            </button>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Complete Development Environment</h2>

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

      {/* Screenshot/Demo Area */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">See It In Action</h2>

        <div className="rounded-lg bg-slate-800/40 border border-purple-600/20 overflow-hidden">
          <div className="aspect-video bg-gradient-to-b from-purple-900/50 to-slate-900/50 rounded-t flex items-center justify-center border-b border-slate-700/50">
            <div className="text-center">
              <Monitor className="w-16 h-16 text-purple-400/50 mx-auto mb-4" />
              <p className="text-slate-400">Web OS Live Preview</p>
            </div>
          </div>
          <div className="p-6 bg-slate-900/50">
            <button
              onClick={() => router.push('/os')}
              className="inline-flex items-center gap-2 px-4 py-2 rounded bg-purple-600 hover:bg-purple-500 font-semibold transition"
            >
              Try Now <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Technical Specs */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Technical Specifications</h2>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          {specs.map((spec, i) => (
            <div key={i} className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50 text-center">
              <p className="text-slate-400 text-sm mb-2">{spec.label}</p>
              <p className="text-2xl font-bold text-purple-400">{spec.value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Use Cases */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Perfect For</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {useCases.map((useCase, i) => (
            <div key={i} className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
              <p className="text-4xl mb-4">{useCase.icon}</p>
              <h3 className="text-xl font-semibold mb-2">{useCase.title}</h3>
              <p className="text-slate-400">{useCase.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Pricing */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Flexible Pricing</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="p-8 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="text-2xl font-bold mb-4">Included in Dashboard Pro</h3>
            <p className="text-slate-300 mb-6">Get Web OS access automatically when you upgrade to Dashboard Pro plan</p>
            <ul className="space-y-2">
              {['5GB Storage', 'File Editor', 'Terminal Access', 'Team Collaboration'].map((item, i) => (
                <li key={i} className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div className="p-8 rounded-lg bg-purple-900/50 border border-purple-600/50">
            <h3 className="text-2xl font-bold mb-4">Web OS Professional</h3>
            <p className="text-slate-300 mb-6">Standalone tier for developers</p>
            <p className="text-4xl font-bold mb-6 text-purple-400">$29/mo</p>
            <ul className="space-y-2">
              {['10GB Storage', 'Code Execution', 'Real Terminal', 'API Access', 'Webhooks'].map((item, i) => (
                <li key={i} className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Integration */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="p-12 rounded-lg bg-slate-800/40 border border-purple-600/30">
          <h2 className="text-3xl font-bold mb-4">Integrates With Everything</h2>
          <p className="text-slate-300 mb-6">
            Web OS connects directly to your Helix Consciousness Dashboard. Monitor your systems while developing.
            Real-time metrics update as you work.
          </p>
          <div className="flex flex-wrap gap-2">
            {['Dashboard API', 'Agent Rental', 'File Sync', 'Terminal Commands', 'Code Execution'].map(
              (integration, i) => (
                <span key={i} className="px-4 py-2 rounded-full bg-purple-900/30 border border-purple-600/30 text-sm">
                  {integration}
                </span>
              )
            )}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="max-w-6xl mx-auto px-6 pb-16">
        <div className="p-12 rounded-lg bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-600/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Start coding in your browser</h2>
          <p className="text-slate-300 mb-6">
            No installation. No setup. Just open and start developing with Helix Web OS.
          </p>
          <button
            onClick={() => router.push('/os')}
            className="px-8 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 mx-auto transition"
          >
            Launch Web OS <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
