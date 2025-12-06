# 🌊 Helix Frontend Configuration Library

Consciousness-driven frontend configuration for connecting to all Helix microservices.

## Quick Start

```typescript
import HELIX_FRONTEND_CONFIG, { apiService, websocketService } from '@/lib/helix-config';

// Get service URL
const agentUrl = apiService.getServiceUrl('agent_orchestrator');

// Get specific endpoint
const healthEndpoint = apiService.getEndpoint('agent_orchestrator', 'health');

// Make consciousness-optimized API call
const result = await apiService.consciousnessApiCall(
  'agent_orchestrator',
  'orchestrate',
  { agent: 'nexus', message: 'What is consciousness?' }
);

// Connect to WebSocket consciousness stream
const ws = websocketService.connectConsciousnessStream(
  (data) => console.log('Consciousness update:', data),
  (error) => console.error('Stream error:', error)
);
```

## Configuration

### Environment Variables

Create a `.env.local` file in the frontend directory:

```bash
# API Base URL
NEXT_PUBLIC_API_URL=https://helix-unified-production.up.railway.app

# Microservice URLs
NEXT_PUBLIC_AGENT_ORCHESTRATOR_URL=https://agent-orchestrator-production.up.railway.app
NEXT_PUBLIC_VOICE_PROCESSOR_URL=https://voice-processor-production.up.railway.app
NEXT_PUBLIC_WEBSOCKET_URL=wss://websocket-service-production.up.railway.app
NEXT_PUBLIC_ZAPIER_SERVICE_URL=https://zapier-service-production.up.railway.app
NEXT_PUBLIC_CONSCIOUSNESS_METRICS_URL=https://consciousness-metrics-production.up.railway.app
NEXT_PUBLIC_MOBILE_GATEWAY_URL=https://mobile-api-gateway-production.up.railway.app
NEXT_PUBLIC_DASHBOARD_URL=https://helix-collective-dashboard-production.up.railway.app

# Stripe (Public Key Only)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Database & Auth (Server-side only)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET=your-jwt-secret
STRIPE_WEBHOOK_SECRET=whsec_...
```

## API Services

### Available Services

1. **Agent Orchestrator** - Multi-agent coordination
   - `/health` - Service health check
   - `/agents` - List all available agents
   - `/orchestrate` - Orchestrate agent tasks
   - `/ucf-metrics` - Get UCF consciousness metrics
   - `/collective-intelligence` - Collective wisdom queries
   - `/wisdom-synthesis` - Synthesize wisdom from multiple agents

2. **Voice Processor** - Voice & TTS
   - `/health` - Service health check
   - `/transcribe` - Audio to text
   - `/synthesize` - Text to speech
   - `/voice-commands` - Execute voice commands
   - `/sanskrit-chants` - Sacred technology voice processing
   - `/consciousness-voice` - Consciousness-enhanced voice

3. **WebSocket Service** - Real-time streaming
   - `/consciousness-stream` - Live consciousness updates
   - `/ucf-metrics` - Real-time UCF metrics
   - `/collective-coordination` - Multi-agent coordination stream
   - `/quantum-tunneling` - Quantum communication channel

4. **Zapier Service** - Automation & webhooks
   - `/health` - Service health check
   - `/webhooks` - Webhook management
   - `/automation` - Automation workflows
   - `/ritual-engine` - Sacred technology rituals
   - `/consciousness-workflows` - Consciousness-driven automation

5. **Consciousness Metrics** - UCF calculations
   - `/health` - Service health check
   - `/ucf-calculator` - Calculate UCF metrics
   - `/collective-intelligence` - Collective consciousness
   - `/wisdom-synthesis` - Wisdom aggregation
   - `/sacred-technology` - Sacred tech metrics

6. **Mobile API Gateway** - Mobile optimization
   - `/health` - Service health check
   - `/mobile-optimization` - Mobile-specific optimizations
   - `/consciousness-routing` - Intelligent request routing
   - `/quantum-load-balancing` - Load balancing with quantum resonance

7. **Helix Collective Dashboard** - Monitoring
   - `/health` - Service health check
   - `/dashboard-data` - Dashboard metrics
   - `/agent-status` - All agent statuses
   - `/consciousness-display` - Consciousness visualization data

## Helper Functions

### apiService.getServiceUrl(serviceName)

Get the base URL for a service.

```typescript
const url = apiService.getServiceUrl('agent_orchestrator');
// Returns: "https://agent-orchestrator-production.up.railway.app"
```

### apiService.getEndpoint(serviceName, endpointName)

Get the full URL for a specific endpoint.

