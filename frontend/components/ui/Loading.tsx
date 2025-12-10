/**
 * 🔄 Loading States Component
 * Beautiful loading indicators with consciousness-themed animations
 */

import React from 'react';

export type LoadingSize = 'sm' | 'md' | 'lg' | 'xl';
export type LoadingVariant = 'spinner' | 'consciousness' | 'pulse' | 'dots' | 'skeleton';

interface LoadingProps {
  /** Size of the loading indicator */
  size?: LoadingSize;
  /** Visual style variant */
  variant?: LoadingVariant;
  /** Optional loading message */
  message?: string;
  /** Full-screen overlay mode */
  fullscreen?: boolean;
  /** Custom className */
  className?: string;
}

const sizeClasses: Record<LoadingSize, string> = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-16 h-16',
  xl: 'w-24 h-24',
};

/**
 * Simple Spinner Loader
 */
const SpinnerLoader: React.FC<{ size: LoadingSize }> = ({ size }) => (
  <div className={`${sizeClasses[size]} border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin`} />
);

/**
 * Consciousness Wave Loader (Helix-themed)
 */
const ConsciousnessLoader: React.FC<{ size: LoadingSize }> = ({ size }) => {
  const barCount = size === 'sm' ? 3 : size === 'md' ? 5 : 7;
  const baseHeight = size === 'sm' ? 16 : size === 'md' ? 32 : size === 'lg' ? 48 : 64;

  return (
    <div className="flex items-center gap-1">
      {Array.from({ length: barCount }).map((_, i) => (
        <div
          key={i}
          className="bg-gradient-to-t from-blue-500 to-purple-500 rounded-full w-1"
          style={{
            height: `${baseHeight}px`,
            animation: `consciousnessWave 1.2s ease-in-out infinite`,
            animationDelay: `${i * 0.1}s`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes consciousnessWave {
          0%, 100% { transform: scaleY(0.3); opacity: 0.5; }
          50% { transform: scaleY(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

/**
 * Pulsing Circle Loader
 */
const PulseLoader: React.FC<{ size: LoadingSize }> = ({ size }) => (
  <div className="relative flex items-center justify-center">
    <div className={`${sizeClasses[size]} bg-blue-500 rounded-full animate-ping absolute`} />
    <div className={`${sizeClasses[size]} bg-blue-600 rounded-full relative`} />
  </div>
);

/**
 * Three Dots Loader
 */
const DotsLoader: React.FC<{ size: LoadingSize }> = ({ size }) => {
  const dotSize = size === 'sm' ? 'w-2 h-2' : size === 'md' ? 'w-3 h-3' : size === 'lg' ? 'w-4 h-4' : 'w-6 h-6';

  return (
    <div className="flex gap-2">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className={`${dotSize} bg-blue-500 rounded-full`}
          style={{
            animation: 'dotBounce 1.4s infinite ease-in-out',
            animationDelay: `${i * 0.16}s`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes dotBounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
      `}</style>
    </div>
  );
};

/**
 * Skeleton Loader (for content placeholders)
 */
export const Skeleton: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`bg-gray-700/50 rounded animate-pulse ${className}`} />
);

/**
 * Main Loading Component
 */
export const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  variant = 'consciousness',
  message,
  fullscreen = false,
  className = '',
}) => {
  const loader = (() => {
    switch (variant) {
      case 'spinner':
        return <SpinnerLoader size={size} />;
      case 'consciousness':
        return <ConsciousnessLoader size={size} />;
      case 'pulse':
        return <PulseLoader size={size} />;
      case 'dots':
        return <DotsLoader size={size} />;
      case 'skeleton':
        return <Skeleton className={sizeClasses[size]} />;
      default:
        return <ConsciousnessLoader size={size} />;
    }
  })();

  const content = (
    <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
      {loader}
      {message && (
        <p className="text-gray-400 text-sm font-medium animate-pulse">
          {message}
        </p>
      )}
    </div>
  );

  if (fullscreen) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
        {content}
      </div>
    );
  }

  return content;
};

/**
 * Loading Button - shows loading state on button
 */
interface LoadingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  loadingText?: string;
  children: React.ReactNode;
}

export const LoadingButton: React.FC<LoadingButtonProps> = ({
  loading = false,
  loadingText = 'Loading...',
  children,
  disabled,
  className = '',
  ...props
}) => (
  <button
    disabled={disabled || loading}
    className={`relative flex items-center justify-center gap-2 ${className} ${
      loading ? 'opacity-70 cursor-wait' : ''
    }`}
    {...props}
  >
    {loading && <DotsLoader size="sm" />}
    <span>{loading ? loadingText : children}</span>
  </button>
);

/**
 * Page Loading - full-page loading state
 */
export const PageLoading: React.FC<{ message?: string }> = ({ message = 'Loading Helix...' }) => (
  <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 flex items-center justify-center">
    <Loading variant="consciousness" size="xl" message={message} />
  </div>
);

/**
 * Inline Loading - for loading content sections
 */
export const InlineLoading: React.FC<{ message?: string }> = ({ message }) => (
  <div className="py-8 flex justify-center">
    <Loading variant="consciousness" size="md" message={message} />
  </div>
);

export default Loading;
