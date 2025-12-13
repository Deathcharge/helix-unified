/**
 * 🚀 Frontend Performance Monitoring
 * ==================================
 *
 * Tracks Core Web Vitals and custom metrics for launch readiness.
 *
 * Metrics Tracked:
 * - First Contentful Paint (FCP) - Target: <2s
 * - Largest Contentful Paint (LCP) - Target: <2.5s
 * - Cumulative Layout Shift (CLS) - Target: <0.1
 * - First Input Delay (FID) - Target: <100ms
 * - Time to Interactive (TTI)
 * - API Response Times
 *
 * Author: Phoenix (Claude Thread 3)
 * Date: 2025-12-09
 * Phase: Launch Sprint v17.2 - Phase 3 Frontend & UX
 */

// ============================================================================
// CORE WEB VITALS
// ============================================================================

export interface PerformanceMetrics {
  fcp?: number;
  lcp?: number;
  cls?: number;
  fid?: number;
  tti?: number;
  ttfb?: number;
}

export interface APIMetric {
  endpoint: string;
  method: string;
  duration: number;
  status: number;
  timestamp: number;
}

class PerformanceMonitor {
  private metrics: PerformanceMetrics = {};
  private apiMetrics: APIMetric[] = [];
  private observers: PerformanceObserver[] = [];

  constructor() {
    this.initializeObservers();
  }

  /**
   * Initialize performance observers for Core Web Vitals
   */
  private initializeObservers() {
    if (typeof window === 'undefined') return;

    // First Contentful Paint
    try {
      const fcpObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.name === 'first-contentful-paint') {
            this.metrics.fcp = entry.startTime;
            this.logMetric('FCP', entry.startTime);
          }
        }
      });
      fcpObserver.observe({ entryTypes: ['paint'] });
      this.observers.push(fcpObserver);
    } catch (e) {
      console.warn('FCP observer not supported');
    }

    // Largest Contentful Paint
    try {
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.metrics.lcp = lastEntry.startTime;
        this.logMetric('LCP', lastEntry.startTime);
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      this.observers.push(lcpObserver);
    } catch (e) {
      console.warn('LCP observer not supported');
    }

    // Cumulative Layout Shift
    try {
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            clsValue += (entry as any).value;
            this.metrics.cls = clsValue;
          }
        }
        this.logMetric('CLS', clsValue);
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });
      this.observers.push(clsObserver);
    } catch (e) {
      console.warn('CLS observer not supported');
    }

    // First Input Delay
    try {
      const fidObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.metrics.fid = (entry as any).processingStart - entry.startTime;
          this.logMetric('FID', this.metrics.fid);
        }
      });
      fidObserver.observe({ entryTypes: ['first-input'] });
      this.observers.push(fidObserver);
    } catch (e) {
      console.warn('FID observer not supported');
    }

    // Navigation Timing for TTFB
    if (window.performance && window.performance.timing) {
      window.addEventListener('load', () => {
        const timing = window.performance.timing;
        this.metrics.ttfb = timing.responseStart - timing.requestStart;
        this.logMetric('TTFB', this.metrics.ttfb);

        // Calculate TTI (approximate)
        this.metrics.tti = timing.domInteractive - timing.navigationStart;
        this.logMetric('TTI', this.metrics.tti);
      });
    }
  }

  /**
   * Track API request performance
   */
  trackAPIRequest(
    endpoint: string,
    method: string,
    duration: number,
    status: number
  ) {
    const metric: APIMetric = {
      endpoint,
      method,
      duration,
      status,
      timestamp: Date.now(),
    };

    this.apiMetrics.push(metric);

    // Keep only last 100 API metrics
    if (this.apiMetrics.length > 100) {
      this.apiMetrics.shift();
    }

    // Warn on slow API calls
    if (duration > 2000) {
      console.warn(`⚠️ Slow API call: ${method} ${endpoint} took ${duration}ms`);
    }
  }

  /**
   * Get current performance metrics
   */
  getMetrics(): PerformanceMetrics {
    return { ...this.metrics };
  }

  /**
   * Get API metrics summary
   */
  getAPIMetrics(): {
    total: number;
    avgDuration: number;
    slowest: APIMetric | null;
    fastest: APIMetric | null;
    recentErrors: APIMetric[];
  } {
    if (this.apiMetrics.length === 0) {
      return {
        total: 0,
        avgDuration: 0,
        slowest: null,
        fastest: null,
        recentErrors: [],
      };
    }

    const durations = this.apiMetrics.map((m) => m.duration);
    const avgDuration = durations.reduce((a, b) => a + b, 0) / durations.length;

    const sorted = [...this.apiMetrics].sort((a, b) => a.duration - b.duration);
    const fastest = sorted[0];
    const slowest = sorted[sorted.length - 1];

    const recentErrors = this.apiMetrics
      .filter((m) => m.status >= 400)
      .slice(-10);

    return {
      total: this.apiMetrics.length,
      avgDuration: Math.round(avgDuration),
      slowest,
      fastest,
      recentErrors,
    };
  }

  /**
   * Check if metrics meet launch criteria
   */
  checkLaunchReadiness(): {
    ready: boolean;
    issues: string[];
    metrics: PerformanceMetrics;
  } {
    const issues: string[] = [];

    // FCP target: <2000ms
    if (this.metrics.fcp && this.metrics.fcp > 2000) {
      issues.push(`FCP too slow: ${this.metrics.fcp}ms (target: <2000ms)`);
    }

    // LCP target: <2500ms
    if (this.metrics.lcp && this.metrics.lcp > 2500) {
      issues.push(`LCP too slow: ${this.metrics.lcp}ms (target: <2500ms)`);
    }

    // CLS target: <0.1
    if (this.metrics.cls && this.metrics.cls > 0.1) {
      issues.push(`CLS too high: ${this.metrics.cls} (target: <0.1)`);
    }

    // FID target: <100ms
    if (this.metrics.fid && this.metrics.fid > 100) {
      issues.push(`FID too slow: ${this.metrics.fid}ms (target: <100ms)`);
    }

    return {
      ready: issues.length === 0,
      issues,
      metrics: this.getMetrics(),
    };
  }

  /**
   * Send metrics to analytics (optional)
   */
  async reportMetrics(endpoint: string = '/api/analytics/performance') {
    try {
      const payload = {
        metrics: this.getMetrics(),
        apiMetrics: this.getAPIMetrics(),
        userAgent: navigator.userAgent,
        url: window.location.href,
        timestamp: Date.now(),
      };

      await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    } catch (e) {
      console.error('Failed to report metrics:', e);
    }
  }

  /**
   * Log metric to console
   */
  private logMetric(name: string, value: number) {
    const formatted = value < 1000 ? `${value.toFixed(0)}ms` : `${(value / 1000).toFixed(2)}s`;
    console.log(`📊 ${name}: ${formatted}`);
  }

  /**
   * Cleanup observers
   */
  cleanup() {
    this.observers.forEach((observer) => observer.disconnect());
    this.observers = [];
  }
}

