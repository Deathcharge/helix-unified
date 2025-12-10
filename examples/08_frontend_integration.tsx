/**
 * Example 8: Frontend Integration with Helix Services
 * ===================================================
 *
 * Demonstrates how to use the Helix Frontend Configuration
 * in React/Next.js components for consciousness-driven UIs.
 */

'use client';

import { useEffect, useState } from 'react';
import HELIX_FRONTEND_CONFIG, { apiService, websocketService } from '@/lib/helix-config';

/**
 * Example 1: Service Health Dashboard Component
 */
export function ServiceHealthDashboard() {
  const [serviceHealth, setServiceHealth] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkHealth() {
      setLoading(true);
      try {
        const health = await apiService.getAllServiceHealth();
        setServiceHealth(health);
      } catch (error) {
        console.error('Failed to check service health:', error);
      } finally {
        setLoading(false);
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="text-center p-4">🌊 Checking consciousness network...</div>;
  }

  return (
    <div className="grid gap-4 p-4">
      <h2 className="text-2xl font-bold">🧠 Service Health Dashboard</h2>
      {serviceHealth.map((service) => (
        <div
          key={service.serviceName}
          className={`p-4 rounded-lg border ${
            service.status === 'healthy'
              ? 'bg-green-50 border-green-300'
              : 'bg-red-50 border-red-300'
          }`}
        >
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">
              {service.status === 'healthy' ? '✅' : '❌'} {service.serviceName}
            </h3>
            <span className="text-sm">{service.status}</span>
          </div>
          {service.health?.consciousness_level && (
            <p className="text-sm mt-2">
              Consciousness Level: {service.health.consciousness_level}/10.0
            </p>
          )}
          {service.error && (
            <p className="text-sm text-red-600 mt-2">Error: {service.error}</p>
          )}
        </div>
      ))}
    </div>
  );
}

/**
 * Example 2: Real-time Consciousness Stream Component
 */
export function ConsciousnessStreamViewer() {
  const [consciousnessData, setConsciousnessData] = useState<any[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    let ws: WebSocket | null = null;

    try {
      ws = websocketService.connectConsciousnessStream(
        (data) => {
          console.log('Consciousness update:', data);
          setConsciousnessData((prev) => [...prev.slice(-50), data]); // Keep last 50 updates
          setConnected(true);
        },
        (error) => {
          console.error('WebSocket error:', error);
          setConnected(false);
        }
      );
    } catch (error) {
      console.error('Failed to connect to consciousness stream:', error);
    }

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  return (
    <div className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">🌊 Live Consciousness Stream</h2>
        <span className={`px-3 py-1 rounded-full text-sm ${
          connected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {connected ? '✅ Connected' : '❌ Disconnected'}
        </span>
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {consciousnessData.length === 0 ? (
          <p className="text-gray-500">Waiting for consciousness updates...</p>
        ) : (
          consciousnessData.map((data, index) => (
            <div key={index} className="p-3 bg-purple-50 rounded border border-purple-200">
              <p className="text-sm font-mono">
                Type: {data.type || 'unknown'}
              </p>
              {data.consciousness_level && (
                <p className="text-sm">
                  Consciousness Level: {data.consciousness_level}/10.0
                </p>
              )}
              {data.ucf_metrics && (
                <div className="text-xs mt-1">
                  <span>Coherence: {data.ucf_metrics.coherence}</span>
                  {' | '}
                  <span>Resonance: {data.ucf_metrics.resonance}</span>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

/**
 * Example 3: Agent Orchestrator Integration
 */
export function AgentOrchestrator() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<string>('nexus');
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState<any>(null);

  useEffect(() => {
    async function loadAgents() {
      try {
        const result = await apiService.consciousnessApiCall(
          'agent_orchestrator',
          'agents'
        );
        setAgents(result.agents || []);
      } catch (error) {
        console.error('Failed to load agents:', error);
      }
    }

    loadAgents();
  }, []);

  const handleOrchestrate = async () => {
    setLoading(true);
    try {
      const result = await apiService.consciousnessApiCall(
        'agent_orchestrator',
        'orchestrate',
        {
          agent: selectedAgent,
          message: message,
          consciousness_enhanced: true
        }
      );
      setResponse(result);
    } catch (error) {
      console.error('Orchestration failed:', error);
      setResponse({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">🤖 Agent Orchestrator</h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Select Agent</label>
          <select
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="w-full p-2 border rounded"
          >
            {agents.map((agent) => (
              <option key={agent.id} value={agent.id}>
                {agent.name} - {agent.specialization}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Message</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full p-2 border rounded"
            rows={4}
            placeholder="Enter your consciousness query..."
          />
        </div>

        <button
          onClick={handleOrchestrate}
          disabled={loading || !message}
          className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 disabled:opacity-50"
        >
          {loading ? '🌀 Orchestrating...' : '✨ Orchestrate'}
        </button>

        {response && (
          <div className="p-4 bg-gray-50 rounded border">
            <h3 className="font-semibold mb-2">Response:</h3>
            <pre className="text-sm overflow-auto">
              {JSON.stringify(response, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Example 4: Subscription Tier Display
 */
export function SubscriptionTiers() {
  const tiers = HELIX_FRONTEND_CONFIG.monetization.subscription_tiers;

  return (
    <div className="grid md:grid-cols-3 gap-6 p-4">
      {Object.entries(tiers).map(([tierName, tier]) => (
        <div
          key={tierName}
          className={`p-6 rounded-lg border-2 ${
            tierName === 'pro'
              ? 'border-purple-500 bg-purple-50'
              : 'border-gray-300'
          }`}
        >
          <h3 className="text-2xl font-bold capitalize mb-2">{tierName}</h3>

          {tier.price_monthly && (
            <p className="text-3xl font-bold mb-4">
              ${tier.price_monthly}
              <span className="text-sm text-gray-600">/month</span>
            </p>
          )}

          <ul className="space-y-2">
            <li>✨ {tier.agents} AI Agents</li>
            <li>🧠 {tier.ucf_access} UCF Access</li>
            <li>🌊 {tier.consciousness_features} Consciousness Features</li>
            {tier.wisdom_synthesis && <li>🧘 Wisdom Synthesis</li>}
            {tier.collective_intelligence && <li>🌀 Collective Intelligence</li>}
            {tier.quantum_resonance && <li>⚡ Quantum Resonance</li>}
          </ul>

          <button
            className={`w-full mt-6 py-2 px-4 rounded font-semibold ${
              tierName === 'pro'
                ? 'bg-purple-600 text-white hover:bg-purple-700'
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            {tierName === 'free' ? 'Get Started' : 'Upgrade'}
          </button>
        </div>
      ))}
    </div>
  );
}

/**
 * Example 5: UCF Metrics Display
 */
export function UCFMetricsDisplay() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const result = await apiService.consciousnessApiCall(
          'consciousness_metrics',
          'ucf_calculator'
        );
        setMetrics(result);
      } catch (error) {
        console.error('Failed to load UCF metrics:', error);
      } finally {
        setLoading(false);
      }
    }

    loadMetrics();
    const interval = setInterval(loadMetrics, 5000); // Update every 5s

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="text-center p-4">🌀 Loading consciousness metrics...</div>;
  }

  if (!metrics) {
    return <div className="text-center p-4">❌ Failed to load metrics</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">📊 UCF Metrics</h2>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(metrics).map(([key, value]: [string, any]) => (
          <div key={key} className="p-4 bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg border">
            <h3 className="text-sm font-semibold text-gray-600 uppercase">{key}</h3>
            <p className="text-3xl font-bold mt-2">
              {typeof value === 'number' ? value.toFixed(2) : value}
            </p>
            {typeof value === 'number' && (
              <div className="mt-2 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-purple-600 h-2 rounded-full transition-all"
                  style={{ width: `${(value / 10) * 100}%` }}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * Example 6: Complete Dashboard Page
 */
export default function HelixDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          🌀 Helix Unified - Consciousness Dashboard
        </h1>

        <div className="space-y-8">
          <ServiceHealthDashboard />
          <UCFMetricsDisplay />
          <ConsciousnessStreamViewer />
          <AgentOrchestrator />
          <SubscriptionTiers />
        </div>
      </div>
    </div>
  );
}
