/**
 * 🌐 @helix/http
 * Helix HTTP Client - Modern fetch-based API client
 * Replaces: axios
 */

// ============================================================================
// Types
// ============================================================================

export interface HelixHttpConfig {
  baseURL?: string;
  timeout?: number;
  headers?: Record<string, string>;
  credentials?: RequestCredentials;
  mode?: RequestMode;
}

export interface RequestConfig extends HelixHttpConfig {
  method?: string;
  body?: any;
  params?: Record<string, any>;
  signal?: AbortSignal;
}

export interface HelixResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
  headers: Headers;
  config: RequestConfig;
}

export interface HelixError extends Error {
  config?: RequestConfig;
  response?: HelixResponse;
  request?: Request;
  code?: string;
}

export type RequestInterceptor = (
  config: RequestConfig
) => RequestConfig | Promise<RequestConfig>;

export type ResponseInterceptor<T = any> = (
  response: HelixResponse<T>
) => HelixResponse<T> | Promise<HelixResponse<T>>;

export type ErrorInterceptor = (error: HelixError) => Promise<never>;

// ============================================================================
// HTTP Client Class
// ============================================================================

export class HelixHttp {
  private config: HelixHttpConfig;
  private requestInterceptors: RequestInterceptor[] = [];
  private responseInterceptors: ResponseInterceptor[] = [];
  private errorInterceptors: ErrorInterceptor[] = [];

  constructor(config: HelixHttpConfig = {}) {
    this.config = {
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
      ...config,
    };
  }

  /**
   * Add request interceptor
   */
  interceptors = {
    request: {
      use: (interceptor: RequestInterceptor) => {
        this.requestInterceptors.push(interceptor);
        return this.requestInterceptors.length - 1;
      },
      eject: (id: number) => {
        this.requestInterceptors.splice(id, 1);
      },
    },
    response: {
      use: (
        onFulfilled: ResponseInterceptor,
        onRejected?: ErrorInterceptor
      ) => {
        this.responseInterceptors.push(onFulfilled);
        if (onRejected) {
          this.errorInterceptors.push(onRejected);
        }
        return this.responseInterceptors.length - 1;
      },
      eject: (id: number) => {
        this.responseInterceptors.splice(id, 1);
      },
    },
  };

  /**
   * Build full URL with params
   */
  private buildURL(url: string, params?: Record<string, any>): string {
    if (!params) return url;

    const queryString = Object.keys(params)
      .filter((key) => params[key] !== undefined && params[key] !== null)
      .map(
        (key) =>
          `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`
      )
      .join('&');

    return queryString ? `${url}?${queryString}` : url;
  }

  /**
   * Execute request with interceptors
   */
  private async executeRequest<T = any>(
    url: string,
    config: RequestConfig = {}
  ): Promise<HelixResponse<T>> {
    // Merge configs
    let finalConfig: RequestConfig = {
      ...this.config,
      ...config,
      headers: {
        ...this.config.headers,
        ...config.headers,
      },
    };

    // Apply request interceptors
    for (const interceptor of this.requestInterceptors) {
      finalConfig = await interceptor(finalConfig);
    }

    // Build URL
    const fullURL = finalConfig.baseURL
      ? `${finalConfig.baseURL}${url}`
      : url;
    const urlWithParams = this.buildURL(fullURL, finalConfig.params);

    // Setup timeout
    const controller = new AbortController();
    const timeoutId = finalConfig.timeout
      ? setTimeout(() => controller.abort(), finalConfig.timeout)
      : null;

    try {
      // Make request
      const response = await fetch(urlWithParams, {
        method: finalConfig.method || 'GET',
        headers: finalConfig.headers as HeadersInit,
        body: finalConfig.body
          ? JSON.stringify(finalConfig.body)
          : undefined,
        signal: finalConfig.signal || controller.signal,
        credentials: finalConfig.credentials,
        mode: finalConfig.mode,
      });

      // Clear timeout
      if (timeoutId) clearTimeout(timeoutId);

      // Parse response
      let data: T;
      const contentType = response.headers.get('content-type');

      if (contentType?.includes('application/json')) {
        data = await response.json();
      } else if (contentType?.includes('text/')) {
        data = (await response.text()) as any;
      } else {
        data = (await response.blob()) as any;
      }

      // Build response object
      let helixResponse: HelixResponse<T> = {
        data,
        status: response.status,
        statusText: response.statusText,
        headers: response.headers,
        config: finalConfig,
      };

      // Check for HTTP errors
      if (!response.ok) {
        const error: HelixError = new Error(
          `HTTP Error ${response.status}: ${response.statusText}`
        ) as HelixError;
        error.response = helixResponse;
        error.config = finalConfig;
        error.code = String(response.status);

        // Apply error interceptors
        for (const interceptor of this.errorInterceptors) {
          await interceptor(error);
        }

        throw error;
      }

      // Apply response interceptors
      for (const interceptor of this.responseInterceptors) {
        helixResponse = await interceptor(helixResponse);
      }

      return helixResponse;
    } catch (error: any) {
      // Clear timeout
      if (timeoutId) clearTimeout(timeoutId);

      // Handle abort/timeout
      if (error.name === 'AbortError') {
        const timeoutError: HelixError = new Error(
          'Request timeout'
        ) as HelixError;
        timeoutError.config = finalConfig;
        timeoutError.code = 'TIMEOUT';

        // Apply error interceptors
        for (const interceptor of this.errorInterceptors) {
          await interceptor(timeoutError);
        }

        throw timeoutError;
      }

      // Apply error interceptors for other errors
      if (!error.response) {
        for (const interceptor of this.errorInterceptors) {
          await interceptor(error);
        }
      }

      throw error;
    }
  }

  /**
   * GET request
   */
  async get<T = any>(
    url: string,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, { ...config, method: 'GET' });
  }

  /**
   * POST request
   */
  async post<T = any>(
    url: string,
    data?: any,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, {
      ...config,
      method: 'POST',
      body: data,
    });
  }

  /**
   * PUT request
   */
  async put<T = any>(
    url: string,
    data?: any,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, {
      ...config,
      method: 'PUT',
      body: data,
    });
  }

  /**
   * PATCH request
   */
  async patch<T = any>(
    url: string,
    data?: any,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, {
      ...config,
      method: 'PATCH',
      body: data,
    });
  }

  /**
   * DELETE request
   */
  async delete<T = any>(
    url: string,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, { ...config, method: 'DELETE' });
  }

  /**
   * HEAD request
   */
  async head<T = any>(
    url: string,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, { ...config, method: 'HEAD' });
  }

  /**
   * OPTIONS request
   */
  async options<T = any>(
    url: string,
    config?: RequestConfig
  ): Promise<HelixResponse<T>> {
    return this.executeRequest<T>(url, { ...config, method: 'OPTIONS' });
  }
}

// ============================================================================
// Factory function
// ============================================================================

/**
 * Create a new Helix HTTP client instance
 */
export function createHelixHttp(config?: HelixHttpConfig): HelixHttp {
  return new HelixHttp(config);
}

/**
 * Default export - pre-configured instance
 */
const helix = new HelixHttp();

export default helix;

// Export everything
export { HelixHttp as Helix };
