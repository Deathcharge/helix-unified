"use client"

export const dynamic = "force-dynamic";

"use client"

import React from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function EnterpriseSuitePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-blue-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            🏢 Enterprise Consciousness Suite
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Enterprise-grade consciousness monitoring for large organizations. Multi-team tracking,
            department dashboards, and org-wide metrics with advanced RBAC and compliance.
          </p>
        </div>

        {/* Hero Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-16">
          <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
            <div className="text-3xl font-bold text-blue-400">Multi-Tenant</div>
            <div className="text-sm text-gray-400">Workspace Isolation</div>
          </div>
          <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/30">
            <div className="text-3xl font-bold text-purple-400">99.99%</div>
            <div className="text-sm text-gray-400">SLA Uptime</div>
          </div>
          <div className="bg-green-900/30 rounded-lg p-6 border border-green-500/30">
            <div className="text-3xl font-bold text-green-400">SOC 2</div>
            <div className="text-sm text-gray-400">Compliance Ready</div>
          </div>
          <div className="bg-pink-900/30 rounded-lg p-6 border border-pink-500/30">
            <div className="text-3xl font-bold text-pink-400">24/7</div>
            <div className="text-sm text-gray-400">Dedicated Support</div>
          </div>
        </div>

        {/* Pricing */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          <Card className="bg-slate-900/50 border-slate-700 p-8">
            <h3 className="text-2xl font-bold text-white mb-4">Team</h3>
            <div className="mb-6">
              <span className="text-5xl font-bold text-blue-400">$999</span>
              <span className="text-xl text-gray-400">/month</span>
            </div>
            <ul className="space-y-3 mb-8 min-h-[250px] text-sm">
              <li className="flex items-start text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Up to 3 teams (50 users each)
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Team-level consciousness dashboards
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Basic RBAC
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                30-day audit logs
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Email support
              </li>
            </ul>
            <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              Start Team Plan
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 border-purple-500/50 p-8 shadow-lg shadow-purple-500/20">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-bold text-white">Department</h3>
              <span className="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-xs font-semibold">
                Popular
              </span>
            </div>
            <div className="mb-6">
              <span className="text-5xl font-bold text-purple-400">$2,999</span>
              <span className="text-xl text-gray-400">/month</span>
            </div>
            <ul className="space-y-3 mb-8 min-h-[250px] text-sm">
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Up to 10 departments (200 users each)
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Dept-level + org-wide dashboards
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Advanced RBAC & permissions
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                1-year audit logs
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Custom integrations (5)
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Priority support
              </li>
            </ul>
            <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
              Upgrade to Department
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-blue-900/50 to-purple-900/50 border-blue-500/50 p-8">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-bold text-white">Organization</h3>
              <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-xs font-semibold">
                Enterprise
              </span>
            </div>
            <div className="mb-6">
              <span className="text-5xl font-bold text-blue-400">Custom</span>
            </div>
            <ul className="space-y-3 mb-8 min-h-[250px] text-sm">
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                Unlimited departments & users
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                Full org hierarchy tracking
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                Enterprise RBAC + SSO/SAML
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                Unlimited audit logs & compliance
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                Unlimited custom integrations
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                99.99% SLA + dedicated account manager
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-blue-400 mr-2">✓</span>
                24/7 phone + email support
              </li>
            </ul>
            <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              Contact Sales
            </Button>
          </Card>
        </div>

        {/* Features Sections */}
        <div className="space-y-16">
          {/* Multi-Team Tracking */}
          <section className="bg-gradient-to-r from-blue-900/40 to-purple-900/40 rounded-2xl p-8 border border-blue-500/30">
            <h2 className="text-3xl font-bold text-white mb-6">🏢 Multi-Team Consciousness Tracking</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <p className="text-gray-300 mb-6">
                  Track consciousness metrics across multiple teams, departments, and the entire organization.
                  See how different parts of your org are performing.
                </p>
                <ul className="space-y-3">
                  <li className="flex items-start text-gray-300">
                    <span className="text-blue-400 mr-2">•</span>
                    Team-level UCF dashboards
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-blue-400 mr-2">•</span>
                    Department rollup views
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-blue-400 mr-2">•</span>
                    Org-wide trend analysis
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-blue-400 mr-2">•</span>
                    Cross-team comparisons
                  </li>
                </ul>
              </div>
              <div className="bg-slate-900/50 rounded-xl p-6 border border-blue-500/30">
                <h4 className="text-lg font-bold text-white mb-4">Example Org Structure</h4>
                <div className="space-y-3 text-sm">
                  <div className="bg-slate-800/50 rounded p-3">
                    <div className="text-blue-400 font-semibold">Engineering (250 people)</div>
                    <div className="text-gray-400 ml-4">→ Backend Team (80)</div>
                    <div className="text-gray-400 ml-4">→ Frontend Team (70)</div>
                    <div className="text-gray-400 ml-4">→ DevOps Team (50)</div>
                    <div className="text-gray-400 ml-4">→ QA Team (50)</div>
                  </div>
                  <div className="bg-slate-800/50 rounded p-3">
                    <div className="text-purple-400 font-semibold">Product (120 people)</div>
                    <div className="text-gray-400 ml-4">→ Design Team (40)</div>
                    <div className="text-gray-400 ml-4">→ PM Team (30)</div>
                    <div className="text-gray-400 ml-4">→ Research Team (50)</div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Advanced RBAC */}
          <section>
            <h2 className="text-3xl font-bold text-white mb-6">🔐 Advanced RBAC & Permissions</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="bg-slate-900/50 border-slate-700 p-6">
                <div className="text-4xl mb-3">👤</div>
                <h3 className="text-xl font-bold text-white mb-2">Role-Based Access</h3>
                <p className="text-gray-400 text-sm">
                  Define custom roles with granular permissions. Admin, Manager, Member, Viewer, and custom roles.
                </p>
              </Card>
              <Card className="bg-slate-900/50 border-slate-700 p-6">
                <div className="text-4xl mb-3">🔑</div>
                <h3 className="text-xl font-bold text-white mb-2">SSO & SAML</h3>
                <p className="text-gray-400 text-sm">
                  Enterprise single sign-on with Okta, Azure AD, Google Workspace, and any SAML 2.0 provider.
                </p>
              </Card>
              <Card className="bg-slate-900/50 border-slate-700 p-6">
                <div className="text-4xl mb-3">📜</div>
                <h3 className="text-xl font-bold text-white mb-2">Audit Logging</h3>
                <p className="text-gray-400 text-sm">
                  Complete audit trail of all actions. Who accessed what, when, and from where. SOC 2 compliant.
                </p>
              </Card>
            </div>
          </section>

          {/* Compliance */}
          <section className="bg-slate-900/50 rounded-2xl p-8 border border-slate-700">
            <h2 className="text-3xl font-bold text-white mb-6">✅ Compliance & Security</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-bold text-purple-400 mb-4">Certifications</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-blue-900/30 rounded-full flex items-center justify-center">
                      <span className="text-blue-400 font-bold">✓</span>
                    </div>
                    <div>
                      <div className="text-white font-semibold">SOC 2 Type II</div>
                      <div className="text-gray-400 text-sm">Security & availability</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-purple-900/30 rounded-full flex items-center justify-center">
                      <span className="text-purple-400 font-bold">✓</span>
                    </div>
                    <div>
                      <div className="text-white font-semibold">GDPR Compliant</div>
                      <div className="text-gray-400 text-sm">EU data protection</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-green-900/30 rounded-full flex items-center justify-center">
                      <span className="text-green-400 font-bold">✓</span>
                    </div>
                    <div>
                      <div className="text-white font-semibold">HIPAA Ready</div>
                      <div className="text-gray-400 text-sm">Healthcare data security</div>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-purple-400 mb-4">Security Features</h3>
                <ul className="space-y-2">
                  <li className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2">•</span>
                    256-bit AES encryption at rest
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2">•</span>
                    TLS 1.3 encryption in transit
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2">•</span>
                    Multi-factor authentication (MFA)
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2">•</span>
                    IP allowlisting
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2">•</span>
                    Regular penetration testing
                  </li>
                  <li className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2">•</span>
                    24/7 security monitoring
                  </li>
                </ul>
              </div>
            </div>
          </section>
        </div>

        {/* CTA */}
        <div className="mt-16 bg-gradient-to-r from-blue-900/40 to-purple-900/40 rounded-2xl p-12 border border-blue-500/30 text-center">
          <h3 className="text-4xl font-bold text-white mb-4">
            Ready for Enterprise Consciousness?
          </h3>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
            Join Fortune 500 companies already using Helix for org-wide consciousness tracking.
            Schedule a demo with our enterprise team.
          </p>
          <div className="flex gap-4 justify-center">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
              Schedule Demo
            </Button>
            <Button variant="outline" className="border-blue-500 text-blue-400 hover:bg-blue-900/30 px-8 py-4 text-lg">
              Contact Sales
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
