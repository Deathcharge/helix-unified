/**
 * 🌀 Helix API Client
 * Unified API client for frontend
 *
 * VILLAIN COMMUNICATION MODULE 😈
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// AUTH
// ============================================================================

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  subscription_tier: string;
  created_at?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}

export const auth = {
  /**
   * Sign up with email/password
   */
  async signup(email: string, password: string, name: string): Promise<Token> {
    const response = await fetch(`${API_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Signup failed');
    }

    return response.json();
  },

  /**
   * Login with email/password
   */
  async login(email: string, password: string): Promise<Token> {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return response.json();
  },

  /**
   * Get demo account (for testing)
   */
  async demoLogin(): Promise<Token> {
    const response = await fetch(`${API_URL}/auth/demo-login`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error('Demo login failed');
    }

    return response.json();
  },

  /**
   * Get current user info
   */
  async getMe(token: string): Promise<User> {
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to get user info');
    }

    return response.json();
  },

  /**
   * Verify Google token
   */
  async verifyGoogleToken(idToken: string): Promise<Token> {
    const response = await fetch(`${API_URL}/auth/verify-google-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_token: idToken }),
    });

    if (!response.ok) {
      throw new Error('Google sign-in failed');
    }

    return response.json();
  },
};

// ============================================================================
// WEB OS
// ============================================================================

export interface FileInfo {
  name: string;
  type: 'file' | 'folder';
  path: string;
  size: number;
  created: string;
  modified: string;
  readable: boolean;
  writable: boolean;
}

export const webOS = {
  /**
   * List files in directory
   */
  async listFiles(path: string = ''): Promise<FileInfo[]> {
    const url = `${API_URL}/api/web-os/files/list${path ? '?path=' + encodeURIComponent(path) : ''}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error('Failed to list files');
    }

    const data = await response.json();
    return data.files || [];
  },

  /**
   * Read file contents
   */
  async readFile(path: string): Promise<string> {
    const url = `${API_URL}/api/web-os/files/read?path=${encodeURIComponent(path)}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error('Failed to read file');
    }

    const data = await response.json();
    return data.content || '';
  },

  /**
   * Execute terminal command
   */
  async executeCommand(command: string): Promise<{ output: string; error: string }> {
    const response = await fetch(`${API_URL}/api/web-os/terminal/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command }),
    });

    if (!response.ok) {
      throw new Error('Command execution failed');
    }

    return response.json();
  },
};

// ============================================================================
// AGENTS
// ============================================================================

export interface Agent {
  id: string;
  name: string;
  role: string;
  specialization: string;
  cost_per_call: number;
  capabilities: string[];
}

export const agents = {
  /**
   * Get agent catalog
   */
  async getCatalog(): Promise<Agent[]> {
    const response = await fetch(`${API_URL}/api/agents/catalog`);

    if (!response.ok) {
      throw new Error('Failed to get agent catalog');
    }

    const data = await response.json();
    return data.agents || [];
  },

  /**
   * Rent an agent
   */
  async rentAgent(agentId: string, userId: string): Promise<any> {
    const response = await fetch(`${API_URL}/api/agents/rent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent_id: agentId, user_id: userId }),
    });

    if (!response.ok) {
      throw new Error('Failed to rent agent');
    }

    return response.json();
  },
};

// ============================================================================
// BILLING
// ============================================================================

export const billing = {
  /**
   * Create Stripe checkout session
   */
  async createCheckout(tier: string): Promise<{ checkout_url: string }> {
    const response = await fetch(`${API_URL}/api/billing/create-checkout-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tier,
        success_url: `${window.location.origin}/dashboard?success=true`,
        cancel_url: `${window.location.origin}/pricing?canceled=true`,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to create checkout session');
    }

    return response.json();
  },
};

// ============================================================================
// UTILS
// ============================================================================

export const utils = {
  /**
   * Get villain status (easter egg)
   */
  async getVillainStatus(): Promise<any> {
    const response = await fetch(`${API_URL}/api/villain-status`);
    return response.json();
  },

  /**
   * Get system status
   */
  async getStatus(): Promise<any> {
    const response = await fetch(`${API_URL}/status`);
    return response.json();
  },
};

export default {
  auth,
  webOS,
  agents,
  billing,
  utils,
};
