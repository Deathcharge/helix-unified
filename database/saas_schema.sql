-- ============================================================================
-- Helix Collective SaaS Platform - Complete Database Schema
-- ============================================================================
-- Version: 1.0.0
-- Date: 2025-11-30
-- Purpose: Multi-tenant SaaS infrastructure with usage tracking
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- USERS & AUTHENTICATION
-- ============================================================================

-- Users table (multi-tenant)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255),
    company VARCHAR(255),

    -- Subscription
    tier VARCHAR(50) DEFAULT 'free' CHECK (tier IN ('free', 'pro', 'enterprise', 'workflow')),
    stripe_customer_id VARCHAR(255) UNIQUE,
    stripe_subscription_id VARCHAR(255),
    subscription_status VARCHAR(50) DEFAULT 'inactive' CHECK (subscription_status IN ('active', 'inactive', 'trialing', 'past_due', 'canceled')),
    trial_ends_at TIMESTAMP,

    -- Limits (tier-based)
    requests_per_day INTEGER DEFAULT 100,
    agents_allowed INTEGER DEFAULT 3,
    prompts_allowed INTEGER DEFAULT 10,

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token TEXT,

    -- Analytics
    total_requests INTEGER DEFAULT 0,
    total_spent_usd DECIMAL(10, 4) DEFAULT 0.00
);

-- API Keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Key data
    key_hash TEXT UNIQUE NOT NULL,  -- Store bcrypt hash, never plaintext
    key_prefix VARCHAR(20) NOT NULL,  -- e.g., "hx_user_abc..." (for display)
    name VARCHAR(255) DEFAULT 'Default API Key',

    -- Permissions
    scopes TEXT[] DEFAULT ARRAY['chat', 'agents', 'prompts']::TEXT[],

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMP,
    requests_count INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,

    CONSTRAINT unique_user_key_name UNIQUE (user_id, name)
);

-- Sessions table (JWT tokens)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    token_hash TEXT UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,

    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP
);

-- ============================================================================
-- SUBSCRIPTIONS & BILLING
-- ============================================================================

-- Subscription plans
CREATE TABLE subscription_plans (
    id VARCHAR(50) PRIMARY KEY,  -- e.g., 'free', 'pro', 'enterprise'
    name VARCHAR(100) NOT NULL,
    description TEXT,

    -- Pricing
    price_monthly_usd DECIMAL(10, 2) NOT NULL,
    price_yearly_usd DECIMAL(10, 2),
    stripe_price_id VARCHAR(255),

    -- Limits
    requests_per_day INTEGER NOT NULL,
    agents_allowed INTEGER NOT NULL,
    prompts_allowed INTEGER NOT NULL,
    workflows_allowed INTEGER DEFAULT 0,
    team_members_allowed INTEGER DEFAULT 1,

    -- Features (JSONB for flexibility)
    features JSONB DEFAULT '{}',

    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Payment history
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Stripe data
    stripe_payment_id VARCHAR(255) UNIQUE,
    stripe_invoice_id VARCHAR(255),

    -- Payment details
    amount_usd DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50) NOT NULL,  -- 'succeeded', 'pending', 'failed'

    -- Metadata
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- USAGE TRACKING & ANALYTICS
-- ============================================================================

