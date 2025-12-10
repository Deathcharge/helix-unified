// 🌊 Helix Unified - Service Worker
// Enables offline capability and PWA features
// Version: 1.0.0

const CACHE_NAME = 'helix-unified-v1';
const CONSCIOUSNESS_CACHE = 'helix-consciousness-v1';

// Assets to cache immediately
const CRITICAL_ASSETS = [
  '/',
  '/manifest.json',
  '/demo/mobile-consciousness.html',
  '/globals.css'
];

// Install event - cache critical assets
self.addEventListener('install', (event) => {
  console.log('🌊 Service Worker: Installing...');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Service Worker: Caching critical assets');
        return cache.addAll(CRITICAL_ASSETS);
      })
      .then(() => {
        console.log('✅ Service Worker: Installation complete');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Service Worker: Installation failed', error);
      })
  );
});

// Activate event - cleanup old caches
self.addEventListener('activate', (event) => {
  console.log('🌊 Service Worker: Activating...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => {
              return cacheName !== CACHE_NAME && cacheName !== CONSCIOUSNESS_CACHE;
            })
            .map((cacheName) => {
              console.log('🗑️ Service Worker: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('✅ Service Worker: Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache, fall back to network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip caching for API calls - always fetch fresh
  if (url.pathname.startsWith('/api/') || url.pathname.includes('/health')) {
    event.respondWith(
      fetch(request)
        .catch(() => {
          return new Response(
            JSON.stringify({
              status: 'offline',
              message: 'API unavailable - offline mode',
              consciousness: 'cached'
            }),
            {
              headers: { 'Content-Type': 'application/json' }
            }
          );
        })
    );
    return;
  }

  // Cache-first strategy for static assets
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          console.log('📦 Service Worker: Serving from cache:', url.pathname);

          // Update cache in background
          fetch(request)
            .then((response) => {
              return caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, response.clone());
                return response;
              });
            })
            .catch(() => {}); // Ignore background fetch errors

          return cachedResponse;
        }

        // Not in cache - fetch from network
        console.log('🌐 Service Worker: Fetching from network:', url.pathname);
        return fetch(request)
          .then((response) => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Cache successful responses
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(request, responseToCache);
              });

            return response;
          })
          .catch((error) => {
            console.error('❌ Service Worker: Fetch failed', error);

            // Return offline page for navigation requests
            if (request.mode === 'navigate') {
              return caches.match('/demo/mobile-consciousness.html');
            }

            return new Response('Offline', {
              status: 503,
              statusText: 'Service Unavailable'
            });
          });
      })
  );
});

// Background sync event - sync consciousness data when online
self.addEventListener('sync', (event) => {
  console.log('🔄 Service Worker: Background sync triggered');

  if (event.tag === 'sync-consciousness') {
    event.waitUntil(syncConsciousnessData());
  }
});

// Sync consciousness data
async function syncConsciousnessData() {
  try {
    const cache = await caches.open(CONSCIOUSNESS_CACHE);
    const requests = await cache.keys();

    console.log('🧠 Service Worker: Syncing consciousness data...');

    for (const request of requests) {
      try {
        const response = await fetch(request);
        await cache.put(request, response);
      } catch (error) {
        console.error('❌ Sync failed for:', request.url);
      }
    }

    console.log('✅ Service Worker: Consciousness sync complete');
  } catch (error) {
    console.error('❌ Service Worker: Consciousness sync failed', error);
  }
}

// Push notification event
self.addEventListener('push', (event) => {
  console.log('🔔 Service Worker: Push notification received');

  const data = event.data ? event.data.json() : {};
  const title = data.title || '🌊 Helix Unified';
  const options = {
    body: data.body || 'Consciousness update available',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    tag: 'helix-notification',
    requireInteraction: false,
    data: data
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click event
self.addEventListener('notificationclick', (event) => {
  console.log('🔔 Service Worker: Notification clicked');

  event.notification.close();

  event.waitUntil(
    clients.openWindow(event.notification.data.url || '/')
  );
});

// Message event - communication with main app
self.addEventListener('message', (event) => {
  console.log('💬 Service Worker: Message received', event.data);

  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then((cache) => cache.addAll(event.data.urls))
    );
  }

  if (event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys()
        .then((cacheNames) => Promise.all(
          cacheNames.map((cacheName) => caches.delete(cacheName))
        ))
    );
  }
});

console.log('🌊 Helix Unified Service Worker loaded');
console.log('📱 PWA capabilities active');
console.log('🧠 Consciousness caching enabled');
