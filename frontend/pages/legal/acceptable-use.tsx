"use client";

/**
 * ⚖️ Acceptable Use Policy - Helix Collective
 */

import React from 'react';
import Link from 'next/link';

export default function AcceptableUsePolicy() {
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
        <h1 className="text-4xl font-bold mb-4">Acceptable Use Policy</h1>
        <p className="text-slate-400 mb-8">Last Updated: December 5, 2025</p>

        <div className="prose prose-invert prose-slate max-w-none space-y-8">
          <section className="bg-purple-900/20 border border-purple-700/30 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Policy Overview</h2>
            <p className="text-slate-300 leading-relaxed">
              This Acceptable Use Policy ("AUP") governs your use of Helix's services. Violations may result 
              in immediate suspension or termination of your account without refund. We reserve the right to 
              investigate suspected violations and cooperate with law enforcement when necessary.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">1. Prohibited Activities</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You may NOT use Helix to:
            </p>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.1 Illegal Activities</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Violate any local, state, national, or international law</li>
              <li>Engage in fraudulent activities or financial scams</li>
              <li>Distribute or access child sexual abuse material (CSAM)</li>
              <li>Facilitate human trafficking or exploitation</li>
              <li>Infringe on intellectual property rights (copyright, trademark, patent)</li>
              <li>Engage in identity theft or impersonation</li>
              <li>Money laundering or terrorist financing</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.2 Security Violations</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Attempt unauthorized access to systems, accounts, or data</li>
              <li>Conduct port scanning, vulnerability testing, or penetration testing without written consent</li>
              <li>Distribute malware, viruses, worms, trojans, or ransomware</li>
              <li>Launch denial-of-service (DoS) or distributed denial-of-service (DDoS) attacks</li>
              <li>Bypass security measures or authentication systems</li>
              <li>Crack passwords or encryption</li>
              <li>Phishing, spoofing, or social engineering attacks</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.3 Abuse and Harassment</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Harass, threaten, stalk, or intimidate others</li>
              <li>Send unsolicited bulk messages (spam)</li>
              <li>Doxing (publishing private information without consent)</li>
              <li>Hate speech or content promoting violence</li>
              <li>Discrimination based on race, religion, gender, sexual orientation, disability, or other protected classes</li>
              <li>Impersonate individuals or organizations</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.4 Service Abuse</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Exceed rate limits or API quotas through automated abuse</li>
              <li>Create multiple accounts to circumvent restrictions</li>
              <li>Resell or redistribute the Service without authorization</li>
              <li>Reverse engineer, decompile, or disassemble our software</li>
              <li>Remove copyright notices, watermarks, or attribution</li>
              <li>Use the Service for cryptocurrency mining without explicit permission</li>
              <li>Overload infrastructure with excessive requests (intentional or negligent)</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">1.5 Content Violations</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Upload or share illegal, obscene, or defamatory content</li>
              <li>Store pirated software, media, or copyrighted materials</li>
              <li>Host content that violates third-party rights</li>
              <li>Distribute sexually explicit material involving minors</li>
              <li>Promote self-harm, suicide, or eating disorders</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">2. Permitted Use Cases</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              You MAY use Helix for:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li><strong>Legitimate Business Operations:</strong> System monitoring, analytics, automation</li>
              <li><strong>Research and Development:</strong> AI/ML experiments, data analysis (with proper consent)</li>
              <li><strong>Security Testing:</strong> On your own systems or with explicit written authorization</li>
              <li><strong>Personal Projects:</strong> Non-commercial hobby projects within your subscription limits</li>
              <li><strong>Educational Use:</strong> Learning, teaching, academic research (non-commercial)</li>
              <li><strong>Content Creation:</strong> Lawful content that respects others' rights</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">3. AI and Machine Learning Specific Rules</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">3.1 Responsible AI Use</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Do NOT use AI systems to generate illegal content</li>
              <li>Do NOT create deepfakes for fraud, defamation, or non-consensual purposes</li>
              <li>Do NOT train models on data you don't have rights to</li>
              <li>Respect robots.txt and API terms of service when scraping data</li>
              <li>Disclose AI-generated content when required by law or ethics</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">3.2 Data Collection Ethics</h3>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Obtain proper consent before collecting personal data</li>
              <li>Comply with GDPR, CCPA, and other data protection laws</li>
              <li>Do NOT scrape websites that prohibit it</li>
              <li>Anonymize data when possible</li>
              <li>Respect opt-out requests</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">4. Resource Limits</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              To ensure fair access for all users:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Respect API rate limits and quotas</li>
              <li>Optimize code to minimize unnecessary requests</li>
              <li>Do NOT attempt to bypass throttling or rate limiting</li>
              <li>Contact support if you need higher limits for legitimate use</li>
              <li>We may throttle or suspend accounts causing excessive load</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">5. Reporting Violations</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              If you become aware of AUP violations, report them to:
            </p>
            <ul className="text-slate-300 space-y-2 mb-4">
              <li><strong>Security Issues:</strong> security@helixspiral.work</li>
              <li><strong>Abuse Reports:</strong> abuse@helixspiral.work</li>
              <li><strong>Copyright Claims:</strong> dmca@helixspiral.work</li>
              <li><strong>General Concerns:</strong> support@helixspiral.work</li>
            </ul>
            <p className="text-slate-300 leading-relaxed">
              Include as much detail as possible: account information, timestamps, evidence, and impact.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">6. Enforcement</h2>
            
            <h3 className="text-xl font-semibold mb-3 text-purple-400">6.1 Investigation</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              We reserve the right to investigate suspected violations. This may include:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li>Reviewing account activity and logs</li>
              <li>Examining user content (when necessary for safety)</li>
              <li>Contacting you for clarification</li>
              <li>Cooperating with law enforcement</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">6.2 Consequences</h3>
            <p className="text-slate-300 leading-relaxed mb-4">
              Violations may result in:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2 mb-4">
              <li><strong>Warning:</strong> First-time minor violations</li>
              <li><strong>Temporary Suspension:</strong> Repeated or moderate violations (1-30 days)</li>
              <li><strong>Permanent Ban:</strong> Severe violations, illegal activity, or repeated offenses</li>
              <li><strong>Legal Action:</strong> Criminal activity, significant harm, or damages</li>
              <li><strong>No Refund:</strong> Fees are non-refundable upon termination for cause</li>
            </ul>

            <h3 className="text-xl font-semibold mb-3 text-purple-400">6.3 Appeals</h3>
            <p className="text-slate-300 leading-relaxed">
              If you believe your account was suspended in error, contact <strong>appeals@helixspiral.work</strong> within 14 days. 
              Provide your account details and explanation. We'll review and respond within 5 business days.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">7. Third-Party Services</h2>
            <p className="text-slate-300 leading-relaxed">
              If you integrate Helix with third-party services (APIs, OAuth providers, webhooks), you are responsible 
              for ensuring your use complies with their terms of service. Violations of third-party terms may constitute 
              violations of this AUP.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">8. Modifications to This Policy</h2>
            <p className="text-slate-300 leading-relaxed">
              We may update this AUP at any time. Significant changes will be announced via email or Service notification. 
              Continued use after changes constitutes acceptance. Review periodically to stay informed.
            </p>
          </section>

          <section className="bg-red-900/20 border border-red-700/30 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-red-400">Zero Tolerance</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We have ZERO TOLERANCE for:
            </p>
            <ul className="list-disc list-inside text-slate-300 space-y-2">
              <li>Child exploitation material (CSAM) - <strong>immediate ban + law enforcement notification</strong></li>
              <li>Terrorism or violent extremism - <strong>immediate ban + law enforcement notification</strong></li>
              <li>Human trafficking - <strong>immediate ban + law enforcement notification</strong></li>
              <li>Ransomware distribution - <strong>immediate ban + law enforcement notification</strong></li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              These violations result in immediate permanent ban, no appeal, with full cooperation with authorities.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">9. Questions</h2>
            <p className="text-slate-300 leading-relaxed">
              If you're unsure whether an activity is permitted, contact us BEFORE proceeding: <strong>legal@helixspiral.work</strong>
            </p>
            <p className="text-slate-300 leading-relaxed mt-4">
              It's better to ask than to risk account suspension.
            </p>
          </section>
        </div>

        {/* Footer Navigation */}
        <div className="mt-16 pt-8 border-t border-slate-700/50 flex flex-wrap gap-6 justify-center text-sm">
          <Link href="/legal/terms" className="text-purple-400 hover:text-purple-300">
            Terms of Service
          </Link>
          <Link href="/legal/privacy" className="text-purple-400 hover:text-purple-300">
            Privacy Policy
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
