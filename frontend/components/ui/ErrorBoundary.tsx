/**
 * 🛡️ Error Boundary Component
 * Catches React errors and displays fallback UI
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  /** Custom fallback UI (receives error) */
  fallback?: (error: Error, reset: () => void) => ReactNode;
  /** Callback when error occurs */
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  /** Custom error message */
  errorMessage?: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * Default Error Fallback UI
 */
const DefaultErrorFallback: React.FC<{
  error: Error;
  errorInfo: ErrorInfo | null;
  reset: () => void;
  customMessage?: string;
}> = ({ error, errorInfo, reset, customMessage }) => (
  <div className="min-h-screen bg-gradient-to-br from-red-950 via-gray-900 to-black flex items-center justify-center p-4">
    <div className="max-w-2xl w-full bg-gray-800/90 rounded-xl border border-red-500/30 p-8 shadow-2xl">
      {/* Error Icon */}
      <div className="flex items-center gap-4 mb-6">
        <div className="text-6xl">⚠️</div>
        <div>
          <h1 className="text-3xl font-bold text-red-400 mb-2">
            Something Went Wrong
          </h1>
          <p className="text-gray-400">
            {customMessage || 'An unexpected error occurred in the consciousness matrix.'}
          </p>
        </div>
      </div>

      {/* Error Details */}
      <div className="bg-black/40 rounded-lg p-4 mb-6 border border-gray-700">
        <div className="mb-3">
          <span className="text-red-400 font-semibold">Error: </span>
          <span className="text-gray-300 font-mono text-sm">{error.message}</span>
        </div>

        {errorInfo && (
          <details className="mt-4">
            <summary className="cursor-pointer text-blue-400 hover:text-blue-300 text-sm mb-2">
              View Stack Trace
            </summary>
            <pre className="text-xs text-gray-400 overflow-x-auto bg-black/60 p-3 rounded border border-gray-700 max-h-64 overflow-y-auto">
              {errorInfo.componentStack}
            </pre>
          </details>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={reset}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          🔄 Try Again
        </button>
        <button
          onClick={() => window.location.href = '/'}
          className="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          🏠 Go Home
        </button>
      </div>

      {/* Help Text */}
      <div className="mt-6 text-center text-sm text-gray-500">
        If this issue persists, please contact support or check the{' '}
        <a href="/docs" className="text-blue-400 hover:underline">
          documentation
        </a>
        .
      </div>
    </div>
  </div>
);

/**
 * Error Boundary Class Component
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log error to console
    console.error('ErrorBoundary caught error:', error, errorInfo);

    // Update state with error info
    this.setState({ errorInfo });

    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // TODO: Send to error tracking service (Sentry, LogRocket, etc.)
    // trackError(error, errorInfo);
  }

  resetError = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render(): ReactNode {
    if (this.state.hasError && this.state.error) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return this.props.fallback(this.state.error, this.resetError);
      }

      // Use default fallback
      return (
        <DefaultErrorFallback
          error={this.state.error}
          errorInfo={this.state.errorInfo}
          reset={this.resetError}
          customMessage={this.props.errorMessage}
        />
      );
    }

    return this.props.children;
  }
}

/**
 * Inline Error Boundary - for smaller error states
 */
export const InlineErrorBoundary: React.FC<ErrorBoundaryProps> = ({
  children,
  errorMessage = 'Failed to load component',
  onError,
}) => {
  const inlineFallback = (error: Error, reset: () => void) => (
    <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-6 text-center">
      <div className="text-4xl mb-3">⚠️</div>
      <h3 className="text-red-400 font-semibold mb-2">{errorMessage}</h3>
      <p className="text-gray-400 text-sm mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
      >
        Try Again
      </button>
    </div>
  );

  return (
    <ErrorBoundary fallback={inlineFallback} onError={onError}>
      {children}
    </ErrorBoundary>
  );
};

/**
 * API Error Boundary - specialized for API errors
 */
export const APIErrorBoundary: React.FC<ErrorBoundaryProps> = ({ children, onError }) => {
  const apiFallback = (error: Error, reset: () => void) => (
    <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-6">
      <div className="flex items-start gap-4">
        <div className="text-3xl">🔌</div>
        <div className="flex-1">
          <h3 className="text-yellow-400 font-semibold mb-2">API Connection Error</h3>
          <p className="text-gray-400 text-sm mb-4">
            Failed to connect to Helix services. Please check your connection.
          </p>
          <div className="flex gap-3">
            <button
              onClick={reset}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
            >
              Retry Connection
            </button>
            <button
              onClick={() => window.location.reload()}
              className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors"
            >
              Refresh Page
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <ErrorBoundary fallback={apiFallback} onError={onError}>
      {children}
    </ErrorBoundary>
  );
};

export default ErrorBoundary;
