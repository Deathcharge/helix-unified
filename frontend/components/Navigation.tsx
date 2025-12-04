"use client";

/**
 * 🌊 Helix Unified - Main Navigation Component
 * Persistent navigation across all pages
 *
 * Usage: Import in _app.tsx or individual pages
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface NavItem {
  label: string;
  href: string;
  icon?: string;
  children?: NavItem[];
}

const navigationItems: NavItem[] = [
  {
    label: 'Home',
    href: '/',
    icon: '🌀'
  },
  {
    label: 'Dashboard',
    href: '/dashboard',
    icon: '📊'
  },
  {
    label: 'Products',
    href: '#',
    icon: '🎯',
    children: [
      { label: 'Consciousness Dashboard', href: '/products/dashboard', icon: '🧠' },
      { label: 'AI Agents', href: '/products/agents', icon: '🤖' },
      { label: 'Helix Web OS', href: '/os', icon: '🖥️' },
    ]
  },
  {
    label: 'Demos',
    href: '#',
    icon: '✨',
    children: [
      { label: 'Meme Generator', href: '/memes', icon: '🎨' },
      { label: 'Mobile Consciousness', href: '/demo/mobile-consciousness.html', icon: '📱' },
      { label: 'Demo Page', href: '/demo', icon: '🎭' },
    ]
  },
  {
    label: 'Pricing',
    href: '/pricing',
    icon: '💰'
  },
  {
    label: 'Account',
    href: '#',
    icon: '👤',
    children: [
      { label: 'Login', href: '/auth/login', icon: '🔑' },
      { label: 'Sign Up', href: '/auth/signup', icon: '✍️' },
      { label: 'Billing', href: '/settings/billing', icon: '💳' },
    ]
  }
];

export default function Navigation() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  const isActive = (href: string) => {
    if (href === '/') return router.pathname === '/';
    return router.pathname.startsWith(href);
  };

  return (
    <>
      {/* Desktop & Mobile Nav */}
      <nav className="sticky top-0 z-50 bg-slate-950/95 border-b border-purple-800/30 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link href="/">
              <a className="flex items-center space-x-2 text-xl font-bold">
                <span className="text-2xl">🌀</span>
                <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  Helix
                </span>
              </a>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-1">
              {navigationItems.map((item) => (
                <div key={item.label} className="relative group">
                  {item.children ? (
                    // Dropdown menu
                    <>
                      <button
                        onClick={() => setOpenDropdown(openDropdown === item.label ? null : item.label)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                          isActive(item.href)
                            ? 'bg-purple-600/20 text-purple-300'
                            : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                        }`}
                      >
                        {item.icon} {item.label} ▾
                      </button>
                      {openDropdown === item.label && (
                        <div className="absolute top-full left-0 mt-1 w-56 bg-slate-900 border border-purple-800/30 rounded-lg shadow-xl py-2 z-50">
                          {item.children.map((child) => (
                            <Link key={child.href} href={child.href}>
                              <a
                                className={`block px-4 py-2 text-sm transition-colors ${
                                  isActive(child.href)
                                    ? 'bg-purple-600/20 text-purple-300'
                                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                                }`}
                                onClick={() => setOpenDropdown(null)}
                              >
                                {child.icon} {child.label}
                              </a>
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    // Regular link
                    <Link href={item.href}>
                      <a
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                          isActive(item.href)
                            ? 'bg-purple-600/20 text-purple-300'
                            : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                        }`}
                      >
                        {item.icon} {item.label}
                      </a>
                    </Link>
                  )}
                </div>
              ))}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 transition"
              aria-label="Toggle menu"
            >
              {isOpen ? '✕' : '☰'}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden border-t border-purple-800/30 bg-slate-950/98 backdrop-blur-lg">
            <div className="px-4 py-4 space-y-2">
              {navigationItems.map((item) => (
                <div key={item.label}>
                  {item.children ? (
                    <>
                      <button
                        onClick={() => setOpenDropdown(openDropdown === item.label ? null : item.label)}
                        className="w-full text-left px-4 py-3 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 transition font-medium"
                      >
                        {item.icon} {item.label} {openDropdown === item.label ? '▴' : '▾'}
                      </button>
                      {openDropdown === item.label && (
                        <div className="ml-4 mt-2 space-y-1">
                          {item.children.map((child) => (
                            <Link key={child.href} href={child.href}>
                              <a
                                className={`block px-4 py-2 rounded-lg text-sm transition ${
                                  isActive(child.href)
                                    ? 'bg-purple-600/20 text-purple-300'
                                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                                }`}
                                onClick={() => {
                                  setIsOpen(false);
                                  setOpenDropdown(null);
                                }}
                              >
                                {child.icon} {child.label}
                              </a>
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <Link href={item.href}>
                      <a
                        className={`block px-4 py-3 rounded-lg transition font-medium ${
                          isActive(item.href)
                            ? 'bg-purple-600/20 text-purple-300'
                            : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                        }`}
                        onClick={() => setIsOpen(false)}
                      >
                        {item.icon} {item.label}
                      </a>
                    </Link>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* Click outside to close dropdowns */}
      {(isOpen || openDropdown) && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            setIsOpen(false);
            setOpenDropdown(null);
          }}
        />
      )}
    </>
  );
}
