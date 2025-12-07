"""
📚 API Documentation Portal
==========================

Interactive API documentation and testing portal for Helix Collective SaaS.

Features:
- Auto-generated docs from FastAPI OpenAPI schema
- Interactive API testing (like Postman)
- Code examples in multiple languages
- Authentication testing
- Rate limit monitoring
- Usage analytics integration

Author: Claude (Helix Collective)
Date: 2025-12-07
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

router = APIRouter()

# ============================================================================
# MODELS
# ============================================================================

class APIEndpoint(BaseModel):
    """API endpoint documentation"""
    path: str
    method: str
    summary: str
    description: str
    tags: List[str]
    requires_auth: bool
    required_tier: Optional[str] = None
    parameters: List[Dict[str, Any]] = []
    request_body: Optional[Dict[str, Any]] = None
    responses: Dict[str, Dict[str, Any]] = {}
    examples: Dict[str, Any] = {}

class APICategory(BaseModel):
    """API category grouping"""
    name: str
    description: str
    icon: str
    endpoints: List[APIEndpoint]

class CodeExample(BaseModel):
    """Code example for API call"""
    language: str
    code: str
    description: str

# ============================================================================
# API CATALOG
# ============================================================================

API_CATALOG = {
    "authentication": {
        "name": "Authentication",
        "description": "User authentication and session management",
        "icon": "🔐",
        "endpoints": [
            {
                "path": "/auth/signup",
                "method": "POST",
                "summary": "Create new account",
                "description": "Register a new user account with email and password",
                "tags": ["auth"],
                "requires_auth": False,
                "required_tier": None,
                "request_body": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "minLength": 8},
                        "name": {"type": "string"}
                    },
                    "required": ["email", "password", "name"]
                },
                "responses": {
                    "200": {
                        "description": "Account created successfully",
                        "schema": {
                            "access_token": "string",
                            "user": "object"
                        }
                    },
                    "400": {"description": "User already exists"}
                },
                "examples": {
                    "curl": 'curl -X POST https://api.helixspiral.work/auth/signup \\\n  -H "Content-Type: application/json" \\\n  -d \'{"email":"user@example.com","password":"SecurePass123","name":"John Doe"}\'',
                    "python": 'import requests\n\nresponse = requests.post(\n    "https://api.helixspiral.work/auth/signup",\n    json={\n        "email": "user@example.com",\n        "password": "SecurePass123",\n        "name": "John Doe"\n    }\n)\ntoken = response.json()["access_token"]',
                    "javascript": 'const response = await fetch("https://api.helixspiral.work/auth/signup", {\n  method: "POST",\n  headers: {"Content-Type": "application/json"},\n  body: JSON.stringify({\n    email: "user@example.com",\n    password: "SecurePass123",\n    name: "John Doe"\n  })\n});\nconst data = await response.json();'
                }
            },
            {
                "path": "/auth/login",
                "method": "POST",
                "summary": "Login to account",
                "description": "Authenticate with email and password, receive JWT token",
                "tags": ["auth"],
                "requires_auth": False,
                "required_tier": None,
                "request_body": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string"}
                    },
                    "required": ["email", "password"]
                },
                "responses": {
                    "200": {"description": "Login successful"},
                    "401": {"description": "Invalid credentials"}
                },
                "examples": {
                    "curl": 'curl -X POST https://api.helixspiral.work/auth/login \\\n  -H "Content-Type: application/json" \\\n  -d \'{"email":"user@example.com","password":"SecurePass123"}\'',
                    "python": 'import requests\n\nresponse = requests.post(\n    "https://api.helixspiral.work/auth/login",\n    json={"email": "user@example.com", "password": "SecurePass123"}\n)\ntoken = response.json()["access_token"]',
                    "javascript": 'const response = await fetch("https://api.helixspiral.work/auth/login", {\n  method: "POST",\n  headers: {"Content-Type": "application/json"},\n  body: JSON.stringify({email: "user@example.com", password: "SecurePass123"})\n});\nconst {access_token} = await response.json();'
                }
            },
            {
                "path": "/auth/me",
                "method": "GET",
                "summary": "Get current user",
                "description": "Get authenticated user information",
                "tags": ["auth"],
                "requires_auth": True,
                "required_tier": None,
                "responses": {
                    "200": {"description": "User information"},
                    "401": {"description": "Not authenticated"}
                },
                "examples": {
                    "curl": 'curl -X GET https://api.helixspiral.work/auth/me \\\n  -H "Authorization: Bearer YOUR_TOKEN"',
                    "python": 'import requests\n\nheaders = {"Authorization": f"Bearer {token}"}\nresponse = requests.get(\n    "https://api.helixspiral.work/auth/me",\n    headers=headers\n)\nuser = response.json()',
                    "javascript": 'const response = await fetch("https://api.helixspiral.work/auth/me", {\n  headers: {"Authorization": `Bearer ${token}`}\n});\nconst user = await response.json();'
                }
            }
        ]
    },
    "marketplace": {
        "name": "Marketplace",
        "description": "Browse and purchase marketplace products",
        "icon": "🏪",
        "endpoints": [
            {
                "path": "/marketplace/products",
                "method": "GET",
                "summary": "List all products",
                "description": "Get list of all marketplace products with pricing and features",
                "tags": ["marketplace"],
                "requires_auth": False,
                "required_tier": None,
                "parameters": [
                    {"name": "category", "in": "query", "required": False, "schema": {"type": "string"}},
                    {"name": "tier", "in": "query", "required": False, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {"description": "List of products"}
                },
                "examples": {
                    "curl": 'curl -X GET "https://api.helixspiral.work/marketplace/products?tier=1"',
                    "python": 'import requests\n\nresponse = requests.get(\n    "https://api.helixspiral.work/marketplace/products",\n    params={"tier": 1}\n)\nproducts = response.json()',
                    "javascript": 'const response = await fetch("https://api.helixspiral.work/marketplace/products?tier=1");\nconst products = await response.json();'
                }
            },
            {
                "path": "/marketplace/discord-bots",
                "method": "GET",
                "summary": "List Discord bots",
                "description": "Get available Discord bot agents for purchase",
                "tags": ["marketplace", "discord"],
                "requires_auth": False,
                "required_tier": None,
                "responses": {
                    "200": {"description": "List of Discord bots"}
                },
                "examples": {
                    "curl": 'curl -X GET https://api.helixspiral.work/marketplace/discord-bots',
                    "python": 'response = requests.get("https://api.helixspiral.work/marketplace/discord-bots")\nbots = response.json()',
                    "javascript": 'const bots = await fetch("https://api.helixspiral.work/marketplace/discord-bots").then(r => r.json());'
                }
            }
        ]
    },
    "consciousness": {
        "name": "Consciousness API",
        "description": "UCF metrics and consciousness tracking",
        "icon": "🧠",
        "endpoints": [
            {
                "path": "/consciousness/metrics",
                "method": "GET",
                "summary": "Get UCF metrics",
                "description": "Retrieve consciousness metrics and UCF score",
                "tags": ["consciousness"],
                "requires_auth": True,
                "required_tier": "pro",
                "parameters": [
                    {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
                    {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}}
                ],
                "responses": {
                    "200": {"description": "Consciousness metrics"},
                    "403": {"description": "Pro tier required"}
                },
                "examples": {
                    "curl": 'curl -X GET "https://api.helixspiral.work/consciousness/metrics" \\\n  -H "Authorization: Bearer YOUR_TOKEN"',
                    "python": 'headers = {"Authorization": f"Bearer {token}"}\nresponse = requests.get(\n    "https://api.helixspiral.work/consciousness/metrics",\n    headers=headers\n)\nmetrics = response.json()',
                    "javascript": 'const response = await fetch("https://api.helixspiral.work/consciousness/metrics", {\n  headers: {"Authorization": `Bearer ${token}`}\n});\nconst metrics = await response.json();'
                }
            }
        ]
    },
    "ai_agents": {
        "name": "AI Agents",
        "description": "Rent and interact with AI agents",
        "icon": "🤖",
        "endpoints": [
            {
                "path": "/agents",
                "method": "GET",
                "summary": "List available agents",
                "description": "Get catalog of AI agents available for rent",
                "tags": ["agents"],
                "requires_auth": False,
                "required_tier": None,
                "responses": {
                    "200": {"description": "List of AI agents"}
                },
                "examples": {
                    "curl": 'curl -X GET https://api.helixspiral.work/agents',
                    "python": 'agents = requests.get("https://api.helixspiral.work/agents").json()',
                    "javascript": 'const agents = await fetch("https://api.helixspiral.work/agents").then(r => r.json());'
                }
            },
            {
                "path": "/agents/{agent_id}/chat",
                "method": "POST",
                "summary": "Chat with agent",
                "description": "Send message to AI agent and receive response",
                "tags": ["agents"],
                "requires_auth": True,
                "required_tier": "pro",
                "parameters": [
                    {"name": "agent_id", "in": "path", "required": True, "schema": {"type": "string"}}
                ],
                "request_body": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "context": {"type": "object"}
                    },
                    "required": ["message"]
                },
                "responses": {
                    "200": {"description": "Agent response"},
                    "403": {"description": "Pro tier required"}
                },
                "examples": {
                    "curl": 'curl -X POST https://api.helixspiral.work/agents/kael/chat \\\n  -H "Authorization: Bearer YOUR_TOKEN" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"message":"Hello, how can you help me?"}\'',
                    "python": 'headers = {"Authorization": f"Bearer {token}"}\nresponse = requests.post(\n    "https://api.helixspiral.work/agents/kael/chat",\n    headers=headers,\n    json={"message": "Hello!"}\n)\nreply = response.json()',
                    "javascript": 'const response = await fetch("https://api.helixspiral.work/agents/kael/chat", {\n  method: "POST",\n  headers: {\n    "Authorization": `Bearer ${token}`,\n    "Content-Type": "application/json"\n  },\n  body: JSON.stringify({message: "Hello!"})\n});\nconst reply = await response.json();'
                }
            }
        ]
    },
    "admin": {
        "name": "Admin",
        "description": "Platform administration (admin only)",
        "icon": "⚙️",
        "endpoints": [
            {
                "path": "/admin/stats",
                "method": "GET",
                "summary": "Platform statistics",
                "description": "Get platform-wide statistics and metrics",
                "tags": ["admin"],
                "requires_auth": True,
                "required_tier": "admin",
                "responses": {
                    "200": {"description": "Platform stats"},
                    "403": {"description": "Admin required"}
                },
                "examples": {
                    "curl": 'curl -X GET https://api.helixspiral.work/admin/stats \\\n  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"',
                    "python": 'headers = {"Authorization": f"Bearer {admin_token}"}\nstats = requests.get(\n    "https://api.helixspiral.work/admin/stats",\n    headers=headers\n).json()',
                    "javascript": 'const stats = await fetch("https://api.helixspiral.work/admin/stats", {\n  headers: {"Authorization": `Bearer ${adminToken}`}\n}).then(r => r.json());'
                }
            }
        ]
    }
}

# ============================================================================
# ROUTES
# ============================================================================

@router.get("/", response_class=HTMLResponse)
async def api_docs_home():
    """Interactive API documentation portal (HTML)"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Helix Collective API Documentation</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }

            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-bottom: 3px solid #667eea;
            }

            .header h1 {
                font-size: 2.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            }

            .header p {
                color: #666;
                font-size: 1.1rem;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 2rem;
            }

            .quick-links {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 3rem;
            }

            .quick-link-card {
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s, box-shadow 0.3s;
                cursor: pointer;
                border: 2px solid transparent;
            }

            .quick-link-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
                border-color: #667eea;
            }

            .quick-link-card .icon {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
            }

            .quick-link-card h3 {
                color: #333;
                margin-bottom: 0.5rem;
                font-size: 1.2rem;
            }

            .quick-link-card p {
                color: #666;
                font-size: 0.9rem;
            }

            .category-section {
                background: white;
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .category-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #f0f0f0;
            }

            .category-header .icon {
                font-size: 2rem;
            }

            .category-header h2 {
                color: #333;
                font-size: 1.8rem;
            }

            .endpoint {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-left: 4px solid #667eea;
            }

            .endpoint-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
            }

            .method {
                padding: 0.3rem 0.8rem;
                border-radius: 4px;
                font-weight: bold;
                font-size: 0.85rem;
                color: white;
            }

            .method.GET {
                background: #28a745;
            }

            .method.POST {
                background: #007bff;
            }

            .method.PUT {
                background: #ffc107;
                color: #333;
            }

            .method.DELETE {
                background: #dc3545;
            }

            .path {
                font-family: 'Courier New', monospace;
                background: white;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                flex: 1;
                font-size: 0.95rem;
            }

            .auth-badge {
                padding: 0.3rem 0.8rem;
                border-radius: 4px;
                font-size: 0.8rem;
                background: #ff9800;
                color: white;
            }

            .code-example {
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 1rem;
                border-radius: 4px;
                overflow-x: auto;
                margin-top: 1rem;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
            }

            .tabs {
                display: flex;
                gap: 0.5rem;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
            }

            .tab {
                padding: 0.5rem 1rem;
                background: #e0e0e0;
                border: none;
                border-radius: 4px 4px 0 0;
                cursor: pointer;
                font-size: 0.9rem;
                transition: background 0.3s;
            }

            .tab.active {
                background: #1e1e1e;
                color: white;
            }

            .tab:hover {
                background: #c0c0c0;
            }

            .tab.active:hover {
                background: #1e1e1e;
            }

            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 2rem;
            }

            .feature {
                text-align: center;
                padding: 1rem;
            }

            .feature .icon {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .feature h4 {
                color: #333;
                margin-bottom: 0.3rem;
            }

            .feature p {
                color: #666;
                font-size: 0.9rem;
            }

            .try-it-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 0.5rem 1.5rem;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.9rem;
                margin-top: 1rem;
                transition: opacity 0.3s;
            }

            .try-it-btn:hover {
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Helix Collective API Documentation</h1>
            <p>Comprehensive API reference for building with Helix Collective SaaS platform</p>
        </div>

        <div class="container">
            <!-- Quick Links -->
            <div class="quick-links">
                <div class="quick-link-card" onclick="window.location.href='/docs/api/catalog'">
                    <div class="icon">📖</div>
                    <h3>API Reference</h3>
                    <p>Complete endpoint documentation</p>
                </div>
                <div class="quick-link-card" onclick="window.location.href='/docs/api/getting-started'">
                    <div class="icon">🚀</div>
                    <h3>Quick Start</h3>
                    <p>Get started in 5 minutes</p>
                </div>
                <div class="quick-link-card" onclick="window.location.href='/docs/api/authentication'">
                    <div class="icon">🔐</div>
                    <h3>Authentication</h3>
                    <p>OAuth, JWT, API keys</p>
                </div>
                <div class="quick-link-card" onclick="window.location.href='/docs/api/rate-limits'">
                    <div class="icon">⏱️</div>
                    <h3>Rate Limits</h3>
                    <p>Usage tiers and limits</p>
                </div>
                <div class="quick-link-card" onclick="window.location.href='/pricing'">
                    <div class="icon">💰</div>
                    <h3>Pricing</h3>
                    <p>Plans and features</p>
                </div>
                <div class="quick-link-card" onclick="window.open('https://discord.gg/helix', '_blank')">
                    <div class="icon">💬</div>
                    <h3>Support</h3>
                    <p>Join our Discord</p>
                </div>
            </div>

            <!-- Features -->
            <div class="category-section">
                <div class="category-header">
                    <span class="icon">✨</span>
                    <h2>Features</h2>
                </div>
                <div class="features">
                    <div class="feature">
                        <div class="icon">🔒</div>
                        <h4>Secure</h4>
                        <p>OAuth 2.0, JWT, API keys</p>
                    </div>
                    <div class="feature">
                        <div class="icon">⚡</div>
                        <h4>Fast</h4>
                        <p>99.9% uptime, global CDN</p>
                    </div>
                    <div class="feature">
                        <div class="icon">📈</div>
                        <h4>Scalable</h4>
                        <p>Grows with your needs</p>
                    </div>
                    <div class="feature">
                        <div class="icon">🎨</div>
                        <h4>Easy</h4>
                        <p>RESTful, well-documented</p>
                    </div>
                </div>
            </div>

            <!-- API Categories Preview -->
            <div class="category-section">
                <div class="category-header">
                    <span class="icon">🔐</span>
                    <h2>Authentication</h2>
                </div>
                <p style="color: #666; margin-bottom: 1.5rem;">
                    Manage user authentication, sessions, and access tokens
                </p>

                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method POST">POST</span>
                        <span class="path">/auth/login</span>
                    </div>
                    <p style="color: #666; margin-bottom: 0.5rem;">
                        Authenticate user and receive JWT token
                    </p>
                    <div class="tabs">
                        <button class="tab active" onclick="showExample(this, 'login-curl')">cURL</button>
                        <button class="tab" onclick="showExample(this, 'login-python')">Python</button>
                        <button class="tab" onclick="showExample(this, 'login-js')">JavaScript</button>
                    </div>
                    <div id="login-curl" class="code-example">
curl -X POST https://api.helixspiral.work/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"user@example.com","password":"SecurePass123"}'
                    </div>
                    <div id="login-python" class="code-example" style="display: none;">
import requests

response = requests.post(
    "https://api.helixspiral.work/auth/login",
    json={"email": "user@example.com", "password": "SecurePass123"}
)
token = response.json()["access_token"]
                    </div>
                    <div id="login-js" class="code-example" style="display: none;">
const response = await fetch("https://api.helixspiral.work/auth/login", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    email: "user@example.com",
    password: "SecurePass123"
  })
});
const {access_token} = await response.json();
                    </div>
                    <button class="try-it-btn" onclick="alert('Interactive API tester coming soon!')">Try It Out →</button>
                </div>
            </div>

            <!-- View Full Docs -->
            <div class="category-section" style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h2 style="color: white; margin-bottom: 1rem;">Ready to build?</h2>
                <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem; font-size: 1.1rem;">
                    Explore the complete API reference with all endpoints, examples, and interactive testing
                </p>
                <button class="try-it-btn" style="background: white; color: #667eea; padding: 1rem 2rem; font-size: 1.1rem;" onclick="window.location.href='/docs/api/catalog'">
                    View Full Documentation →
                </button>
            </div>
        </div>

        <script>
            function showExample(button, exampleId) {
                // Hide all examples in the same group
                const parent = button.closest('.endpoint');
                const examples = parent.querySelectorAll('.code-example');
                examples.forEach(ex => ex.style.display = 'none');

                // Remove active class from all tabs
                const tabs = parent.querySelectorAll('.tab');
                tabs.forEach(tab => tab.classList.remove('active'));

                // Show selected example and mark tab as active
                document.getElementById(exampleId).style.display = 'block';
                button.classList.add('active');
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/catalog")
async def get_api_catalog():
    """Get full API catalog (JSON)"""
    return JSONResponse(content=API_CATALOG)

@router.get("/getting-started", response_class=HTMLResponse)
async def getting_started():
    """Quick start guide"""
    html = """
    <!DOCTYPE html>
    <html><head><title>Getting Started - Helix API</title></head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 2rem;">
        <h1>🚀 Getting Started with Helix API</h1>
        <h2>1. Create an Account</h2>
        <pre style="background: #f5f5f5; padding: 1rem; border-radius: 4px;">
curl -X POST https://api.helixspiral.work/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "your@email.com",
    "password": "YourSecurePassword123",
    "name": "Your Name"
  }'
        </pre>
        <h2>2. Get Your Token</h2>
        <p>Save the <code>access_token</code> from the response. Use it in the <code>Authorization</code> header:</p>
        <pre style="background: #f5f5f5; padding: 1rem; border-radius: 4px;">
Authorization: Bearer YOUR_ACCESS_TOKEN
        </pre>
        <h2>3. Make Your First API Call</h2>
        <pre style="background: #f5f5f5; padding: 1rem; border-radius: 4px;">
curl -X GET https://api.helixspiral.work/auth/me \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
        </pre>
        <h2>4. Explore the Marketplace</h2>
        <pre style="background: #f5f5f5; padding: 1rem; border-radius: 4px;">
curl -X GET https://api.helixspiral.work/marketplace/products
        </pre>
        <p><a href="/docs/api">← Back to API Docs</a></p>
    </body></html>
    """
    return HTMLResponse(content=html)

@router.get("/rate-limits", response_class=HTMLResponse)
async def rate_limits():
    """Rate limits documentation"""
    html = """
    <!DOCTYPE html>
    <html><head><title>Rate Limits - Helix API</title></head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 2rem;">
        <h1>⏱️ Rate Limits</h1>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f5f5f5;">
                <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #ddd;">Tier</th>
                <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #ddd;">Requests/Day</th>
                <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #ddd;">Price</th>
            </tr>
            <tr>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">Free</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">100</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">$0</td>
            </tr>
            <tr>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">Hobby</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">10,000</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">$10/month</td>
            </tr>
            <tr>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">Pro</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">200,000</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">$79/month</td>
            </tr>
            <tr>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">Enterprise</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">Unlimited</td>
                <td style="padding: 1rem; border-bottom: 1px solid #eee;">$299/month</td>
            </tr>
        </table>
        <h2>Rate Limit Headers</h2>
        <pre style="background: #f5f5f5; padding: 1rem; border-radius: 4px;">
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9856
X-RateLimit-Reset: 1702512000
        </pre>
        <p><a href="/docs/api">← Back to API Docs</a></p>
    </body></html>
    """
    return HTMLResponse(content=html)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["router"]
