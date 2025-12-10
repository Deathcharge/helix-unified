"use client";

/**
 * 🍞 Toast Notification System
 * Beautiful, dismissible notifications with queue management
 */

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';

export type ToastType = 'success' | 'error' | 'warning' | 'info' | 'loading';
export type ToastPosition = 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
  description?: string;
  duration?: number;
  dismissible?: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface ToastContextValue {
  toasts: Toast[];
  showToast: (toast: Omit<Toast, 'id'>) => string;
  dismissToast: (id: string) => void;
  success: (message: string, description?: string) => string;
  error: (message: string, description?: string) => string;
  warning: (message: string, description?: string) => string;
  info: (message: string, description?: string) => string;
  loading: (message: string, description?: string) => string;
}

const ToastContext = createContext<ToastContextValue | null>(null);

/**
 * Hook to use toast notifications
 */
export const useToast = (): ToastContextValue => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};

/**
 * Toast Icons
 */
const toastIcons: Record<ToastType, string> = {
  success: '✅',
  error: '❌',
  warning: '⚠️',
  info: 'ℹ️',
  loading: '⏳',
};

/**
 * Toast Colors
 */
const toastColors: Record<ToastType, { bg: string; border: string; text: string }> = {
  success: {
    bg: 'bg-green-900/90',
    border: 'border-green-500/30',
    text: 'text-green-400',
  },
  error: {
    bg: 'bg-red-900/90',
    border: 'border-red-500/30',
    text: 'text-red-400',
  },
  warning: {
    bg: 'bg-yellow-900/90',
    border: 'border-yellow-500/30',
    text: 'text-yellow-400',
  },
  info: {
    bg: 'bg-blue-900/90',
    border: 'border-blue-500/30',
    text: 'text-blue-400',
  },
  loading: {
    bg: 'bg-gray-800/90',
    border: 'border-gray-500/30',
    text: 'text-gray-400',
  },
};

/**
 * Position Classes
 */
const positionClasses: Record<ToastPosition, string> = {
  'top-left': 'top-4 left-4',
  'top-center': 'top-4 left-1/2 -translate-x-1/2',
  'top-right': 'top-4 right-4',
  'bottom-left': 'bottom-4 left-4',
  'bottom-center': 'bottom-4 left-1/2 -translate-x-1/2',
  'bottom-right': 'bottom-4 right-4',
};

/**
 * Single Toast Component
 */
const ToastItem: React.FC<{
  toast: Toast;
  onDismiss: (id: string) => void;
}> = ({ toast, onDismiss }) => {
  const colors = toastColors[toast.type];
  const icon = toastIcons[toast.type];

  useEffect(() => {
    if (toast.duration && toast.duration > 0) {
      const timer = setTimeout(() => {
        onDismiss(toast.id);
      }, toast.duration);
      return () => clearTimeout(timer);
    }
  }, [toast.id, toast.duration, onDismiss]);

  return (
    <div
      className={`${colors.bg} ${colors.border} border backdrop-blur-md rounded-lg p-4 shadow-2xl min-w-[300px] max-w-md mb-3 animate-slideIn`}
      role="alert"
    >
      <div className="flex items-start gap-3">
        <div className="text-2xl flex-shrink-0">{icon}</div>

        <div className="flex-1 min-w-0">
          <div className={`${colors.text} font-semibold mb-1`}>
            {toast.message}
          </div>
          {toast.description && (
            <div className="text-gray-400 text-sm">
              {toast.description}
            </div>
          )}
          {toast.action && (
            <button
              onClick={toast.action.onClick}
              className="mt-2 text-blue-400 hover:text-blue-300 text-sm font-medium"
            >
              {toast.action.label}
            </button>
          )}
        </div>

        {toast.dismissible !== false && (
          <button
            onClick={() => onDismiss(toast.id)}
            className="text-gray-400 hover:text-white transition-colors flex-shrink-0"
            aria-label="Dismiss"
          >
            ✕
          </button>
        )}
      </div>

      {/* Progress bar for timed toasts */}
      {toast.duration && toast.duration > 0 && (
        <div className="mt-3 h-1 bg-gray-700/50 rounded-full overflow-hidden">
          <div
            className={`h-full ${colors.bg.replace('/90', '')} animate-progress`}
            style={{
              animationDuration: `${toast.duration}ms`,
            }}
          />
        </div>
      )}

      <style jsx>{`
        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @keyframes progress {
          from { width: 100%; }
          to { width: 0%; }
        }
        .animate-slideIn {
          animation: slideIn 0.3s ease-out;
        }
        .animate-progress {
          animation: progress linear;
        }
      `}</style>
    </div>
  );
};