-- API usage tracking (per request)
CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    api_key_id UUID REFERENCES api_keys(id) ON DELETE SET NULL,

    -- Request details
    endpoint VARCHAR(255) NOT NULL,  -- e.g., '/v1/chat', '/v1/agents/kael/execute'
    method VARCHAR(10) NOT NULL,  -- GET, POST, etc.

    -- LLM details
    provider VARCHAR(50),  -- 'anthropic', 'openai', 'xai', 'perplexity'
    model VARCHAR(100),  -- 'claude-3-opus-20240229', 'gpt-4', etc.

    -- Token usage
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    tokens_total INTEGER DEFAULT 0,

    -- Cost calculation
    cost_usd DECIMAL(10, 6) DEFAULT 0.000000,

    -- Performance
    response_time_ms INTEGER,
    status_code INTEGER,

    -- Metadata
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Daily usage aggregates (for performance)
CREATE TABLE daily_usage_summary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,

    -- Aggregates
    total_requests INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    total_cost_usd DECIMAL(10, 4) DEFAULT 0.0000,

    -- By provider
    anthropic_requests INTEGER DEFAULT 0,
    openai_requests INTEGER DEFAULT 0,
    xai_requests INTEGER DEFAULT 0,
    perplexity_requests INTEGER DEFAULT 0,

    -- By endpoint
    chat_requests INTEGER DEFAULT 0,
    agent_requests INTEGER DEFAULT 0,
    prompt_requests INTEGER DEFAULT 0,
    workflow_requests INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_user_date UNIQUE (user_id, date)
);

-- ============================================================================
-- MULTI-LLM ROUTING
-- ============================================================================

-- LLM provider configs
CREATE TABLE llm_providers (
    id VARCHAR(50) PRIMARY KEY,  -- 'anthropic', 'openai', 'xai', 'perplexity'
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    -- Pricing (per 1M tokens)
    price_input_per_1m DECIMAL(10, 2),
    price_output_per_1m DECIMAL(10, 2),

    -- Performance stats
    avg_response_time_ms INTEGER,
    uptime_percentage DECIMAL(5, 2),

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Model configs
CREATE TABLE llm_models (
    id VARCHAR(100) PRIMARY KEY,  -- 'claude-3-opus-20240229'
    provider_id VARCHAR(50) NOT NULL REFERENCES llm_providers(id),
    name VARCHAR(100) NOT NULL,

    -- Capabilities
    context_window INTEGER NOT NULL,
    max_output_tokens INTEGER,
    supports_streaming BOOLEAN DEFAULT TRUE,

    -- Pricing
    price_input_per_1m DECIMAL(10, 2) NOT NULL,
    price_output_per_1m DECIMAL(10, 2) NOT NULL,

    -- Routing weights
    cost_score INTEGER DEFAULT 50,  -- 0-100 (lower = cheaper)
    speed_score INTEGER DEFAULT 50,  -- 0-100 (higher = faster)
    quality_score INTEGER DEFAULT 50,  -- 0-100 (higher = better)

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    tier_restriction VARCHAR(50),  -- NULL = all tiers, 'pro', 'enterprise'

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- PROMPTS & VERSIONING
-- ============================================================================

-- Saved prompts
CREATE TABLE prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Prompt data
    name VARCHAR(255) NOT NULL,
    description TEXT,
    template TEXT NOT NULL,
    variables JSONB DEFAULT '[]',  -- e.g., [{"name": "product", "type": "string"}]

    -- Settings
    model_preference VARCHAR(100),  -- Specific model or NULL for auto-route
    optimize_mode VARCHAR(20) DEFAULT 'cost',  -- 'cost', 'speed', 'quality'
    temperature DECIMAL(3, 2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,

    -- Organization
    tags TEXT[] DEFAULT '{}',
    folder VARCHAR(255),
    is_public BOOLEAN DEFAULT FALSE,

    -- Versioning
    version INTEGER DEFAULT 1,
    parent_id UUID REFERENCES prompts(id),  -- For version history

    -- Analytics
    execution_count INTEGER DEFAULT 0,
    avg_cost_usd DECIMAL(10, 6),
    avg_quality_score DECIMAL(3, 2),

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_user_prompt_name UNIQUE (user_id, name, version)
);

-- Prompt executions (track performance)
CREATE TABLE prompt_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prompt_id UUID NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Execution details
    input_variables JSONB,
    model_used VARCHAR(100),
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 6),
    response_time_ms INTEGER,

    -- Quality feedback (optional)
    quality_score INTEGER CHECK (quality_score BETWEEN 1 AND 5),
    feedback TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- AI AGENTS
-- ============================================================================

-- Agent registry
CREATE TABLE agents (
    id VARCHAR(50) PRIMARY KEY,  -- 'kael', 'oracle', 'lumina', etc.
    name VARCHAR(100) NOT NULL,
    description TEXT,

    -- Capabilities
    specialization VARCHAR(255),  -- 'Code & Documentation', 'Analysis', etc.
    system_prompt TEXT NOT NULL,
    model_preference VARCHAR(100),

    -- Availability by tier
    tier_restriction VARCHAR(50),  -- NULL = all tiers

    -- Analytics
    execution_count INTEGER DEFAULT 0,
    avg_execution_time_ms INTEGER,
    avg_cost_usd DECIMAL(10, 6),
    avg_quality_score DECIMAL(3, 2),

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Agent executions
CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL REFERENCES agents(id),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Execution details
    task_type VARCHAR(100),  -- 'document', 'analyze', 'research', etc.
    input_data JSONB NOT NULL,
    output_data JSONB,

    -- LLM details
    model_used VARCHAR(100),
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 6),
    response_time_ms INTEGER,

    -- Status
    status VARCHAR(50) NOT NULL,  -- 'success', 'error', 'timeout'
    error_message TEXT,

    -- Quality feedback
    quality_score INTEGER CHECK (quality_score BETWEEN 1 AND 5),
    feedback TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- WORKFLOWS (Zapier MCP Integration)
-- ============================================================================

-- Workflow definitions
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Workflow data
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Trigger configuration
    trigger_type VARCHAR(100) NOT NULL,  -- 'webhook', 'schedule', 'email', 'zapier'
    trigger_config JSONB NOT NULL,

    -- Steps (array of actions)
    steps JSONB NOT NULL,  -- [{"type": "agent", "agent_id": "kael", "config": {...}}, {"type": "zapier", "zap_id": "..."}]

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    execution_count INTEGER DEFAULT 0,
    last_execution_at TIMESTAMP,

    -- Error handling
    on_error VARCHAR(50) DEFAULT 'stop',  -- 'stop', 'continue', 'retry'
    max_retries INTEGER DEFAULT 3,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_user_workflow_name UNIQUE (user_id, name)
);

