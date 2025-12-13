"use client";

/**
 * 🛡️ Error Boundary Component
 * Catches React errors and displays fallback UI
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  errorMessage?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('Error caught by boundary:', error, errorInfo);
    }

    // In production, send to error tracking service (e.g., Sentry)
    if (process.env.NODE_ENV === 'production') {
      // TODO: Send to Sentry or other error tracking service
      // Sentry.captureException(error, { contexts: { react: { componentStack: errorInfo.componentStack } } });
    }

    this.setState({
      error,
      errorInfo,
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 p-4">
          <div className="max-w-2xl w-full bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">⚠️</div>
              <h1 className="text-3xl font-bold text-white mb-2">
                {this.props.errorMessage || 'Oops! Something went wrong'}
              </h1>
              <p className="text-gray-300">
                {this.props.errorMessage ? 'Please try again later.' : 'We encountered an unexpected error. Don\'t worry, our team has been notified.'}
              </p>
            </div>

            {process.env.NODE_ENV === 'development' && this.state.error && (
              <div className="mt-6 p-4 bg-red-500/20 rounded-lg border border-red-500/30">
                <h2 className="text-lg font-semibold text-red-300 mb-2">
                  Error Details (Development Only)
                </h2>
                <pre className="text-sm text-red-200 overflow-auto max-h-64">
                  {this.state.error.toString()}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </div>
            )}

            <div className="mt-8 flex gap-4 justify-center">
              <button
                onClick={this.handleReset}
                className="px-6 py-3 bg-gradient-to-r from-purple-500 to-indigo-500 text-white rounded-lg font-semibold hover:from-purple-600 hover:to-indigo-600 transition-all shadow-lg"
              >
                Try Again
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="px-6 py-3 bg-white/10 text-white rounded-lg font-semibold hover:bg-white/20 transition-all border border-white/30"
              >
                Go Home
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Alias for inline error handling
export const InlineErrorBoundary = ErrorBoundary;

export default ErrorBoundary;
