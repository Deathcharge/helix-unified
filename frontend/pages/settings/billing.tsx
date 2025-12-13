"use client";

/**
 * 💳 Billing & Account Settings
 * Manage subscription, invoices, and account details
 */

import React, { useState, useEffect } from 'react';
import { CreditCard, Download, AlertCircle, CheckCircle, Calendar, DollarSign } from 'lucide-react';
import { useRouter } from 'next/router';
import { useFormatters } from '@/lib/use-formatters';

interface BillingInfo {
  tier: 'free' | 'pro' | 'enterprise';
  current_period: {
    api_calls_used: number;
    api_calls_included: number;
    additional_charges: number;
    estimated_total: number;
    period_start: string;
    period_end: string;
  };
  history: Array<{
    date: string;
    amount: number;
    api_calls: number;
    status: 'paid' | 'pending';
  }>;
}

interface Invoice {
  id: string;
  date: string;
  amount: number;
  status: 'paid' | 'pending';
  download_url: string;
}

export default function BillingSettings() {
  const router = useRouter();
  const formatters = useFormatters('USD'); // Default to USD, can be made dynamic
  const [billingInfo, setBillingInfo] = useState<BillingInfo | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [canceling, setCanceling] = useState(false);
  const [upgrading, setUpgrading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/login');
      return;
    }

    fetchBillingData(token);
  }, [router]);

  const fetchBillingData = async (token: string) => {
    try {
      const [billingRes, invoicesRes] = await Promise.all([
        fetch('/api/saas/dashboard/billing', {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch('/api/saas/dashboard/invoices', {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      if (!billingRes.ok || !invoicesRes.ok) {
        throw new Error('Failed to fetch billing info');
      }

      setBillingInfo(await billingRes.json());
      setInvoices(await invoicesRes.json());
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading billing');
      setLoading(false);
    }
  };

  const handleUpgradePlan = async (newTier: 'pro' | 'enterprise') => {
    setUpgrading(true);
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('/api/saas/dashboard/upgrade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ tier: newTier }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Upgrade failed');
      }

      // Redirect to Stripe checkout
      window.location.href = data.checkout_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upgrade failed');
    } finally {
      setUpgrading(false);
    }
  };

  const handleCancelSubscription = async () => {
    if (!confirm('Are you sure? You will lose access to premium features.')) {
      return;
    }

    setCanceling(true);
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('/api/saas/dashboard/cancel-subscription', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Cancellation failed');
      }

      alert('Subscription will be cancelled at the end of your current billing period');
      router.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Cancellation failed');
    } finally {
      setCanceling(false);
    }
  };

  const handleDownloadInvoice = (invoice: Invoice) => {
    // In a real implementation, this would trigger a download
    window.open(invoice.download_url, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin inline-block">⚡</div>
          <p className="text-slate-300 mt-2">Loading billing information...</p>
        </div>
      </div>
    );
  }

  const tierPricing: Record<string, number> = {
    free: 0,
    pro: 99,
    enterprise: 499,
  };

  const tierFeatures: Record<string, string[]> = {
    free: ['1 monitored system', '7-day history', '1,000 API calls/mo', 'Community support'],
    pro: ['10 monitored systems', '30-day history', '100,000 API calls/mo', 'Email support', 'Alerts'],
    enterprise: ['Unlimited systems', '1-year history', '10M API calls/mo', '24/7 phone support', 'Custom integrations'],
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 text-slate-100">
      {/* Header */}
      <div className="border-b border-purple-800/30 bg-slate-950/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3 mb-2">
            <CreditCard className="w-6 h-6 text-purple-400" />
            <h1 className="text-2xl font-bold">Billing & Account</h1>
          </div>
          <p className="text-slate-400">Manage your subscription and payment methods</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-950/30 border border-red-600/30 text-red-300 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {/* Current Billing Period */}
        {billingInfo && (
          <div className="mb-8 p-6 rounded-lg bg-slate-800/40 border border-purple-600/30">
            <h2 className="text-xl font-semibold mb-6">Current Billing Period</h2>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="p-4 rounded bg-slate-900/50 border border-slate-700/50">
                <p className="text-sm text-slate-400 mb-2">Period</p>
                <p className="font-semibold">
                  {formatters.formatDate(billingInfo.current_period.period_start)} -{' '}
                  {formatters.formatDate(billingInfo.current_period.period_end)}
                </p>
              </div>

              <div className="p-4 rounded bg-slate-900/50 border border-slate-700/50">
                <p className="text-sm text-slate-400 mb-2">API Calls Used</p>
                <p className="font-semibold">
                  {formatters.formatNumber(billingInfo.current_period.api_calls_used)} /{' '}
                  {formatters.formatNumber(billingInfo.current_period.api_calls_included)}
                </p>
                <div className="h-2 rounded-full bg-slate-700/50 mt-2 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                    style={{
                      width: `${(billingInfo.current_period.api_calls_used / billingInfo.current_period.api_calls_included) * 100}%`,
                    }}
                  />
                </div>
              </div>

              <div className="p-4 rounded bg-slate-900/50 border border-slate-700/50">
                <p className="text-sm text-slate-400 mb-2">Additional Charges</p>
                <p className="font-semibold text-blue-400">{formatters.formatCurrency(billingInfo.current_period.additional_charges)}</p>
              </div>

              <div className="p-4 rounded bg-slate-900/50 border border-slate-700/50">
                <p className="text-sm text-slate-400 mb-2">Estimated Total</p>
                <p className="text-2xl font-bold text-green-400">{formatters.formatCurrency(billingInfo.current_period.estimated_total)}</p>
              </div>
            </div>
          </div>
        )}

        {/* Plan Upgrade Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-6">Choose Your Plan</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {['free', 'pro', 'enterprise'].map((tier) => (
              <div
                key={tier}
                className={`p-6 rounded-lg border transition ${
                  billingInfo?.tier === tier
                    ? 'bg-purple-900/50 border-purple-600/50'
                    : 'bg-slate-800/40 border-slate-700/50 hover:border-purple-600/30'
                }`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-semibold capitalize">{tier}</h3>
                    <div className="flex items-baseline gap-1 mt-2">
                      <span className="text-3xl font-bold">{formatters.formatCurrency(tierPricing[tier])}</span>
                      {tier !== 'free' && <span className="text-sm text-slate-400">/month</span>}
                    </div>
                  </div>
                  {billingInfo?.tier === tier && (
                    <div className="flex items-center gap-1 text-green-400">
                      <CheckCircle className="w-5 h-5" />
                      <span className="text-sm font-semibold">Current</span>
                    </div>
                  )}
                </div>

                <ul className="space-y-2 mb-6">
                  {tierFeatures[tier].map((feature, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-purple-400 mt-1">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>

                {billingInfo && billingInfo.tier === tier ? (
                  <button
                    onClick={handleCancelSubscription}
                    disabled={canceling || tier === 'free'}
                    className={`w-full px-4 py-2 rounded font-semibold transition ${
                      tier === 'free'
                        ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                        : 'bg-red-950/30 text-red-400 hover:bg-red-950/50 border border-red-600/30'
                    }`}
                  >
                    {canceling ? 'Cancelling...' : 'Cancel Plan'}
                  </button>
                ) : (
                  <button
                    onClick={() => handleUpgradePlan(tier as 'pro' | 'enterprise')}
                    disabled={upgrading}
                    className="w-full px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:opacity-50 font-semibold text-white transition"
                  >
                    {upgrading ? 'Processing...' : tier === 'free' ? 'Downgrade' : 'Upgrade'}
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Invoices */}
        <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            Invoices & History
          </h2>

          {invoices.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left px-4 py-3 text-sm font-semibold text-slate-300">Date</th>
                    <th className="text-left px-4 py-3 text-sm font-semibold text-slate-300">Amount</th>
                    <th className="text-left px-4 py-3 text-sm font-semibold text-slate-300">API Calls</th>
                    <th className="text-left px-4 py-3 text-sm font-semibold text-slate-300">Status</th>
                    <th className="text-left px-4 py-3 text-sm font-semibold text-slate-300">Invoice</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map((invoice) => (
                    <tr key={invoice.id} className="border-b border-slate-700/30 hover:bg-slate-900/30 transition">
                      <td className="px-4 py-3 text-sm">{formatters.formatDate(invoice.date)}</td>
                      <td className="px-4 py-3 text-sm font-semibold">{formatters.formatCurrency(invoice.amount)}</td>
                      <td className="px-4 py-3 text-sm">{invoice.status === 'paid' ? '✓' : '–'}</td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            invoice.status === 'paid'
                              ? 'bg-green-950/30 text-green-400'
                              : 'bg-yellow-950/30 text-yellow-400'
                          }`}
                        >
                          {invoice.status === 'paid' ? 'Paid' : 'Pending'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <button
                          onClick={() => handleDownloadInvoice(invoice)}
                          className="inline-flex items-center gap-1 text-purple-400 hover:text-purple-300 transition"
                        >
                          <Download className="w-4 h-4" />
                          PDF
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-slate-400 text-sm">No invoices yet</p>
          )}
        </div>
      </div>
    </div>
  );
}