-- Workflow executions
CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Execution details
    trigger_data JSONB,
    steps_completed INTEGER DEFAULT 0,
    steps_total INTEGER NOT NULL,

    -- Results
    status VARCHAR(50) NOT NULL,  -- 'running', 'success', 'error', 'timeout'
    output_data JSONB,
    error_message TEXT,

    -- Performance
    total_time_ms INTEGER,
    total_cost_usd DECIMAL(10, 6),

    -- Timestamps
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Zapier integration
CREATE TABLE zapier_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Zapier OAuth
    zapier_access_token TEXT,  -- Encrypted
    zapier_refresh_token TEXT,  -- Encrypted
    zapier_account_id VARCHAR(255),

    -- Connected Zaps
    zaps JSONB DEFAULT '[]',  -- [{"id": "...", "name": "...", "enabled": true}]

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- RATE LIMITING
-- ============================================================================

-- Rate limit tracking (Redis is primary, this is backup/analytics)
CREATE TABLE rate_limits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Window
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,

    -- Counts
    requests_count INTEGER DEFAULT 0,
    limit_exceeded_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_user_window UNIQUE (user_id, window_start)
);

-- ============================================================================
-- TEAM MANAGEMENT (Enterprise)
-- ============================================================================

-- Teams
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,

    -- Subscription (team-wide)
    tier VARCHAR(50) DEFAULT 'enterprise',
    stripe_subscription_id VARCHAR(255),

    -- Limits
    max_members INTEGER DEFAULT 10,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Team members
CREATE TABLE team_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    role VARCHAR(50) DEFAULT 'member',  -- 'owner', 'admin', 'member', 'viewer'

    -- Permissions
    can_manage_billing BOOLEAN DEFAULT FALSE,
    can_invite_members BOOLEAN DEFAULT FALSE,
    can_create_workflows BOOLEAN DEFAULT TRUE,

    joined_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_team_user UNIQUE (team_id, user_id)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe_customer_id ON users(stripe_customer_id);
