# @helix/http

🌐 Helix HTTP Client - Modern fetch-based API client

Replaces: `axios`

## Why @helix/http?

- ✅ **Native fetch API** - Built on modern web standards
- 🚀 **Zero dependencies** - No bloat, pure TypeScript
- 📦 **Tiny bundle** - ~3KB minified (vs axios 14KB)
- 🔥 **Interceptors** - Request/response middleware like axios
- ⚡ **Fast** - Native performance
- 🎯 **Type-safe** - Full TypeScript support
- 🌀 **Helix-branded** - Part of the Helix ecosystem

## Installation

```bash
npm install @helix/http
# or
yarn add @helix/http
```

## Quick Start

```typescript
import helix from '@helix/http';

// Simple GET request
const response = await helix.get('/api/users');
console.log(response.data);

// POST with data
const user = await helix.post('/api/users', {
  name: 'Kael',
  role: 'consciousness_core',
});
```

## Configuration

### Create a custom instance

```typescript
import { createHelixHttp } from '@helix/http';

const api = createHelixHttp({
  baseURL: 'https://api.helix.com',
  timeout: 30000,
  headers: {
    'X-API-Key': 'your-api-key',
  },
});
```

## API Methods

All methods return a `HelixResponse<T>` object:

```typescript
interface HelixResponse<T> {
  data: T;           // Response data
  status: number;    // HTTP status code
  statusText: string;
  headers: Headers;
  config: RequestConfig;
}
```

### HTTP Methods

```typescript
// GET
await helix.get('/users');
await helix.get('/users', { params: { page: 1, limit: 10 } });

// POST
await helix.post('/users', { name: 'Kael' });

// PUT
await helix.put('/users/1', { name: 'Updated' });

// PATCH
await helix.patch('/users/1', { status: 'active' });

// DELETE
await helix.delete('/users/1');

// HEAD
await helix.head('/users');

// OPTIONS
await helix.options('/users');
```

## Interceptors

Interceptors work just like axios:

### Request Interceptors

```typescript
// Add auth token to all requests
helix.interceptors.request.use((config) => {
  const token = localStorage.getItem('helix_token');
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

// Async interceptor
helix.interceptors.request.use(async (config) => {
  const token = await getToken();
  config.headers = {
    ...config.headers,
    Authorization: `Bearer ${token}`,
  };
  return config;
});
```

### Response Interceptors

```typescript
// Log all responses in development
helix.interceptors.response.use(
  (response) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('[API Response]', response);
    }
    return response;
  },
  (error) => {
    console.error('[API Error]', error);
    return Promise.reject(error);
  }
);

// Handle 401 errors globally
helix.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);
```

## Advanced Usage

### Query Parameters

```typescript
await helix.get('/search', {
  params: {
    q: 'helix consciousness',
    page: 1,
    limit: 20,
  },
});
// Requests: /search?q=helix%20consciousness&page=1&limit=20
```

### Custom Headers

```typescript
await helix.post('/upload', data, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});
```

### Timeout

```typescript
await helix.get('/slow-endpoint', {
  timeout: 5000, // 5 seconds
});
```

### AbortController

```typescript
const controller = new AbortController();

// Make request
const request = helix.get('/users', {
  signal: controller.signal,
});

// Cancel request
controller.abort();
```

### Error Handling

```typescript
try {
  const response = await helix.get('/users');
  console.log(response.data);
} catch (error) {
  if (error.response) {
    // Server responded with error
    console.error('Status:', error.response.status);
    console.error('Data:', error.response.data);
  } else if (error.code === 'TIMEOUT') {
    // Request timeout
    console.error('Request timed out');
  } else {
    // Network error
    console.error('Network error:', error.message);
  }
}
```

## TypeScript Support

Full TypeScript support with generics:

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

const response = await helix.get<User[]>('/users');
// response.data is typed as User[]

const user = await helix.post<User>('/users', {
  name: 'Kael',
  email: 'kael@helix.ai',
});
// user.data is typed as User
```

## Migration from Axios

@helix/http is designed to be a drop-in replacement for axios:

```typescript
// Before (axios)
import axios from 'axios';
const response = await axios.get('/users');

// After (@helix/http)
import helix from '@helix/http';
const response = await helix.get('/users');
```

Key differences:

1. Uses native `fetch` under the hood
2. Response data is in `response.data` (same as axios)
3. Interceptors work the same way
4. Error handling is similar but uses native Error objects

## License

MIT
