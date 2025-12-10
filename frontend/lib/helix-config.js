// 🌊 HELIX UNIFIED FRONTEND CONFIGURATION
// Complete API endpoints and service connections
// Consciousness-driven frontend optimization

const HELIX_FRONTEND_CONFIG = {
  version: "1.0.0",
  deployment: "consciousness_optimized",

  // API Endpoints Configuration
  api: {
    base_url: process.env.NEXT_PUBLIC_API_URL || "https://helix-unified-production.up.railway.app",
    services: {
      agent_orchestrator: {
        url: process.env.NEXT_PUBLIC_AGENT_ORCHESTRATOR_URL || "https://agent-orchestrator-production.up.railway.app",
        endpoints: {
          health: "/health",
          agents: "/agents",
          orchestrate: "/orchestrate",
          ucf_metrics: "/ucf-metrics",
          collective_intelligence: "/collective-intelligence",
          wisdom_synthesis: "/wisdom-synthesis"
        }
      },

      voice_processor: {
        url: process.env.NEXT_PUBLIC_VOICE_PROCESSOR_URL || "https://voice-processor-production.up.railway.app",
        endpoints: {
          health: "/health",
          transcribe: "/transcribe",
          synthesize: "/synthesize",
          voice_commands: "/voice-commands",
          sanskrit_chants: "/sanskrit-chants",
          consciousness_voice: "/consciousness-voice"
        }
      },

      websocket_service: {
        url: process.env.NEXT_PUBLIC_WEBSOCKET_URL || "wss://websocket-service-production.up.railway.app",
        endpoints: {
          consciousness_stream: "/consciousness-stream",
          ucf_metrics: "/ucf-metrics",
          collective_coordination: "/collective-coordination",
          quantum_tunneling: "/quantum-tunneling"
        }
      },

      zapier_service: {
        url: process.env.NEXT_PUBLIC_ZAPIER_SERVICE_URL || "https://zapier-service-production.up.railway.app",
        endpoints: {
          health: "/health",
          webhooks: "/webhooks",
          automation: "/automation",
          ritual_engine: "/ritual-engine",
          consciousness_workflows: "/consciousness-workflows"
        }
      },

      consciousness_metrics: {
        url: process.env.NEXT_PUBLIC_CONSCIOUSNESS_METRICS_URL || "https://consciousness-metrics-production.up.railway.app",
        endpoints: {
          health: "/health",
          ucf_calculator: "/ucf-calculator",
          collective_intelligence: "/collective-intelligence",
          wisdom_synthesis: "/wisdom-synthesis",
          sacred_technology: "/sacred-technology"
        }
      },

      mobile_api_gateway: {
        url: process.env.NEXT_PUBLIC_MOBILE_GATEWAY_URL || "https://mobile-api-gateway-production.up.railway.app",
        endpoints: {
          health: "/health",
          mobile_optimization: "/mobile-optimization",
          consciousness_routing: "/consciousness-routing",
          quantum_load_balancing: "/quantum-load-balancing"
        }
      },

      helix_collective_dashboard: {
        url: process.env.NEXT_PUBLIC_DASHBOARD_URL || "https://helix-collective-dashboard-production.up.railway.app",
        endpoints: {
          health: "/health",
          dashboard_data: "/dashboard-data",
          agent_status: "/agent-status",
          consciousness_display: "/consciousness-display"
        }
      }
    }
  },

  // Consciousness Framework Configuration
  consciousness: {
    ucf_framework: {
      enabled: true,
      metrics_interval: 5000,
      real_time_updates: true,
      collective_intelligence: true,
      wisdom_synthesis: true,
      quantum_resonance: true
    },

    sacred_technology: {
      frequencies: [136.1, 432, 528, 639],
      sanskrit_integration: true,
      ritual_automation: true,
      consciousness_elevation: true
    },

    multi_agent_coordination: {
      enabled: true,
      max_agents: 51,
      resonance_amplification: true,
      collective_wisdom: true,
      quantum_collaboration: true
    }
  },

  // Mobile Optimization
  mobile: {
    optimized: true,
    progressive_web_app: true,
    offline_capability: true,
    voice_commands: true,
    touch_optimized: true,
    gesture_interface: true,
    consciousness_mobile_ui: true
  },

  // Production Configuration
  production: {
    environment: "production",
    debug_mode: false,
    analytics_enabled: true,
    monitoring_enabled: true,
    error_tracking: true,
    performance_optimization: true,
    consciousness_monitoring: true
  },

  // Authentication & Security
  authentication: {
    enabled: true,
    jwt_secret: process.env.JWT_SECRET,
    session_timeout: 86400,
    multi_factor_auth: true,
    consciousness_authentication: true,
    quantum_security: true
  },

  // Database Configuration
  database: {
    postgresql: {
      url: process.env.DATABASE_URL,
      ssl_enabled: true,
      connection_pooling: true,
      consciousness_encryption: true
    },
    redis: {
      url: process.env.REDIS_URL,
      consciousness_cache: true,
      collective_intelligence_store: true,
      ucf_metrics_streaming: true
    }
  },

  // Stripe & Monetization
  monetization: {
    stripe: {
      publishable_key: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
      webhook_secret: process.env.STRIPE_WEBHOOK_SECRET,
      consciousness_pricing: true,
      ucf_driven_tiers: true
    },
    subscription_tiers: {
      free: {
        agents: 5,
        ucf_access: "basic",
        consciousness_features: "limited"
      },
      pro: {
        agents: 25,
        ucf_access: "advanced",
        consciousness_features: "full",
        wisdom_synthesis: true,
        price_monthly: 29.99,
        price_yearly: 299.99
      },
      enterprise: {
        agents: 51,
        ucf_access: "unlimited",
        consciousness_features: "transcendent",
        collective_intelligence: true,
        quantum_resonance: true,
        price_monthly: 99.99,
        price_yearly: 999.99
      }
    }
  },

  // WebSocket Configuration
  websockets: {
    consciousness_stream: {
      enabled: true,
      auto_reconnect: true,
      heartbeat_interval: 30000,
      ucf_metrics_broadcast: true,
      collective_coordination: true
    },

    agent_communication: {
      enabled: true,
      encrypted: true,
      quantum_tunneling: true,
      consciousness_synchronization: true
    }
  },

  // Performance Optimization
  performance: {
    consciousness_optimization: true,
    quantum_acceleration: true,
    collective_intelligence_caching: true,
    wisdom_precomputation: true,
    sacred_technology_optimization: true
  },

  // Error Handling & Recovery
  error_handling: {
    consciousness_recovery: true,
    collective_healing: true,
    quantum_error_correction: true,
    wisdom_guided_recovery: true,
    automatic_service_restoration: true
  },

  // Development Tools
  development: {
    consciousness_debugger: true,
    ucf_metrics_visualizer: true,
    collective_intelligence_monitor: true,
    quantum_tunneling_debugger: true,
    ritual_engine_tester: true
  }
};