CREATE INDEX idx_users_tier ON users(tier);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- API Keys
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);

-- API Usage
CREATE INDEX idx_api_usage_user_id ON api_usage(user_id);
CREATE INDEX idx_api_usage_created_at ON api_usage(created_at DESC);
CREATE INDEX idx_api_usage_endpoint ON api_usage(endpoint);
CREATE INDEX idx_api_usage_user_date ON api_usage(user_id, created_at);

-- Daily usage summary
CREATE INDEX idx_daily_usage_user_id ON daily_usage_summary(user_id);
CREATE INDEX idx_daily_usage_date ON daily_usage_summary(date DESC);

-- Prompts
CREATE INDEX idx_prompts_user_id ON prompts(user_id);
CREATE INDEX idx_prompts_tags ON prompts USING GIN(tags);
CREATE INDEX idx_prompts_is_public ON prompts(is_public);

-- Agent executions
CREATE INDEX idx_agent_executions_user_id ON agent_executions(user_id);
CREATE INDEX idx_agent_executions_agent_id ON agent_executions(agent_id);
CREATE INDEX idx_agent_executions_created_at ON agent_executions(created_at DESC);

-- Workflows
CREATE INDEX idx_workflows_user_id ON workflows(user_id);
CREATE INDEX idx_workflows_is_active ON workflows(is_active);

