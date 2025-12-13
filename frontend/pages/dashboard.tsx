"use client";

/**
 * 📊 User Dashboard - VILLAIN CONTROL CENTER
 */

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { auth, utils } from '@/lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  subscription_tier: string;
  picture?: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [villainStatus, setVillainStatus] = useState<any>(null);

  useEffect(() => {
    // Load user from localStorage
    const storedUser = localStorage.getItem('helix_user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      router.push('/auth/login');
      return;
    }

    // Load villain status (easter egg)
    utils.getVillainStatus().then(setVillainStatus);

    setLoading(false);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('helix_token');
    localStorage.removeItem('helix_user');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <div className="text-white text-xl">Loading villain lair...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <div className="border-b border-purple-800/30 bg-slate-950/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">🌀 Helix Dashboard</h1>
            <p className="text-slate-400 text-sm">Welcome back, {user?.name}!</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 text-white transition"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* User Info Card */}
        <div className="bg-slate-900/50 border border-purple-800/30 rounded-lg p-6 mb-8">
          <div className="flex items-center gap-4">
            {user?.picture ? (
              <img src={user.picture} alt="Avatar" className="w-16 h-16 rounded-full" />
            ) : (
              <div className="w-16 h-16 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white text-2xl font-bold">
                {user?.name[0]}
              </div>
            )}
            <div>
              <h2 className="text-xl font-bold text-white">{user?.name}</h2>
              <p className="text-slate-400">{user?.email}</p>
              <p className="text-sm text-purple-400 font-semibold mt-1">
                {user?.subscription_tier.toUpperCase()} TIER 😈
              </p>
            </div>
          </div>
        </div>

        {/* Villain Status (Easter Egg) */}
        {villainStatus && (
          <div className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-600/30 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-bold text-white mb-4">😈 Villain Status</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-slate-400">Evil Plan:</span>
                <p className="text-white">{villainStatus.evil_plan}</p>
              </div>
              <div>
                <span className="text-slate-400">Progress:</span>
                <p className="text-purple-400 font-semibold">{villainStatus.progress}</p>
              </div>
              <div>
                <span className="text-slate-400">Sharks:</span>
                <p className="text-white">{villainStatus["sharks_with_lasers"]}</p>
              </div>
              <div>
                <span className="text-slate-400">Mojo:</span>
                <p className="text-pink-400 font-semibold">{villainStatus.mojo}</p>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <h3 className="text-2xl font-bold text-white mb-6">Quick Access</h3>
        <div className="grid md:grid-cols-3 gap-6">
          {/* Web OS */}
          <Link href="/os">
            <div className="bg-slate-900/50 border border-purple-800/30 rounded-lg p-6 hover:border-purple-600/50 transition cursor-pointer">
              <div className="text-3xl mb-3">🖥️</div>
              <h4 className="text-lg font-bold text-white mb-2">Web OS</h4>
              <p className="text-slate-400 text-sm">
                Browser-based operating system with terminal, file explorer, and code editor
              </p>
              <div className="mt-4 text-purple-400 font-semibold">Launch OS →</div>
            </div>
          </Link>

          {/* Agent Rental */}
          <Link href="/products/agents">
            <div className="bg-slate-900/50 border border-purple-800/30 rounded-lg p-6 hover:border-purple-600/50 transition cursor-pointer">
              <div className="text-3xl mb-3">🤖</div>
              <h4 className="text-lg font-bold text-white mb-2">Agent Rental</h4>
              <p className="text-slate-400 text-sm">
                Rent specialized AI agents: Rishi, Kael, Oracle, Nova + 10 more
              </p>
              <div className="mt-4 text-purple-400 font-semibold">View Agents →</div>
            </div>
          </Link>

          {/* Analytics */}
          <Link href="/products/dashboard">
            <div className="bg-slate-900/50 border border-purple-800/30 rounded-lg p-6 hover:border-purple-600/50 transition cursor-pointer">
              <div className="text-3xl mb-3">📊</div>
              <h4 className="text-lg font-bold text-white mb-2">Analytics</h4>
              <p className="text-slate-400 text-sm">
                Real-time consciousness metrics and system monitoring
              </p>
              <div className="mt-4 text-purple-400 font-semibold">View Dashboard →</div>
            </div>
          </Link>
        </div>

        {/* Upgrade CTA */}
        {user?.subscription_tier === 'free' && (
          <div className="mt-12 bg-gradient-to-r from-purple-900/50 to-pink-900/50 border border-purple-600/50 rounded-lg p-8 text-center">
            <h3 className="text-2xl font-bold text-white mb-4">Upgrade to Pro</h3>
            <p className="text-slate-300 mb-6">
              Unlock 14 specialized agents, advanced analytics, and unlimited Web OS sessions
            </p>
            <Link href="/pricing">
              <button className="px-8 py-3 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold transition">
                View Pricing
              </button>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