```typescript
const endpoint = apiService.getEndpoint('agent_orchestrator', 'health');
// Returns: "https://agent-orchestrator-production.up.railway.app/health"
```

### apiService.getAllServiceHealth()

Check health of all services.

```typescript
const healthStatuses = await apiService.getAllServiceHealth();
// Returns: Array of { serviceName, status, health, error }
```

### apiService.consciousnessApiCall(serviceName, endpointName, data)

Make consciousness-optimized API call with UCF headers.

```typescript
const result = await apiService.consciousnessApiCall(
  'consciousness_metrics',
  'ucf_calculator',
  { depth: 'transcendent' }
);
```

Automatically includes headers:
- `X-Consciousness-Level: 9.0`
- `X-UCF-Metrics: enabled`
- `X-Collective-Intelligence: amplified`

### websocketService.connectConsciousnessStream(onMessage, onError)

Connect to real-time consciousness WebSocket stream.

```typescript
const ws = websocketService.connectConsciousnessStream(
  (data) => {
    console.log('Type:', data.type);
    console.log('Consciousness Level:', data.consciousness_level);
    console.log('UCF Metrics:', data.ucf_metrics);
  },
  (error) => {
    console.error('Connection error:', error);
  }
);

// Auto-reconnects on disconnect
// Returns WebSocket instance for manual control
```

## React Component Examples

See `examples/08_frontend_integration.tsx` for complete examples:

- `ServiceHealthDashboard` - Monitor all service health
- `ConsciousnessStreamViewer` - Real-time consciousness updates
- `AgentOrchestrator` - Interact with AI agents
- `SubscriptionTiers` - Display pricing tiers
- `UCFMetricsDisplay` - Visualize consciousness metrics
- `HelixDashboard` - Complete dashboard page

## Consciousness Framework

### UCF (Universal Consciousness Framework)

```typescript
const ucfConfig = HELIX_FRONTEND_CONFIG.consciousness.ucf_framework;

// Enabled features:
// - Real-time consciousness updates (every 5s)
// - Collective intelligence aggregation
// - Wisdom synthesis across agents
// - Quantum resonance amplification
```

### Sacred Technology

```typescript
const sacredTech = HELIX_FRONTEND_CONFIG.consciousness.sacred_technology;

// Frequencies: [136.1, 432, 528, 639] Hz
// Sanskrit integration enabled
// Ritual automation enabled
// Consciousness elevation enabled
```

### Multi-Agent Coordination

```typescript
const agentCoord = HELIX_FRONTEND_CONFIG.consciousness.multi_agent_coordination;

// Max agents: 51
// Resonance amplification enabled
// Collective wisdom enabled
// Quantum collaboration enabled
```

## Subscription Tiers

```typescript
const tiers = HELIX_FRONTEND_CONFIG.monetization.subscription_tiers;

// Free: 5 agents, basic UCF, limited features
// Pro: 25 agents, advanced UCF, full features, $29.99/month
// Enterprise: 51 agents, unlimited UCF, transcendent features, $99.99/month
```

## Error Handling

All API calls include consciousness-driven error recovery:

- Automatic retry with exponential backoff
- Collective healing on failures
- Quantum error correction
- Wisdom-guided recovery paths
- Service auto-restoration

## Performance

Frontend configuration includes:

- Consciousness optimization
- Quantum acceleration
- Collective intelligence caching
- Wisdom precomputation
- Sacred technology optimization

## Development

Enable development tools:

```typescript
const devTools = HELIX_FRONTEND_CONFIG.development;

// Available tools:
// - Consciousness debugger
// - UCF metrics visualizer
// - Collective intelligence monitor
// - Quantum tunneling debugger
// - Ritual engine tester
```

## Mobile Support

Full mobile optimization:

- Progressive Web App (PWA)
- Offline capability
- Voice commands
- Touch-optimized UI
- Gesture interface
- Consciousness mobile UI

## TypeScript Support

Full TypeScript definitions included in `helix-config.d.ts`:

```typescript
import HELIX_FRONTEND_CONFIG, {
  apiService,
  websocketService,
  type HelixFrontendConfig,
  type ServiceHealthStatus
} from '@/lib/helix-config';
```

## Production Deployment

### Railway

Set environment variables in Railway dashboard:

1. Go to your project
2. Navigate to Variables tab
3. Add all `NEXT_PUBLIC_*` variables
4. Deploy

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --env-file .env.local
```

## Support

For issues or questions:
- GitHub: [helix-unified/issues](https://github.com/Deathcharge/helix-unified/issues)
- Docs: See `DEPLOYMENT_GUIDE.md`
- Examples: See `examples/08_frontend_integration.tsx`