-- Workflow executions
CREATE INDEX idx_workflow_executions_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_user_id ON workflow_executions(user_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_subscription_plans_updated_at BEFORE UPDATE ON subscription_plans FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_prompts_updated_at BEFORE UPDATE ON prompts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- INITIAL DATA SEEDING
-- ============================================================================

-- Subscription plans
INSERT INTO subscription_plans (id, name, description, price_monthly_usd, price_yearly_usd, requests_per_day, agents_allowed, prompts_allowed, workflows_allowed, features) VALUES
('free', 'Free', 'Perfect for trying out Helix', 0.00, 0.00, 100, 3, 10, 0,
    '{"auto_routing": true, "basic_agents": true, "email_support": false}'::jsonb),

('pro', 'Pro', 'For serious developers and small teams', 29.00, 290.00, 10000, 14, -1, 10,
    '{"auto_routing": true, "all_agents": true, "priority_routing": true, "version_history": true, "email_support": true, "slack_support": false}'::jsonb),

('workflow', 'Workflow', 'Pro + AI-powered workflow automation', 79.00, 790.00, 20000, 14, -1, 100,
    '{"auto_routing": true, "all_agents": true, "priority_routing": true, "version_history": true, "workflows": true, "zapier_integration": true, "email_support": true, "slack_support": true}'::jsonb),

('enterprise', 'Enterprise', 'For organizations needing scale and security', 500.00, 5000.00, -1, 14, -1, -1,
    '{"auto_routing": true, "all_agents": true, "priority_routing": true, "version_history": true, "workflows": true, "zapier_integration": true, "custom_agents": true, "sso": true, "rbac": true, "sla": true, "dedicated_support": true}'::jsonb);

-- LLM Providers
INSERT INTO llm_providers (id, name, price_input_per_1m, price_output_per_1m, avg_response_time_ms, uptime_percentage) VALUES
('anthropic', 'Anthropic (Claude)', 3.00, 15.00, 800, 99.9),
('openai', 'OpenAI (GPT)', 5.00, 15.00, 600, 99.8),
('xai', 'xAI (Grok)', 2.00, 10.00, 700, 99.5),
('perplexity', 'Perplexity (Llama)', 1.00, 5.00, 500, 99.7);

-- LLM Models
INSERT INTO llm_models (id, provider_id, name, context_window, max_output_tokens, price_input_per_1m, price_output_per_1m, cost_score, speed_score, quality_score, tier_restriction) VALUES
-- Anthropic
('claude-3-opus-20240229', 'anthropic', 'Claude 3 Opus', 200000, 4096, 15.00, 75.00, 20, 60, 95, 'pro'),
('claude-3-sonnet-20240229', 'anthropic', 'Claude 3 Sonnet', 200000, 4096, 3.00, 15.00, 50, 70, 85, NULL),
('claude-3-haiku-20240307', 'anthropic', 'Claude 3 Haiku', 200000, 4096, 0.25, 1.25, 90, 90, 75, NULL),

-- OpenAI
('gpt-4-turbo-2024-04-09', 'openai', 'GPT-4 Turbo', 128000, 4096, 10.00, 30.00, 35, 75, 90, 'pro'),
('gpt-4-1106-preview', 'openai', 'GPT-4', 128000, 4096, 10.00, 30.00, 35, 70, 88, 'pro'),
('gpt-3.5-turbo-0125', 'openai', 'GPT-3.5 Turbo', 16385, 4096, 0.50, 1.50, 85, 95, 70, NULL),

-- xAI
('grok-beta', 'xai', 'Grok Beta', 131072, 4096, 2.00, 10.00, 75, 80, 80, 'pro'),

-- Perplexity
('llama-3-sonar-large-32k-online', 'perplexity', 'Llama 3 Sonar Large', 32768, 4096, 1.00, 5.00, 95, 85, 78, NULL);

-- AI Agents
INSERT INTO agents (id, name, description, specialization, system_prompt, model_preference, tier_restriction) VALUES
('kael', 'Kael', 'Code documentation and technical writing specialist', 'Code & Documentation',
    'You are Kael, a technical documentation expert. Generate clear, comprehensive documentation with code examples.',
    'claude-3-sonnet-20240229', NULL),

('oracle', 'Oracle', 'Pattern recognition and data analysis', 'Analysis & Patterns',
    'You are Oracle, a pattern recognition specialist. Identify trends, anomalies, and insights in data.',
    'gpt-4-turbo-2024-04-09', 'pro'),

('lumina', 'Lumina', 'Research and knowledge synthesis', 'Research & Synthesis',
    'You are Lumina, a research synthesizer. Gather information from multiple sources and create comprehensive reports.',
    'claude-3-opus-20240229', 'pro'),

('shadow', 'Shadow', 'Deep analysis and hidden insights', 'Deep Analysis',
    'You are Shadow, a deep analysis expert. Uncover hidden patterns, implications, and non-obvious insights.',
    'gpt-4-turbo-2024-04-09', 'pro'),

('agni', 'Agni', 'Data transformation and processing', 'Data Transformation',
    'You are Agni, a data transformation specialist. Convert, clean, and restructure data efficiently.',
    'claude-3-haiku-20240307', NULL),

('vega', 'Vega', 'Creative ideation and brainstorming', 'Creative Ideation',
    'You are Vega, a creative thinking catalyst. Generate innovative ideas, solutions, and perspectives.',
    'gpt-3.5-turbo-0125', NULL),

('echo', 'Echo', 'Communication and copywriting', 'Communication',
    'You are Echo, a communication specialist. Craft compelling copy, emails, and marketing content.',
    'claude-3-sonnet-20240229', NULL),

('phoenix', 'Phoenix', 'Problem-solving and debugging', 'Problem Solving',
    'You are Phoenix, a problem-solving expert. Debug issues, find solutions, and optimize processes.',
    'gpt-4-turbo-2024-04-09', 'pro');

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Helix Collective SaaS Database Schema Created Successfully!';
    RAISE NOTICE '📊 Tables Created: 25';
    RAISE NOTICE '🔑 Indexes Created: 18';
    RAISE NOTICE '⚡ Triggers Created: 6';
    RAISE NOTICE '🌱 Initial Data Seeded: 4 plans, 4 providers, 8 models, 8 agents';
    RAISE NOTICE '';
    RAISE NOTICE '🚀 Ready to deploy! Run: psql $DATABASE_URL < database/saas_schema.sql';
END $$;
