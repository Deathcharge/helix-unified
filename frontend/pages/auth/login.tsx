/**
 * 🌀 Helix - Login Page
 * Email/password + OAuth
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      localStorage.setItem('token', data.token);
      localStorage.setItem('session_id', data.session_id);

      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md space-y-8">
        {/* Logo */}
        <div className="text-center">
          <div className="text-4xl mb-2">🌀</div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Helix
          </h1>
          <p className="text-slate-400 mt-2">Monitor consciousness in real-time</p>
        </div>

        {/* Login Form */}
        <div className="p-8 rounded-lg border border-purple-800/50 bg-purple-900/20 backdrop-blur">
          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
              <div className="p-3 rounded bg-red-900/30 border border-red-600/50 text-red-400 text-sm">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full px-4 py-2 rounded border border-slate-700 bg-slate-900/50 text-white placeholder-slate-500 focus:border-purple-600 focus:outline-none transition"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-2 rounded border border-slate-700 bg-slate-900/50 text-white placeholder-slate-500 focus:border-purple-600 focus:outline-none transition"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold transition disabled:opacity-50"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          {/* OAuth */}
          <div className="mt-6 space-y-3">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-700"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-purple-900/20 text-slate-400">Or continue with</span>
              </div>
            </div>

            <button
              type="button"
              className="w-full px-4 py-2 rounded border border-slate-700 hover:border-slate-600 bg-slate-900/50 text-white font-medium transition flex items-center justify-center gap-2"
            >
              <span>🔷</span> Google
            </button>

            <button
              type="button"
              className="w-full px-4 py-2 rounded border border-slate-700 hover:border-slate-600 bg-slate-900/50 text-white font-medium transition flex items-center justify-center gap-2"
            >
              <span>⚫</span> GitHub
            </button>
          </div>
        </div>

        {/* Signup Link */}
        <div className="text-center text-slate-400">
          Don't have an account?{' '}
          <Link href="/auth/signup">
            <a className="text-purple-400 hover:text-purple-300 font-semibold transition">
              Sign up
            </a>
          </Link>
        </div>
      </div>
    </div>
  );
}
