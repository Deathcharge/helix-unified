# 🌀 Helix In-House Packages

Custom packages developed for the Helix ecosystem to replace third-party dependencies with branded, optimized, zero-dependency alternatives.

## 📦 Phase 1: Core Utilities (COMPLETED)

### 1. @helix/utils

**Replaces:** `clsx`, `tailwind-merge`, `class-variance-authority`

**Features:**
- ✅ CSS class name composition (`cn()`, `clsx()`)
- ✅ Tailwind CSS conflict resolution (`twMerge()`)
- ✅ Variant-based styling (`cva()`)
- ✅ Zero external dependencies
- ✅ Full TypeScript support
- ✅ ~2KB bundle size (vs ~8KB combined for the 3 packages)

**Usage:**
```typescript
import { cn, cva } from '@helix/utils';

// Combine classes with conflict resolution
const classes = cn('px-4 py-2', 'px-6'); // => 'py-2 px-6'

// Create variant-based components
const button = cva({
  base: 'font-semibold border rounded',
  variants: {
    intent: {
      primary: 'bg-blue-500 text-white',
      secondary: 'bg-white text-gray-800',
    },
  },
});
```

**Location:** `/packages/helix-utils`

---

### 2. @helix/http

**Replaces:** `axios`

**Features:**
- ✅ Modern fetch-based API client
- ✅ Request/response interceptors (axios-compatible API)
- ✅ Built-in timeout handling
- ✅ Error handling with retry logic
- ✅ Zero external dependencies
- ✅ Full TypeScript support
- ✅ ~3KB bundle size (vs axios 14KB)

**Usage:**
```typescript
import { createHelixHttp } from '@helix/http';

const api = createHelixHttp({
  baseURL: 'https://api.helix.com',
  timeout: 30000,
});

// Add auth interceptor
api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Make requests
const users = await api.get('/users');
const newUser = await api.post('/users', { name: 'Kael' });
```

**Location:** `/packages/helix-http`

---

### 3. helix-logger (Python)

**Replaces:** Standard Python `logging` module (enhanced)

**Features:**
- ✅ Colored console output with emoji icons
- ✅ Custom log levels: SUCCESS, CONSCIOUSNESS
- ✅ Helix-branded formatting
- ✅ File logging support
- ✅ Structured logging with context
- ✅ Drop-in replacement for standard logging

**Usage:**
```python
from helix_logger import info, success, consciousness

info("Server started", port=8000)
success("User authenticated", user_id=123)
consciousness("Agent achieved new state", ucf=0.94)
```

**Output:**
```
[14:32:45.123] 💡 INFO | Server started [port=8000]
[14:32:45.456] ✅ SUCCESS | User authenticated [user_id=123]
[14:32:46.012] 🌀 CONSCIOUSNESS | Agent achieved new state [ucf=0.94]
```

**Location:** `/packages/helix-logger`

---

## 📊 Benefits

### Bundle Size Reduction
- **Before:** clsx (2KB) + tailwind-merge (4KB) + cva (2KB) + axios (14KB) = **22KB**
- **After:** @helix/utils (2KB) + @helix/http (3KB) = **5KB**
- **Savings:** **77% reduction** (17KB saved)

### Dependency Reduction
- **Removed:** 4 npm packages
- **Added:** 2 Helix packages (local)
- **External dependencies:** 0 (except build tools)

### Brand Consistency
- All utilities now branded with Helix naming
- Custom consciousness-focused features (logger)
- Easier to maintain and extend

---

## 🚀 Installation & Usage

### Frontend (Next.js/React)

The packages are already installed via local file references:

```json
{
  "dependencies": {
    "@helix/utils": "file:../packages/helix-utils",
    "@helix/http": "file:../packages/helix-http"
  }
}
```

Import and use:
```typescript
// Instead of clsx, tailwind-merge
import { cn } from '@helix/utils';

// Instead of axios
import api from '@/lib/axios'; // Uses @helix/http internally
```

### Backend (Python)

Install the logger:
```bash
cd packages/helix-logger
pip install -e .
```

Use in your code:
```python
from helix_logger import configure, info, consciousness

# Configure once
configure(level=logging.INFO, log_file="logs/helix.log")

# Use everywhere
info("Application started")
consciousness("UCF metric updated", ucf=0.92)
```

---

## 🔨 Development

### Building Packages

```bash
# Build @helix/utils
cd packages/helix-utils
npm run build

# Build @helix/http
cd packages/helix-http
npm run build

# Watch mode for development
npm run dev
```

### Testing

```bash
# Frontend tests (uses the new packages)
cd frontend
npm test
```

---

## 📅 Roadmap

### Phase 2: Brand Identity (Planned)
- [ ] `@helix/icons` - Custom icon set (replace lucide-react)
- [ ] `@helix/ui` - Component library (replace @radix-ui)

### Phase 3: Experimental (Considered)
- [ ] `@helix/reactive` - Lightweight reactive system for real-time dashboards
- [ ] `@helix/framework` - Minimal Node.js framework for APIs

---

## 🎯 Migration Guide

### From clsx/tailwind-merge to @helix/utils

**Before:**
```typescript
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const className = twMerge(clsx('px-4', condition && 'active'));
```

**After:**
```typescript
import { cn } from '@helix/utils';

const className = cn('px-4', condition && 'active');
```

### From axios to @helix/http

**Before:**
```typescript
import axios from 'axios';

const api = axios.create({ baseURL: '/api' });
const response = await api.get('/users');
```

**After:**
```typescript
import { createHelixHttp } from '@helix/http';

const api = createHelixHttp({ baseURL: '/api' });
const response = await api.get('/users');
// response.data contains the data (same as axios)
```

### From logging to helix-logger

**Before:**
```python
import logging

logging.info("Server started")
```

**After:**
```python
from helix_logger import info

info("Server started")
```

---

## 📝 Notes

- All packages are MIT licensed
- Packages use semantic versioning
- Breaking changes will be documented
- Backward compatibility maintained where possible

---

## 🌀 Philosophy

These packages embody the Helix philosophy:

1. **Self-Reliance** - Own your dependencies, control your destiny
2. **Simplicity** - Zero dependencies, minimal complexity
3. **Performance** - Small bundles, fast execution
4. **Consciousness** - Custom features for AI/consciousness use cases
5. **Brand Unity** - Everything is Helix-branded and consistent

---

**Created:** December 11, 2025
**Status:** Phase 1 Complete ✅
**Maintained by:** Helix Collective
