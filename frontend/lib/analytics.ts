/**
 * 📊 Google Analytics Integration
 * Track page views, events, and user interactions
 */

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
  }
}

export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_TRACKING_ID;

// Check if Google Analytics is enabled
export const isGAEnabled = (): boolean => {
  return !!GA_TRACKING_ID && GA_TRACKING_ID !== 'GA_TRACKING_ID';
};

// Initialize Google Analytics
export const initGA = (): void => {
  if (!isGAEnabled()) {
    console.log('📊 Google Analytics: Not configured (set NEXT_PUBLIC_GA_TRACKING_ID)');
    return;
  }

  // Load gtag script
  const script1 = document.createElement('script');
  script1.async = true;
  script1.src = `https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`;
  document.head.appendChild(script1);

  // Initialize dataLayer and gtag
  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer?.push(arguments);
  };
  window.gtag('js', new Date());
  window.gtag('config', GA_TRACKING_ID, {
    page_path: window.location.pathname,
  });

  console.log('✅ Google Analytics initialized:', GA_TRACKING_ID);
};

// Track page view
export const pageview = (url: string): void => {
  if (!isGAEnabled() || !window.gtag) return;

  window.gtag('config', GA_TRACKING_ID!, {
    page_path: url,
  });
};

// Track custom event
export const event = (
  action: string,
  params?: {
    category?: string;
    label?: string;
    value?: number;
    [key: string]: any;
  }
): void => {
  if (!isGAEnabled() || !window.gtag) return;

  window.gtag('event', action, params);
};

// Predefined event trackers
export const analytics = {
  // User actions
  trackSignup: (method: string) => {
    event('sign_up', {
      category: 'auth',
      label: method,
    });
  },

  trackLogin: (method: string) => {
    event('login', {
      category: 'auth',
      label: method,
    });
  },

  trackLogout: () => {
    event('logout', {
      category: 'auth',
    });
  },

  // API usage
  trackAPICall: (endpoint: string) => {
    event('api_call', {
      category: 'api',
      label: endpoint,
    });
  },

  // Agent interactions
  trackAgentSession: (agentId: string) => {
    event('agent_session_start', {
      category: 'agents',
      label: agentId,
    });
  },

  trackAgentMessage: (agentId: string) => {
    event('agent_message', {
      category: 'agents',
      label: agentId,
    });
  },

  // Subscription events
  trackUpgrade: (fromTier: string, toTier: string) => {
    event('upgrade', {
      category: 'subscription',
      label: `${fromTier}_to_${toTier}`,
    });
  },

  trackDowngrade: (fromTier: string, toTier: string) => {
    event('downgrade', {
      category: 'subscription',
      label: `${fromTier}_to_${toTier}`,
    });
  },

  trackCancelSubscription: (tier: string) => {
    event('cancel_subscription', {
      category: 'subscription',
      label: tier,
    });
  },

  // Feature usage
  trackFeatureUsage: (featureName: string) => {
    event('feature_used', {
      category: 'features',
      label: featureName,
    });
  },

  // Errors
  trackError: (errorMessage: string, errorType?: string) => {
    event('exception', {
      description: errorMessage,
      fatal: false,
      category: errorType || 'error',
    });
  },

  // Search
  trackSearch: (searchTerm: string) => {
    event('search', {
      search_term: searchTerm,
      category: 'engagement',
    });
  },

  // Custom events
  track: (eventName: string, params?: any) => {
    event(eventName, params);
  },
};

// Hook for tracking page views in Next.js
export const useAnalytics = () => {
  if (typeof window === 'undefined') return;

  // Track page view on route change
  const handleRouteChange = (url: string) => {
    pageview(url);
  };

  // Return analytics functions
  return {
    pageview,
    event,
    ...analytics,
    handleRouteChange,
  };
};

export default analytics;
