"use client";

/**
 * 💰 Pricing Page
 * All subscription tiers and features overview
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Check, ArrowRight, Zap, Brain, Users, Clock } from 'lucide-react';

export default function Pricing() {
  const router = useRouter();
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');
  const [selectedPlan, setSelectedPlan] = useState<'pro' | 'enterprise'>('pro');

  const handleUpgrade = (plan: 'pro' | 'enterprise') => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/signup');
      return;
    }

    setSelectedPlan(plan);
    router.push('/settings/billing');
  };

  const plans = [
    {
      id: 'free',
      name: 'Free',
      description: 'Perfect for getting started',
      price: 0,
      monthly: 0,
      features: [
        '1 monitored system',
        '7-day metrics history',
        '1,000 API calls/month',
        'Basic dashboard',
        'Email support',
        'Community access',
      ],
      limitations: ['No real-time alerts', 'Single system only'],
      cta: 'Get Started Free',
      ctaAction: () => router.push('/auth/signup'),
      highlight: false,
    },
    {
      id: 'pro',
      name: 'Professional',
      description: 'For growing teams',
      price: billingCycle === 'monthly' ? 99 : 990,
      monthly: 99,
      features: [
        '10 monitored systems',
        '30-day metrics history',
        '100,000 API calls/month',
        'Advanced dashboard with alerts',
        'Real-time notifications',
        'API access',
        'Priority email support',
        'Custom integrations',
        'Team collaboration (up to 5 members)',
      ],
      limitations: [],
      cta: billingCycle === 'monthly' ? 'Start Free Trial' : 'Save 17%',
      ctaAction: () => handleUpgrade('pro'),
      highlight: true,
      savings: billingCycle === 'annual' ? 'Save $198/year' : null,
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      description: 'For large-scale operations',
      price: billingCycle === 'monthly' ? 499 : 4990,
      monthly: 499,
      features: [
        'Unlimited monitored systems',
        '1-year metrics history',
        '10M API calls/month',
        'White-label dashboard',
        'Advanced ML predictions',
        'Webhooks & streaming',
        '24/7 phone & email support',
        'Dedicated account manager',
        'Custom SLAs',
        'Multi-team management',
        'Advanced security features',
        'Custom integrations',
      ],
      limitations: [],
      cta: 'Contact Sales',
      ctaAction: () => (window.location.href = 'mailto:sales@helixspiral.work'),
      highlight: false,
      badge: 'Most Popular',
    },
  ];

  const comparisonFeatures = [
    { name: 'Monitored Systems', free: '1', pro: '10', enterprise: 'Unlimited' },
    { name: 'Metrics History', free: '7 days', pro: '30 days', enterprise: '1 year' },
    { name: 'API Calls/Month', free: '1,000', pro: '100,000', enterprise: '10,000,000' },
    { name: 'Real-time Alerts', free: 'No', pro: 'Yes', enterprise: 'Yes' },
    { name: 'Webhooks', free: 'No', pro: 'Yes', enterprise: 'Yes' },
    { name: 'Team Members', free: '1', pro: 'Up to 5', enterprise: 'Unlimited' },
    { name: 'White Label', free: 'No', pro: 'No', enterprise: 'Yes' },
    { name: 'Support', free: 'Community', pro: 'Email', enterprise: '24/7 Phone' },
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
            <Link href="/" className="text-slate-400 hover:text-slate-200 transition">
              Home
            </Link>
            <Link href="/auth/login" className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 transition">
              Login
            </Link>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-5xl mx-auto px-6 py-16 text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6">Simple, Transparent Pricing</h1>
        <p className="text-xl text-slate-300 mb-8">
          Start free. Scale as you grow. No credit card required.
        </p>

        {/* Billing Toggle */}
        <div className="inline-flex items-center gap-4 p-1 rounded-lg bg-slate-800/50 border border-slate-700/50 mb-12">
          <button
            onClick={() => setBillingCycle('monthly')}
            className={`px-6 py-2 rounded font-semibold transition ${
              billingCycle === 'monthly'
                ? 'bg-purple-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Monthly
          </button>
          <button
            onClick={() => setBillingCycle('annual')}
            className={`px-6 py-2 rounded font-semibold transition relative ${
              billingCycle === 'annual'
                ? 'bg-purple-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Annual
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-xs font-bold text-green-400 whitespace-nowrap">
              Save 17%
            </span>
          </button>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="max-w-7xl mx-auto px-6 pb-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative rounded-lg border transition-all duration-300 ${
                plan.highlight
                  ? 'md:scale-105 bg-gradient-to-b from-purple-900/40 to-slate-900/40 border-purple-600/40 shadow-2xl shadow-purple-600/20'
                  : 'bg-slate-900/30 border-slate-700/50 hover:border-purple-600/30'
              }`}
            >
              {plan.badge && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xs font-bold">
                  {plan.badge}
                </div>
              )}

              <div className="p-8 h-full flex flex-col">
                <div className="mb-6">
                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <p className="text-slate-400 text-sm">{plan.description}</p>
                </div>

                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-bold">${plan.price}</span>
                    {plan.monthly > 0 && (
                      <span className="text-slate-400">
                        /{billingCycle === 'monthly' ? 'month' : 'year'}
                      </span>
                    )}
                  </div>
                  {plan.savings && <p className="text-sm text-green-400 font-semibold mt-2">{plan.savings}</p>}
                  {plan.monthly > 0 && billingCycle === 'annual' && (
                    <p className="text-xs text-slate-400 mt-1">${(plan.price / 12).toFixed(0)}/month billed annually</p>
                  )}
                </div>

                {/* CTA Button */}
                <button
                  onClick={plan.ctaAction}
                  className={`w-full px-4 py-2 rounded font-semibold flex items-center justify-center gap-2 mb-6 transition ${
                    plan.highlight
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                  }`}
                >
                  {plan.cta}
                  <ArrowRight className="w-4 h-4" />
                </button>

                {/* Features */}
                <div className="space-y-3 flex-1 mb-6">
                  {plan.features.map((feature, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <Check className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span className="text-sm">{feature}</span>
                    </div>
                  ))}
                </div>

                {/* Limitations */}
                {plan.limitations.length > 0 && (
                  <div className="pt-6 border-t border-slate-700/30 space-y-2">
                    {plan.limitations.map((limitation, i) => (
                      <div key={i} className="flex items-start gap-3 opacity-60">
                        <div className="w-5 h-5 text-slate-600 flex-shrink-0 mt-0.5">–</div>
                        <span className="text-sm text-slate-400">{limitation}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Comparison Table */}
      <div className="max-w-6xl mx-auto px-6 mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">Complete Feature Comparison</h2>

        <div className="rounded-lg bg-slate-900/30 border border-slate-700/50 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700/50 bg-slate-800/50">
                  <th className="px-6 py-4 text-left font-semibold">Feature</th>
                  <th className="px-6 py-4 text-center font-semibold">Free</th>
                  <th className="px-6 py-4 text-center font-semibold">Professional</th>
                  <th className="px-6 py-4 text-center font-semibold">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {comparisonFeatures.map((feature, i) => (
                  <tr key={i} className="border-b border-slate-700/30 hover:bg-slate-800/30 transition">
                    <td className="px-6 py-4 font-medium">{feature.name}</td>
                    <td className="px-6 py-4 text-center text-slate-300">{feature.free}</td>
                    <td className="px-6 py-4 text-center text-slate-300 font-semibold text-purple-400">
                      {feature.pro}
                    </td>
                    <td className="px-6 py-4 text-center text-slate-300">{feature.enterprise}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* FAQ-style Section */}
      <div className="max-w-4xl mx-auto px-6 mb-16">
        <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-400" />
              Can I switch plans anytime?
            </h3>
            <p className="text-slate-400 text-sm">
              Yes! Upgrade or downgrade your plan at any time. Changes take effect immediately.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <Zap className="w-5 h-5 text-purple-400" />
              What happens if I exceed my limits?
            </h3>
            <p className="text-slate-400 text-sm">
              We'll notify you and you can upgrade immediately. No surprises or overage charges.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <Users className="w-5 h-5 text-purple-400" />
              Do you offer team discounts?
            </h3>
            <p className="text-slate-400 text-sm">
              Yes! Enterprise plans include team management. Contact sales for bulk pricing.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <Clock className="w-5 h-5 text-purple-400" />
              Is there a free trial?
            </h3>
            <p className="text-slate-400 text-sm">
              Pro plan includes a 14-day free trial with full feature access. No credit card required.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-4xl mx-auto px-6 pb-16">
        <div className="p-12 rounded-lg bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-600/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to monitor consciousness?</h2>
          <p className="text-slate-300 mb-6">
            Join 1000+ teams using Helix to monitor and optimize their AI systems.
          </p>
          <button
            onClick={() => router.push('/auth/signup')}
            className="px-8 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold text-white flex items-center gap-2 mx-auto transition"
          >
            Get Started Free <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-purple-800/30 bg-slate-950/50 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-slate-400 text-sm">
          <p>All prices in USD. Billing occurs at the end of your trial or monthly subscription period.</p>
        </div>
      </div>
    </div>
  );
}
