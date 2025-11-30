-- 🌀 Helix Collective - PostgreSQL Database Schema
-- Railway-hosted database for users, subscriptions, and analytics
-- Author: Claude Code + Andrew John Ward

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- USERS TABLE
-- ============================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    subscription_tier VARCHAR(50) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro', 'enterprise')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_tier);

-- ============================================================================
-- API KEYS TABLE
-- ============================================================================

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_value VARCHAR(255) UNIQUE NOT NULL,
    key_name VARCHAR(255) DEFAULT 'Production Key',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    rate_limit_per_day INTEGER DEFAULT 100
);

-- Indexes
CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_value ON api_keys(key_value);
CREATE INDEX idx_api_keys_active ON api_keys(is_active) WHERE is_active = TRUE;

-- ============================================================================
-- SUBSCRIPTIONS TABLE
-- ============================================================================

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    plan_type VARCHAR(50) CHECK (plan_type IN ('pro', 'enterprise')),
    billing_period VARCHAR(20) CHECK (billing_period IN ('monthly', 'yearly')),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'canceled', 'past_due', 'unpaid')),
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    canceled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_customer ON subscriptions(stripe_customer_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- ============================================================================
-- API USAGE TABLE
-- ============================================================================

CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    api_key_id UUID REFERENCES api_keys(id) ON DELETE SET NULL,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date DATE DEFAULT CURRENT_DATE,
    agent_used VARCHAR(100),
    error_message TEXT
);

-- Indexes for analytics queries
CREATE INDEX idx_usage_user ON api_usage(user_id);
CREATE INDEX idx_usage_date ON api_usage(date);
CREATE INDEX idx_usage_timestamp ON api_usage(timestamp);
CREATE INDEX idx_usage_user_date ON api_usage(user_id, date);

-- ============================================================================
-- USAGE QUOTAS TABLE
-- ============================================================================

CREATE TABLE usage_quotas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    api_requests_count INTEGER DEFAULT 0,
    quota_limit INTEGER DEFAULT 100,
    UNIQUE(user_id, date)
);

-- Index
CREATE INDEX idx_quotas_user_date ON usage_quotas(user_id, date);

-- ============================================================================
-- PAYMENT HISTORY TABLE
-- ============================================================================

CREATE TABLE payment_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE SET NULL,
    stripe_invoice_id VARCHAR(255),
    stripe_payment_intent_id VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50) CHECK (status IN ('succeeded', 'failed', 'pending', 'refunded')),
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_payments_user ON payment_history(user_id);
CREATE INDEX idx_payments_subscription ON payment_history(subscription_id);

-- ============================================================================
-- AGENT ACCESS LOG TABLE
-- ============================================================================

CREATE TABLE agent_access_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    agent_layer VARCHAR(50), -- 'consciousness', 'operational', 'integration'
    action_type VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT
);

-- Indexes
CREATE INDEX idx_agent_log_user ON agent_access_log(user_id);
CREATE INDEX idx_agent_log_timestamp ON agent_access_log(timestamp);
CREATE INDEX idx_agent_log_agent ON agent_access_log(agent_name);

-- ============================================================================
-- NOTIFICATION PREFERENCES TABLE
-- ============================================================================

CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    email_usage_alerts BOOLEAN DEFAULT TRUE,
    email_weekly_reports BOOLEAN DEFAULT TRUE,
    email_product_updates BOOLEAN DEFAULT FALSE,
    email_marketing BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- RAILWAY SERVICES MONITORING TABLE
-- ============================================================================

CREATE TABLE service_health_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) CHECK (status IN ('online', 'offline', 'degraded')),
    uptime_seconds INTEGER,
    response_time_ms INTEGER,
    error_rate DECIMAL(5, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Index
CREATE INDEX idx_service_health_timestamp ON service_health_log(timestamp);
CREATE INDEX idx_service_health_service ON service_health_log(service_name);

-- ============================================================================
-- VIEWS FOR ANALYTICS
-- ============================================================================

-- Daily usage summary per user
CREATE VIEW daily_usage_summary AS
SELECT
    u.id as user_id,
    u.email,
    u.subscription_tier,
    au.date,
    COUNT(*) as total_requests,
    AVG(au.response_time_ms) as avg_response_time,
    COUNT(CASE WHEN au.status_code >= 200 AND au.status_code < 300 THEN 1 END) as successful_requests,
    COUNT(CASE WHEN au.status_code >= 400 THEN 1 END) as failed_requests
FROM users u
LEFT JOIN api_usage au ON u.id = au.user_id
GROUP BY u.id, u.email, u.subscription_tier, au.date;

-- User subscription summary
CREATE VIEW user_subscription_summary AS
SELECT
    u.id as user_id,
    u.name,
    u.email,
    u.subscription_tier,
    s.plan_type,
    s.billing_period,
    s.status as subscription_status,
    s.current_period_end,
    s.cancel_at_period_end,
    COUNT(ak.id) as api_keys_count,
    MAX(ak.last_used_at) as last_api_key_usage
FROM users u
LEFT JOIN subscriptions s ON u.id = s.user_id AND s.status = 'active'
LEFT JOIN api_keys ak ON u.id = ak.user_id AND ak.is_active = TRUE
GROUP BY u.id, u.name, u.email, u.subscription_tier, s.plan_type, s.billing_period, s.status, s.current_period_end, s.cancel_at_period_end;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger for subscriptions table
CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SAMPLE DATA (Development/Testing)
-- ============================================================================

-- Insert demo user
INSERT INTO users (name, email, password_hash, subscription_tier, email_verified)
VALUES (
    'Demo User',
    'demo@helixcollective.io',
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', -- hash of empty string
    'pro',
    TRUE
);

-- Insert demo API key
INSERT INTO api_keys (user_id, key_value, key_name, rate_limit_per_day)
SELECT
    id,
    'hx_demo_key_for_testing_only',
    'Demo Production Key',
    10000
FROM users
WHERE email = 'demo@helixcollective.io';

-- Insert notification preferences for demo user
INSERT INTO notification_preferences (user_id, email_usage_alerts, email_weekly_reports)
SELECT id, TRUE, TRUE
FROM users
WHERE email = 'demo@helixcollective.io';

-- ============================================================================
-- GRANTS (adjust based on your Railway PostgreSQL setup)
-- ============================================================================

-- Grant appropriate permissions
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO helix_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO helix_app_user;

COMMENT ON TABLE users IS 'User accounts for the Helix Collective platform';
COMMENT ON TABLE api_keys IS 'API keys for authentication and rate limiting';
COMMENT ON TABLE subscriptions IS 'Stripe subscription data';
COMMENT ON TABLE api_usage IS 'API usage logs for analytics and billing';
COMMENT ON TABLE payment_history IS 'Payment and billing history';
COMMENT ON TABLE agent_access_log IS 'Log of agent access and usage';