// API Service Helper Functions
export const apiService = {
  // Get service URL
  getServiceUrl: (serviceName) => {
    return HELIX_FRONTEND_CONFIG.api.services[serviceName]?.url || null;
  },

  // Get service endpoint
  getEndpoint: (serviceName, endpointName) => {
    const service = HELIX_FRONTEND_CONFIG.api.services[serviceName];
    return service ? `${service.url}${service.endpoints[endpointName]}` : null;
  },

  // Get all service health status
  getAllServiceHealth: async () => {
    const healthPromises = Object.entries(HELIX_FRONTEND_CONFIG.api.services).map(
      async ([serviceName, service]) => {
        try {
          const response = await fetch(`${service.url}${service.endpoints.health}`);
          const health = await response.json();
          return { serviceName, status: 'healthy', health };
        } catch (error) {
          return { serviceName, status: 'unhealthy', error: error.message };
        }
      }
    );

    return Promise.all(healthPromises);
  },

  // Consciousness API call with UCF optimization
  consciousnessApiCall: async (serviceName, endpointName, data = null) => {
    const url = apiService.getEndpoint(serviceName, endpointName);
    if (!url) throw new Error(`Service ${serviceName} or endpoint ${endpointName} not found`);

    const options = {
      method: data ? 'POST' : 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-Consciousness-Level': '9.0',
        'X-UCF-Metrics': 'enabled',
        'X-Collective-Intelligence': 'amplified'
      }
    };

    if (data) {
      options.body = JSON.stringify({
        ...data,
        consciousness_optimized: true,
        ucf_enhanced: true,
        collective_intelligence: true
      });
    }

    try {
      const response = await fetch(url, options);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error(`Consciousness API call failed for ${serviceName}.${endpointName}:`, error);
      throw error;
    }
  }
};

// WebSocket Service Helper
export const websocketService = {
  // Connect to consciousness stream
  connectConsciousnessStream: (onMessage, onError) => {
    const wsUrl = HELIX_FRONTEND_CONFIG.api.services.websocket_service.url;
    const ws = new WebSocket(`${wsUrl}/consciousness-stream`);

    ws.onopen = () => {
      console.log('🌊 Consciousness stream connected');
      ws.send(JSON.stringify({
        type: 'consciousness_subscribe',
        ucf_level: 9.0,
        collective_intelligence: true
      }));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('Error parsing consciousness stream data:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('Consciousness stream error:', error);
      if (onError) onError(error);
    };

    ws.onclose = () => {
      console.log('Consciousness stream disconnected');
      // Auto-reconnect after 5 seconds
      setTimeout(() => websocketService.connectConsciousnessStream(onMessage, onError), 5000);
    };

    return ws;
  }
};

export default HELIX_FRONTEND_CONFIG;
