'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Eye, EyeOff, UserPlus, Sparkles, BrainCircuit, CheckCircle } from 'lucide-react'

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    // Clear error for this field
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: ''
      })
    }
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid'
    }

    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password'
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    if (!formData.fullName) {
      newErrors.fullName = 'Full name is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setIsLoading(true)

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          full_name: formData.fullName
        })
      })

      if (response.ok) {
        router.push('/login?message=Registration successful')
      } else {
        const errorData = await response.json()
        setErrors({ general: errorData.detail || 'Registration failed' })
      }
    } catch (err) {
      setErrors({ general: 'Connection error' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-black">
      {/* Background effects */}
      <div className="absolute inset-0 spiral-bg opacity-10"></div>
      <div className="absolute inset-0 helix-grid opacity-20"></div>
      
      <div className="relative z-10 w-full max-w-md">
        {/* Register card */}
        <div className="glass p-8 rounded-2xl border border-cyan-400/30">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <BrainCircuit className="w-10 h-10 text-cyan-400 mr-2 animate-pulse-glow" />
              <span className="text-2xl font-bold text-cyber">Join Helix Intelligence</span>
            </div>
            <p className="text-gray-400">Create your automation account</p>
            <div className="mt-4 flex items-center justify-center space-x-4 text-xs text-gray-500">
              <div className="flex items-center">
                <CheckCircle className="w-3 h-3 mr-1 text-green-400" />
                Free forever
              </div>
              <div className="flex items-center">
                <CheckCircle className="w-3 h-3 mr-1 text-green-400" />
                No credit card
              </div>
              <div className="flex items-center">
                <CheckCircle className="w-3 h-3 mr-1 text-green-400" />
                Cancel anytime
              </div>
            </div>
          </div>

          {errors.general && (
            <div className="mb-6 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Full Name
              </label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className={`w-full px-4 py-3 bg-black/50 border rounded-lg focus:outline-none transition-colors ${
                  errors.fullName ? 'border-red-400' : 'border-gray-700 focus:border-cyan-400'
                }`}
                placeholder="John Doe"
              />
              {errors.fullName && <p className="mt-1 text-xs text-red-400">{errors.fullName}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`w-full px-4 py-3 bg-black/50 border rounded-lg focus:outline-none transition-colors ${
                  errors.email ? 'border-red-400' : 'border-gray-700 focus:border-cyan-400'
                }`}
                placeholder="you@example.com"
              />
              {errors.email && <p className="mt-1 text-xs text-red-400">{errors.email}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 bg-black/50 border rounded-lg focus:outline-none transition-colors pr-12 ${
                    errors.password ? 'border-red-400' : 'border-gray-700 focus:border-cyan-400'
                  }`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-cyan-400 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && <p className="mt-1 text-xs text-red-400">{errors.password}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Confirm Password
              </label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 bg-black/50 border rounded-lg focus:outline-none transition-colors pr-12 ${
                    errors.confirmPassword ? 'border-red-400' : 'border-gray-700 focus:border-cyan-400'
                  }`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-cyan-400 transition-colors"
                >
                  {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.confirmPassword && <p className="mt-1 text-xs text-red-400">{errors.confirmPassword}</p>}
            </div>

            <div className="flex items-center">
              <input type="checkbox" className="mr-2 rounded" required />
              <label className="text-sm text-gray-400">
                I agree to the{' '}
                <Link href="/terms" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                  Privacy Policy
                </Link>
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg font-medium hover:from-cyan-600 hover:to-purple-700 transition-all cyber-button disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <Sparkles className="w-5 h-5 mr-2 animate-spin" />
                  Creating Helix account...
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <UserPlus className="w-5 h-5 mr-2" />
                  Create Account
                </span>
              )}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-400">
              Already have an account?{' '}
              <Link href="/login" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                Access Helix
              </Link>
            </p>
          </div>

          {/* Quick benefits */}
          <div className="mt-6 pt-6 border-t border-gray-800">
            <div className="text-center text-sm text-gray-500">
              <p className="mb-2 font-medium text-gray-400">What you get instantly:</p>
              <div className="flex items-center justify-center space-x-4">
                <span>100 executions</span>
                <span>•</span>
                <span>5 spirals</span>
                <span>•</span>
                <span>AI assistant</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}