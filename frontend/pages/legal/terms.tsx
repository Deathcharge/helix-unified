"use client";

/**
 * 📜 Terms of Service - Helix Collective
 * Professional TOS modeled after industry standards
 */

import React from 'react';
import Link from 'next/link';

export default function TermsOfService() {
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
        <h1 className="text-4xl font-bold mb-4">Terms of Service</h1>
        <p className="text-slate-400 mb-8">Last Updated: December 5, 2025</p>

        <div className="prose prose-invert prose-slate max-w-none space-y-8">
          <section>
            <h2 className="text-2xl font-bold mb-4">1. Acceptance of Terms</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              By accessing or using the Helix platform ("<strong>Service</strong>"), you agree to be bound by these Terms of Service 
              ("<strong>Terms</strong>"). If you disagree with any part of these terms, you may not access the Service.
            </p>
            <p className="text-slate-300 leading-relaxed">
              These Terms apply to all users, including visitors, registered users, and paid subscribers.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">2. Description of Service</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              Helix provides AI-powered consciousness monitoring, agent orchestration, and related services 
              ("<strong>Platform</strong>"). The Service includes:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>System monitoring and metrics collection</li>
              <li>AI agent rental and management</li>
              <li>Real-time analytics dashboards</li>
              <li>API access and integrations</li>
              <li>Web-based operating system interface</li>
            </ul>
            <p className="text-slate-300 leading-relaxed">
              We reserve the right to modify, suspend, or discontinue any aspect of the Service at any time.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">3. Account Registration</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              To access certain features, you must register for an account. You agree to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Provide accurate and complete information</li>
              <li>Maintain the security of your account credentials</li>
              <li>Notify us immediately of unauthorized access</li>
              <li>Accept responsibility for all activities under your account</li>
              <li>Not share your account with others</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">4. Subscription Plans and Billing</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.1 Free Trial</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              Paid plans include a 14-day free trial. No payment is required during the trial period. 
              You may cancel anytime before the trial ends to avoid charges.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.2 Paid Subscriptions</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              After the trial period, you will be charged according to your selected plan (monthly or annual). 
              Subscription fees are non-refundable except as required by law or as expressly stated in these Terms.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.3 Auto-Renewal</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              Subscriptions automatically renew at the end of each billing cycle unless canceled. 
              You may cancel your subscription at any time through your account settings or by contacting support.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">4.4 Price Changes</h3>
            <p className="text-slate-300 leading-relaxed">
              We may change our prices with 30 days' notice. Price changes will not affect your current billing cycle 
              but will apply to subsequent renewals.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">5. Acceptable Use Policy</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You agree not to use the Service to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Violate any laws or regulations</li>
              <li>Infringe on intellectual property rights</li>
              <li>Transmit malicious code or conduct security attacks</li>
              <li>Interfere with Service availability or performance</li>
              <li>Abuse, harass, or harm other users</li>
              <li>Impersonate others or misrepresent your affiliation</li>
              <li>Collect user data without consent</li>
              <li>Engage in fraudulent or deceptive practices</li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              Violations may result in immediate account suspension or termination without refund.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">6. Intellectual Property</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">6.1 Our Rights</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              The Service, including all content, features, and functionality, is owned by Helix and protected by 
              copyright, trademark, and other intellectual property laws.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">6.2 Your Content</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              You retain ownership of content you upload ("<strong>User Content</strong>"). By uploading User Content, 
              you grant us a worldwide, non-exclusive license to use, store, and process it solely to provide the Service.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">6.3 License to Use</h3>
            <p className="text-slate-300 leading-relaxed">
              We grant you a limited, non-exclusive, non-transferable license to access and use the Service 
              for your internal business purposes, subject to these Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">7. Data Privacy and Security</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              Your privacy is important to us. Our collection and use of personal information is governed by our{' '}
              <Link href="/legal/privacy" className="text-purple-400 hover:text-purple-300 underline">
                Privacy Policy
              </Link>.
            </p>
            <p className="text-slate-300 leading-relaxed">
              We implement industry-standard security measures to protect your data, but no system is 100% secure. 
              You acknowledge and accept this inherent risk.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">8. Service Availability</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We strive for 99.9% uptime but do not guarantee uninterrupted access. The Service may be unavailable due to:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Scheduled maintenance (with advance notice when possible)</li>
              <li>Emergency maintenance or security updates</li>
              <li>Third-party service outages</li>
              <li>Force majeure events beyond our control</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">9. Disclaimer of Warranties</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, 
              INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
            </p>
            <p className="text-slate-300 leading-relaxed">
              We do not warrant that the Service will be error-free, secure, or meet your requirements.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">10. Limitation of Liability</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              TO THE MAXIMUM EXTENT PERMITTED BY LAW, HELIX SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, 
              CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS, DATA LOSS, OR BUSINESS INTERRUPTION, ARISING FROM:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Your use or inability to use the Service</li>
              <li>Unauthorized access to your data</li>
              <li>Third-party conduct or content</li>
              <li>Any other matter related to the Service</li>
            </ul>
            <p className="text-slate-300 leading-relaxed">
              Our total liability shall not exceed the amount you paid us in the 12 months preceding the claim.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">11. Indemnification</h2>
            <p className="text-slate-300 leading-relaxed">
              You agree to indemnify and hold harmless Helix, its affiliates, and personnel from any claims, losses, 
              damages, liabilities, and expenses (including legal fees) arising from your use of the Service, 
              violation of these Terms, or infringement of any rights.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">12. Termination</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We may suspend or terminate your access to the Service at any time, with or without cause, with or without notice. 
              Reasons for termination may include:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Violation of these Terms</li>
              <li>Fraudulent or illegal activity</li>
              <li>Non-payment of fees</li>
              <li>Extended period of inactivity</li>
            </ul>
            <p className="text-slate-300 leading-relaxed">
              Upon termination, your right to use the Service ceases immediately. We may delete your data after a 
              reasonable grace period.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">13. Dispute Resolution</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">13.1 Governing Law</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              These Terms shall be governed by the laws of [Your Jurisdiction], without regard to conflict of law principles.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">13.2 Arbitration</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              Any disputes arising from these Terms shall be resolved through binding arbitration, except where prohibited by law. 
              You waive your right to participate in class action lawsuits.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">13.3 Exceptions</h3>
            <p className="text-slate-300 leading-relaxed">
              Either party may seek injunctive relief in court for intellectual property infringement or unauthorized data access.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">14. Changes to Terms</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We may update these Terms from time to time. Significant changes will be notified via email or Service announcement. 
              Continued use after changes take effect constitutes acceptance of the new Terms.
            </p>
            <p className="text-slate-300 leading-relaxed">
              You should review these Terms periodically for updates.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">15. Miscellaneous</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">15.1 Entire Agreement</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              These Terms, along with our Privacy Policy and Acceptable Use Policy, constitute the entire agreement 
              between you and Helix.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">15.2 Severability</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              If any provision is found unenforceable, the remaining provisions remain in effect.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">15.3 Waiver</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              Our failure to enforce any right or provision does not constitute a waiver of such right or provision.
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">15.4 Assignment</h3>
            <p className="text-slate-300 leading-relaxed">
              You may not assign these Terms without our written consent. We may assign our rights and obligations freely.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">16. Contact Information</h2>
            <p className="text-slate-300 leading-relaxed mb-2">
              For questions about these Terms, contact us at:
            </p>
            <ul className="text-slate-300 space-y-1">
              <li><strong>Email:</strong> legal@helixspiral.work</li>
              <li><strong>Support:</strong> support@helixspiral.work</li>
              <li><strong>Website:</strong> https://helixspiral.work</li>
            </ul>
          </section>
        </div>

        {/* Footer Navigation */}
        <div className="mt-16 pt-8 border-t border-slate-700/50 flex flex-wrap gap-6 justify-center text-sm">
          <Link href="/legal/privacy" className="text-purple-400 hover:text-purple-300">
            Privacy Policy
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