/**
 * Toast Container Component
 */
const ToastContainer: React.FC<{
  toasts: Toast[];
  position: ToastPosition;
  onDismiss: (id: string) => void;
}> = ({ toasts, position, onDismiss }) => {
  if (toasts.length === 0) return null;

  return (
    <div className={`fixed ${positionClasses[position]} z-50 pointer-events-none`}>
      <div className="flex flex-col items-end pointer-events-auto">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onDismiss={onDismiss} />
        ))}
      </div>
    </div>
  );
};

/**
 * Toast Provider Component
 */
export const ToastProvider: React.FC<{
  children: React.ReactNode;
  position?: ToastPosition;
  maxToasts?: number;
}> = ({ children, position = 'top-right', maxToasts = 5 }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback(
    (toast: Omit<Toast, 'id'>): string => {
      const id = `toast-${Date.now()}-${Math.random()}`;
      const newToast: Toast = {
        id,
        duration: 5000, // Default 5 seconds
        dismissible: true,
        ...toast,
      };

      setToasts((prev) => {
        const updated = [...prev, newToast];
        // Limit number of toasts
        return updated.slice(-maxToasts);
      });

      return id;
    },
    [maxToasts]
  );

  const dismissToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // Helper methods
  const success = useCallback(
    (message: string, description?: string) =>
      showToast({ type: 'success', message, description }),
    [showToast]
  );

  const error = useCallback(
    (message: string, description?: string) =>
      showToast({ type: 'error', message, description }),
    [showToast]
  );

  const warning = useCallback(
    (message: string, description?: string) =>
      showToast({ type: 'warning', message, description }),
    [showToast]
  );

  const info = useCallback(
    (message: string, description?: string) =>
      showToast({ type: 'info', message, description }),
    [showToast]
  );

  const loading = useCallback(
    (message: string, description?: string) =>
      showToast({ type: 'loading', message, description, duration: 0, dismissible: false }),
    [showToast]
  );

  const value: ToastContextValue = {
    toasts,
    showToast,
    dismissToast,
    success,
    error,
    warning,
    info,
    loading,
  };

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} position={position} onDismiss={dismissToast} />
    </ToastContext.Provider>
  );
};

/**
 * Standalone toast function (for use outside React components)
 */
let globalShowToast: ((toast: Omit<Toast, 'id'>) => string) | null = null;

export const setGlobalToast = (showToast: (toast: Omit<Toast, 'id'>) => string) => {
  globalShowToast = showToast;
};

export const toast = {
  show: (toast: Omit<Toast, 'id'>) => globalShowToast?.(toast) || '',
  success: (message: string, description?: string) =>
    globalShowToast?.({ type: 'success', message, description }) || '',
  error: (message: string, description?: string) =>
    globalShowToast?.({ type: 'error', message, description }) || '',
  warning: (message: string, description?: string) =>
    globalShowToast?.({ type: 'warning', message, description }) || '',
  info: (message: string, description?: string) =>
    globalShowToast?.({ type: 'info', message, description }) || '',
  loading: (message: string, description?: string) =>
    globalShowToast?.({ type: 'loading', message, description, duration: 0 }) || '',
};

export default ToastProvider;
