"use client";

/**
 * 🔒 Privacy Policy - Helix Collective
 * GDPR-compliant privacy policy
 */

import React from 'react';
import Link from 'next/link';

export default function PrivacyPolicy() {
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
            <Link href="/pricing" className="text-slate-400 hover:text-slate-200 transition">
              Pricing
            </Link>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-16">
        <h1 className="text-4xl font-bold mb-4">Privacy Policy</h1>
        <p className="text-slate-400 mb-8">Last Updated: December 5, 2025</p>

        <div className="prose prose-invert prose-slate max-w-none space-y-8">
          <section>
            <h2 className="text-2xl font-bold mb-4">Our Commitment to Privacy</h2>
            <p className="text-slate-300 leading-relaxed">
              At Helix, we take your privacy seriously. This Privacy Policy explains how we collect, use, disclose, and safeguard 
              your information when you use our Service. By using Helix, you consent to the practices described in this policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">1. Information We Collect</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.1 Information You Provide</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li><strong>Account Information:</strong> Name, email address, password</li>
              <li><strong>Payment Information:</strong> Billing details (processed securely via Stripe)</li>
              <li><strong>Profile Data:</strong> Company name, job title, preferences</li>
              <li><strong>Communications:</strong> Support tickets, feedback, inquiries</li>
              <li><strong>User Content:</strong> Files, configurations, and data you upload</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.2 Automatically Collected Information</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li><strong>Usage Data:</strong> Pages visited, features used, interaction patterns</li>
              <li><strong>Device Information:</strong> IP address, browser type, operating system</li>
              <li><strong>Cookies:</strong> Session tokens, preferences, analytics (see Cookie Policy)</li>
              <li><strong>Performance Metrics:</strong> API call counts, system performance data</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.3 Third-Party Data</h3>
            <p className="text-slate-300 leading-relaxed">
              We may receive information from third-party services you connect (e.g., OAuth providers, integrations).
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">2. How We Use Your Information</h2>
            <p className="text-slate-300 leading-relaxed mb-4">We use your information to:</p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li><strong>Provide the Service:</strong> Account management, feature access, support</li>
              <li><strong>Process Payments:</strong> Billing, invoicing, subscription management</li>
              <li><strong>Improve Our Service:</strong> Analytics, bug fixes, new features</li>
              <li><strong>Communicate:</strong> Service updates, security alerts, marketing (with consent)</li>
              <li><strong>Security:</strong> Fraud detection, abuse prevention, threat monitoring</li>
              <li><strong>Compliance:</strong> Legal obligations, law enforcement requests</li>
              <li><strong>Research:</strong> Aggregated, anonymized analytics (no personal identification)</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">3. Legal Basis for Processing (GDPR)</h2>
            <p className="text-slate-300 leading-relaxed mb-4">For EU/EEA users, we process your data under:</p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li><strong>Contract Performance:</strong> Providing the Service you've subscribed to</li>
              <li><strong>Legitimate Interests:</strong> Service improvement, security, fraud prevention</li>
              <li><strong>Consent:</strong> Marketing communications, optional features</li>
              <li><strong>Legal Compliance:</strong> Regulatory requirements, law enforcement</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">4. Data Sharing and Disclosure</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We do <strong>not</strong> sell your personal information. We may share data with:
            </p>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.1 Service Providers</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li><strong>Payment Processing:</strong> Stripe (payment processing)</li>
              <li><strong>Infrastructure:</strong> Railway, Vercel (hosting)</li>
              <li><strong>Analytics:</strong> Aggregated usage statistics</li>
              <li><strong>Support:</strong> Customer service tools</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.2 Legal Requirements</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              We may disclose information if required by law, court order, or to protect our rights and safety.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.3 Business Transfers</h3>
            <p className="text-slate-300 leading-relaxed">
              If Helix is acquired or merged, your information may be transferred to the new entity.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">5. Data Retention</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We retain your information for as long as your account is active or as needed to provide services. After account deletion:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Account data is deleted within 90 days</li>
              <li>Backups may persist for up to 6 months for disaster recovery</li>
              <li>Aggregated, anonymized data may be retained indefinitely</li>
              <li>Legal or compliance data retained as required by law</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">6. Your Rights</h2>
            <p className="text-slate-300 leading-relaxed mb-4">You have the right to:</p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li><strong>Access:</strong> Request a copy of your personal data</li>
              <li><strong>Rectification:</strong> Correct inaccurate information</li>
              <li><strong>Erasure:</strong> Request deletion of your data ("right to be forgotten")</li>
              <li><strong>Portability:</strong> Receive your data in machine-readable format</li>
              <li><strong>Restriction:</strong> Limit how we process your data</li>
              <li><strong>Objection:</strong> Opt-out of certain processing activities</li>
              <li><strong>Withdraw Consent:</strong> Cancel previously given consent</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              To exercise these rights, contact us at <strong>privacy@helixspiral.work</strong>
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">7. Data Security</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We implement industry-standard security measures including:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Encryption in transit (TLS/SSL) and at rest</li>
              <li>Regular security audits and penetration testing</li>
              <li>Access controls and authentication (JWT, OAuth)</li>
              <li>Secure database practices and backups</li>
              <li>Employee training on data protection</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              Despite our efforts, no system is 100% secure. You acknowledge this inherent risk.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">8. International Data Transfers</h2>
            <p className="text-slate-300 leading-relaxed">
              Your data may be transferred to and processed in countries other than your own. We ensure appropriate 
              safeguards are in place, including Standard Contractual Clauses (SCCs) for EU data transfers.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">9. Children's Privacy</h2>
            <p className="text-slate-300 leading-relaxed">
              Our Service is not directed to individuals under 13 (or 16 in the EU). We do not knowingly collect 
              personal information from children. If you believe a child has provided us with data, contact us immediately.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">10. Cookies and Tracking</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We use cookies and similar technologies for:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li><strong>Essential Cookies:</strong> Authentication, security, basic functionality</li>
              <li><strong>Analytics Cookies:</strong> Usage statistics, performance monitoring</li>
              <li><strong>Preference Cookies:</strong> Settings, language, theme</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              You can control cookies through your browser settings. Disabling cookies may limit Service functionality.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">11. Changes to This Policy</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this Privacy Policy periodically. Significant changes will be notified via email or Service announcement. 
              Continued use after changes constitutes acceptance of the updated policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">12. Contact Us</h2>
            <p className="text-slate-300 leading-relaxed mb-2">
              For privacy-related inquiries:
            </p>
            <ul className="text-slate-300 space-y-1">
              <li><strong>Privacy Team:</strong> privacy@helixspiral.work</li>
              <li><strong>Data Protection Officer:</strong> dpo@helixspiral.work</li>
              <li><strong>General Inquiries:</strong> support@helixspiral.work</li>
            </ul>
          </section>

          <section className="bg-purple-900/20 border border-purple-700/30 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Your Privacy Matters</h2>
            <p className="text-slate-300 leading-relaxed">
              We are committed to protecting your privacy and being transparent about our data practices. 
              If you have questions or concerns, please don't hesitate to reach out.
            </p>
          </section>
        </div>

        {/* Footer Navigation */}
        <div className="mt-16 pt-8 border-t border-slate-700/50 flex flex-wrap gap-6 justify-center text-sm">
          <Link href="/legal/terms" className="text-purple-400 hover:text-purple-300">
            Terms of Service
          </Link>
          <Link href="/legal/acceptable-use" className="text-purple-400 hover:text-purple-300">
            Acceptable Use Policy
          </Link>
          <Link href="/pricing" className="text-purple-400 hover:text-purple-300">
            Pricing
          </Link>
          <Link href="/" className="text-purple-400 hover:text-purple-300">
            Home
          </Link>
        </div>
      </div>
    </div>
  );
}
