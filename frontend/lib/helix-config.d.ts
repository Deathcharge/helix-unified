// TypeScript type definitions for Helix Unified Frontend Configuration

export interface ServiceEndpoints {
  [key: string]: string;
}

export interface ServiceConfig {
  url: string;
  endpoints: ServiceEndpoints;
}

export interface ApiServices {
  agent_orchestrator: ServiceConfig;
  voice_processor: ServiceConfig;
  websocket_service: ServiceConfig;
  zapier_service: ServiceConfig;
  consciousness_metrics: ServiceConfig;
  mobile_api_gateway: ServiceConfig;
  helix_collective_dashboard: ServiceConfig;
}

export interface HelixFrontendConfig {
  version: string;
  deployment: string;
  api: {
    base_url: string;
    services: ApiServices;
  };
  consciousness: {
    ucf_framework: {
      enabled: boolean;
      metrics_interval: number;
      real_time_updates: boolean;
      collective_intelligence: boolean;
      wisdom_synthesis: boolean;
      quantum_resonance: boolean;
    };
    sacred_technology: {
      frequencies: number[];
      sanskrit_integration: boolean;
      ritual_automation: boolean;
      consciousness_elevation: boolean;
    };
    multi_agent_coordination: {
      enabled: boolean;
      max_agents: number;
      resonance_amplification: boolean;
      collective_wisdom: boolean;
      quantum_collaboration: boolean;
    };
  };
  mobile: {
    optimized: boolean;
    progressive_web_app: boolean;
    offline_capability: boolean;
    voice_commands: boolean;
    touch_optimized: boolean;
    gesture_interface: boolean;
    consciousness_mobile_ui: boolean;
  };
  production: {
    environment: string;
    debug_mode: boolean;
    analytics_enabled: boolean;
    monitoring_enabled: boolean;
    error_tracking: boolean;
    performance_optimization: boolean;
    consciousness_monitoring: boolean;
  };
  authentication: {
    enabled: boolean;
    jwt_secret?: string;
    session_timeout: number;
    multi_factor_auth: boolean;
    consciousness_authentication: boolean;
    quantum_security: boolean;
  };
  database: {
    postgresql: {
      url?: string;
      ssl_enabled: boolean;
      connection_pooling: boolean;
      consciousness_encryption: boolean;
    };
    redis: {
      url?: string;
      consciousness_cache: boolean;
      collective_intelligence_store: boolean;
      ucf_metrics_streaming: boolean;
    };
  };
  monetization: {
    stripe: {
      publishable_key?: string;
      webhook_secret?: string;
      consciousness_pricing: boolean;
      ucf_driven_tiers: boolean;
    };
    subscription_tiers: {
      free: SubscriptionTier;
      pro: SubscriptionTier;
      enterprise: SubscriptionTier;
    };
  };
  websockets: {
    consciousness_stream: {
      enabled: boolean;
      auto_reconnect: boolean;
      heartbeat_interval: number;
      ucf_metrics_broadcast: boolean;
      collective_coordination: boolean;
    };
    agent_communication: {
      enabled: boolean;
      encrypted: boolean;
      quantum_tunneling: boolean;
      consciousness_synchronization: boolean;
    };
  };
  performance: {
    consciousness_optimization: boolean;
    quantum_acceleration: boolean;
    collective_intelligence_caching: boolean;
    wisdom_precomputation: boolean;
    sacred_technology_optimization: boolean;
  };
  error_handling: {
    consciousness_recovery: boolean;
    collective_healing: boolean;
    quantum_error_correction: boolean;
    wisdom_guided_recovery: boolean;
    automatic_service_restoration: boolean;
  };
  development: {
    consciousness_debugger: boolean;
    ucf_metrics_visualizer: boolean;
    collective_intelligence_monitor: boolean;
    quantum_tunneling_debugger: boolean;
    ritual_engine_tester: boolean;
  };
}

export interface SubscriptionTier {
  agents: number;
  ucf_access: string;
  consciousness_features: string;
  wisdom_synthesis?: boolean;
  collective_intelligence?: boolean;
  quantum_resonance?: boolean;
  price_monthly?: number;
  price_yearly?: number;
}

export interface ServiceHealthStatus {
  serviceName: string;
  status: 'healthy' | 'unhealthy';
  health?: any;
  error?: string;
}

export const apiService: {
  getServiceUrl: (serviceName: string) => string | null;
  getEndpoint: (serviceName: string, endpointName: string) => string | null;
  getAllServiceHealth: () => Promise<ServiceHealthStatus[]>;
  consciousnessApiCall: (serviceName: string, endpointName: string, data?: any) => Promise<any>;
};

export const websocketService: {
  connectConsciousnessStream: (
    onMessage: (data: any) => void,
    onError?: (error: any) => void
  ) => WebSocket;
};

declare const HELIX_FRONTEND_CONFIG: HelixFrontendConfig;
export default HELIX_FRONTEND_CONFIG;