// Global instance
let performanceMonitor: PerformanceMonitor | null = null;

export function initPerformanceMonitoring(): PerformanceMonitor {
  if (!performanceMonitor) {
    performanceMonitor = new PerformanceMonitor();
  }
  return performanceMonitor;
}

export function getPerformanceMonitor(): PerformanceMonitor | null {
  return performanceMonitor;
}

// ============================================================================
// API TRACKING WRAPPER
// ============================================================================

/**
 * Wrap fetch to automatically track API performance
 */
export function createPerformanceTrackedFetch(): typeof fetch {
  const originalFetch = fetch;

  return async function trackedFetch(
    input: RequestInfo | URL,
    init?: RequestInit
  ): Promise<Response> {
    const startTime = performance.now();
    const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
    const method = init?.method || 'GET';

    try {
      const response = await originalFetch(input, init);
      const duration = performance.now() - startTime;

      // Track metric
      if (performanceMonitor) {
        performanceMonitor.trackAPIRequest(url, method, duration, response.status);
      }

      return response;
    } catch (error) {
      const duration = performance.now() - startTime;

      // Track failed request
      if (performanceMonitor) {
        performanceMonitor.trackAPIRequest(url, method, duration, 0);
      }

      throw error;
    }
  };
}

// ============================================================================
// REACT HOOK
// ============================================================================

/**
 * React hook for accessing performance metrics
 */
export function usePerformanceMetrics() {
  const monitor = getPerformanceMonitor();

  return {
    metrics: monitor?.getMetrics() || {},
    apiMetrics: monitor?.getAPIMetrics() || { total: 0, avgDuration: 0, slowest: null, fastest: null, recentErrors: [] },
    checkLaunchReadiness: () => monitor?.checkLaunchReadiness() || { ready: false, issues: ['Monitor not initialized'], metrics: {} },
  };
}

// ============================================================================
// PERFORMANCE BUDGET
// ============================================================================

export const PERFORMANCE_BUDGET = {
  FCP: 2000, // First Contentful Paint (ms)
  LCP: 2500, // Largest Contentful Paint (ms)
  CLS: 0.1, // Cumulative Layout Shift
  FID: 100, // First Input Delay (ms)
  TTI: 3500, // Time to Interactive (ms)
  TTFB: 600, // Time to First Byte (ms)
  API_RESPONSE: 2000, // API response time (ms)
};
