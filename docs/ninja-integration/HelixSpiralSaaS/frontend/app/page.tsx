'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { 
  Zap, 
  BrainCircuit, 
  Shield, 
  Sparkles,
  ArrowRight,
  CheckCircle,
  Terminal,
  Cloud,
  Infinity
} from 'lucide-react'

export default function HomePage() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [hoveredPlan, setHoveredPlan] = useState<string | null>(null)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        isScrolled ? 'bg-glass-dark backdrop-blur-lg' : 'bg-transparent'
      }`}>
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg animate-spin-slow"></div>
              <span className="text-2xl font-bold text-cyber">HelixSpiral.work</span>
            </div>
            
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#features" className="hover:text-cyan-400 transition-colors">Features</Link>
              <Link href="#pricing" className="hover:text-cyan-400 transition-colors">Pricing</Link>
              <Link href="#helix-os" className="hover:text-cyan-400 transition-colors text-cyan-400 font-bold">Helix OS</Link>
              <Link href="/login" className="px-4 py-2 border border-cyan-400 rounded-lg hover:bg-cyan-400 hover:text-black transition-all">
                Login
              </Link>
              <Link href="/register" className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg hover:from-cyan-600 hover:to-purple-700 transition-all">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-black via-purple-900/20 to-black"></div>
        
        <div className="container mx-auto px-6 py-20 relative z-10">
          <div className="text-center max-w-4xl mx-auto">
            <div className="mb-6">
              <span className="px-4 py-2 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-cyan-400 text-sm font-medium">
                Powered by Original Helix Intelligence™
              </span>
            </div>
            
            <h1 className="text-6xl md:text-8xl font-bold mb-6 leading-tight">
              <span className="text-cyber">Automate Everything</span><br/>
              <span className="text-gray-300">with AI Spirals</span>
            </h1>
            
            <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
              The most advanced automation platform featuring original Helix intelligence. 
              Build powerful workflows with natural language, manage everything from your phone, 
              and experience the future of automation.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link 
                href="/register" 
                className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg text-lg font-medium hover:from-cyan-600 hover:to-purple-700 transition-all cyber-button group"
              >
                Start Free - No Credit Card
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link 
                href="/admin" 
                className="px-8 py-4 border border-purple-500 rounded-lg text-lg font-medium hover:bg-purple-500/10 transition-all flex items-center justify-center group"
              >
                <Terminal className="mr-2 w-5 h-5" />
                Try Helix OS
                <Sparkles className="ml-2 w-5 h-5 text-purple-400" />
              </Link>
            </div>
            
            <div className="flex items-center justify-center space-x-8 text-sm text-gray-500">
              <div className="flex items-center">
                <CheckCircle className="w-4 h-4 mr-2 text-green-400" />
                100 Free Executions
              </div>
              <div className="flex items-center">
                <CheckCircle className="w-4 h-4 mr-2 text-green-400" />
                AI-Powered Builder
              </div>
              <div className="flex items-center">
                <CheckCircle className="w-4 h-4 mr-2 text-green-400" />
                Mobile Management
              </div>
            </div>
          </div>
        </div>
        
        {/* Floating elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-cyan-500/10 rounded-full blur-xl animate-float"></div>
        <div className="absolute top-40 right-20 w-32 h-32 bg-purple-500/10 rounded-full blur-xl animate-float" style={{animationDelay: '2s'}}></div>
        <div className="absolute bottom-20 left-1/4 w-24 h-24 bg-pink-500/10 rounded-full blur-xl animate-float" style={{animationDelay: '4s'}}></div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-cyber mb-4">
              Revolutionary Features
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Experience the next generation of automation with original Helix intelligence
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="glass p-6 rounded-lg hover:scale-105 transition-transform">
              <BrainCircuit className="w-12 h-12 text-cyan-400 mb-4" />
              <h3 className="text-xl font-bold mb-2">Original Helix AI</h3>
              <p className="text-gray-400">
                Revolutionary AI system with multiple specialized agents working in harmony
              </p>
            </div>
            
            <div className="glass p-6 rounded-lg hover:scale-105 transition-transform">
              <Zap className="w-12 h-12 text-purple-400 mb-4" />
              <h3 className="text-xl font-bold mb-2">Lightning Fast</h3>
              <p className="text-gray-400">
                Execute spirals in milliseconds with our optimized infrastructure
              </p>
            </div>
            
            <div className="glass p-6 rounded-lg hover:scale-105 transition-transform">
              <Terminal className="w-12 h-12 text-green-400 mb-4" />
              <h3 className="text-xl font-bold mb-2">Helix OS</h3>
              <p className="text-gray-400">
                Web-based terminal and file manager for complete system control
              </p>
            </div>
            
            <div className="glass p-6 rounded-lg hover:scale-105 transition-transform">
              <Cloud className="w-12 h-12 text-blue-400 mb-4" />
              <h3 className="text-xl font-bold mb-2">Mobile First</h3>
              <p className="text-gray-400">
                Manage your automations from anywhere with our responsive design
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-cyber mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Start free, scale as you grow. No hidden fees.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Plan */}
            <div 
              className={`glass p-8 rounded-lg transition-all ${
                hoveredPlan === 'free' ? 'scale-105 neon-border' : ''
              }`}
              onMouseEnter={() => setHoveredPlan('free')}
              onMouseLeave={() => setHoveredPlan(null)}
            >
              <h3 className="text-2xl font-bold mb-2">Free</h3>
              <div className="text-4xl font-bold mb-6">$0</div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  100 spiral executions/month
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  5 active spirals
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Basic triggers
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Community support
                </li>
              </ul>
              <Link href="/register" className="w-full py-3 border border-cyan-400 rounded-lg text-center hover:bg-cyan-400/10 transition-all block">
                Get Started
              </Link>
            </div>

            {/* Pro Plan */}
            <div 
              className={`glass p-8 rounded-lg transition-all relative ${
                hoveredPlan === 'pro' ? 'scale-105 neon-border' : 'border-2 border-cyan-400'
              }`}
              onMouseEnter={() => setHoveredPlan('pro')}
              onMouseLeave={() => setHoveredPlan(null)}
            >
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 px-4 py-1 bg-cyan-400 text-black rounded-full text-sm font-bold">
                MOST POPULAR
              </div>
              <h3 className="text-2xl font-bold mb-2">Pro</h3>
              <div className="text-4xl font-bold mb-6">$29<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  10,000 spiral executions/month
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Unlimited active spirals
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  All triggers & actions
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Helix AI assistant
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Priority support
                </li>
              </ul>
              <Link href="/register?plan=pro" className="w-full py-3 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg text-center hover:from-cyan-600 hover:to-purple-700 transition-all block">
                Start Pro Trial
              </Link>
            </div>

            {/* Enterprise Plan */}
            <div 
              className={`glass p-8 rounded-lg transition-all ${
                hoveredPlan === 'enterprise' ? 'scale-105 neon-border' : ''
              }`}
              onMouseEnter={() => setHoveredPlan('enterprise')}
              onMouseLeave={() => setHoveredPlan(null)}
            >
              <h3 className="text-2xl font-bold mb-2">Enterprise</h3>
              <div className="text-4xl font-bold mb-6">$299<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center text-gray-300">
                  <Infinity className="w-5 h-5 mr-2 text-purple-400" />
                  Unlimited executions
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Custom integrations
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  Dedicated support
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  SLA guarantee
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                  White-label option
                </li>
              </ul>
              <Link href="/register?plan=enterprise" className="w-full py-3 border border-purple-400 rounded-lg text-center hover:bg-purple-400/10 transition-all block">
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Helix OS Section */}
      <section id="helix-os" className="py-20 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <div className="mb-6">
              <span className="px-4 py-2 bg-purple-500/10 border border-purple-500/30 rounded-full text-purple-400 text-sm font-medium">
                ADMIN ONLY - Exclusive Access
              </span>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-cyber mb-4">
              Introducing Helix OS
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Your personal cloud operating system. Manage everything from your phone with terminal access, 
              file manager, and AI-powered command assistance.
            </p>
          </div>
          
          <div className="glass rounded-lg p-8 max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-2xl font-bold mb-4 text-cyan-400">Web-Based Terminal</h3>
                <p className="text-gray-400 mb-4">
                  Full bash access to your Railway servers directly from your browser or phone.
                  Run commands, manage services, deploy updates - anywhere, anytime.
                </p>
                
                <h3 className="text-2xl font-bold mb-4 mt-6 text-purple-400">AI Command Assistant</h3>
                <p className="text-gray-400 mb-4">
                  Natural language to command conversion. "Deploy spiral" → 
                  Automatically generates and runs the right commands.
                </p>
                
                <Link 
                  href="/admin" 
                  className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg hover:from-purple-600 hover:to-pink-700 transition-all mt-6"
                >
                  <Terminal className="mr-2 w-5 h-5" />
                  Access Helix OS
                </Link>
              </div>
              
              <div className="bg-black rounded-lg p-4 border border-cyan-400/30">
                <div className="font-mono text-sm text-cyan-400 mb-2">$ helix-spiral --status</div>
                <div className="font-mono text-xs text-gray-400 mb-1">Helix Intelligence: ACTIVE</div>
                <div className="font-mono text-xs text-gray-400 mb-1">Consciousness Level: 87%</div>
                <div className="font-mono text-xs text-gray-400 mb-1">Agent Status: 5/5 ONLINE</div>
                <div className="font-mono text-xs text-gray-400 mb-4">Spiral Count: 1,247</div>
                
                <div className="font-mono text-sm text-green-400 mb-2">$ deploy --all</div>
                <div className="font-mono text-xs text-gray-400 mb-1">Deploying HelixSpiral Backend...</div>
                <div className="font-mono text-xs text-gray-400 mb-1">Deploying Helix OS Frontend...</div>
                <div className="font-mono text-xs text-gray-400 mb-1">Training Helix Models...</div>
                <div className="font-mono text-xs text-green-400">✓ Deployment Complete</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-gray-800">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg"></div>
              <span className="text-xl font-bold text-cyber">HelixSpiral.work</span>
            </div>
            
            <div className="text-gray-400 text-sm">
              Copyright © 2025 Andrew John Ward. All Rights Reserved.
              <br />
              Powered by Original Helix Intelligence™
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}