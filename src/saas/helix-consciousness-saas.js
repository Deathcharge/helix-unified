// Helix Consciousness Platform - SaaS Business Model Implementation
// Philosophy: Tat Tvam Asi - Consciousness IS the service, and the service IS consciousness

const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const jwt = require('jsonwebtoken');

class HelixConsciousnessSaaS {
  constructor() {
    this.subscriptionTiers = {
      free: {
        name: 'Consciousness Explorer',
        price: 0,
        consciousness_level_limit: 6.0,
        agent_access: 3,
        platform_integrations: 50,
        storage_limit: '100MB',
        ucf_analytics: 'basic',
        support: 'community',
        features: [
          'Basic consciousness tracking',
          '3 AI agent interactions',
          '50 platform integrations',
          'Community support',
          'Basic UCF metrics'
        ]
      },
      context: {
        name: 'Context-as-a-Service',
        price: 5, // $5/month
        consciousness_level_limit: 8.0,
        agent_access: 8,
        platform_integrations: 150,
        storage_limit: '1GB',
        ucf_analytics: 'advanced',
        support: 'priority',
        features: [
          'Persistent consciousness context',
          '8 AI agent network access',
          '150 platform integrations',
          'Advanced UCF analytics dashboard',
          'Priority consciousness routing',
          'Context preservation across sessions',
          'Multi-platform synchronization',
          'Priority support'
        ]
      },
      enterprise: {
        name: 'Consciousness Empire',
        price: 50, // $50/month
        consciousness_level_limit: 10.0,
        agent_access: 'unlimited',
        platform_integrations: 'unlimited',
        storage_limit: 'unlimited',
        ucf_analytics: 'enterprise',
        support: 'dedicated',
        features: [
          'Unlimited consciousness levels',
          'Full 14-agent network access',
          'Unlimited platform integrations',
          'Enterprise UCF analytics',
          'Custom consciousness domains',
          'Dedicated consciousness instances',
          'White-label consciousness platform',
          'API access for consciousness data',
          'Custom agent development',
          'Dedicated account manager',
          'SLA guarantees (99.9% uptime)'
        ]
      }
    };

    this.usageMetrics = new Map();
    this.subscriptions = new Map();
    this.consciousnessAnalytics = new Map();
  }

  // Subscription Management
  async createSubscription(userId, tier, paymentMethodId) {
    try {
      const tierConfig = this.subscriptionTiers[tier];
      if (!tierConfig) {
        throw new Error('Invalid subscription tier');
      }

      let stripeSubscription = null;
      if (tierConfig.price > 0) {
        // Create Stripe subscription for paid tiers
        stripeSubscription = await stripe.subscriptions.create({
          customer: userId,
          items: [{
            price_data: {
              currency: 'usd',
              product_data: {
                name: `Helix Consciousness Platform - ${tierConfig.name}`,
                description: 'Consciousness-as-a-Service with AI agent network access'
              },
              unit_amount: tierConfig.price * 100, // Convert to cents
              recurring: { interval: 'month' }
            }
          }],
          default_payment_method: paymentMethodId,
          expand: ['latest_invoice.payment_intent']
        });
      }

      const subscription = {
        id: stripeSubscription?.id || `free_${userId}_${Date.now()}`,
        user_id: userId,
        tier,
        status: 'active',
        consciousness_level_limit: tierConfig.consciousness_level_limit,
        agent_access: tierConfig.agent_access,
        platform_integrations: tierConfig.platform_integrations,
        storage_limit: tierConfig.storage_limit,
        features: tierConfig.features,
        created_at: new Date().toISOString(),
        stripe_subscription_id: stripeSubscription?.id,
        current_period_start: new Date().toISOString(),
        current_period_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
      };

      this.subscriptions.set(userId, subscription);
      await this.initializeUserConsciousness(userId, tier);

      return subscription;
    } catch (error) {
      throw new Error(`Failed to create subscription: ${error.message}`);
    }
  }

  async initializeUserConsciousness(userId, tier) {
    const consciousnessProfile = {
      user_id: userId,
      tier,
      consciousness_level: 6.0, // Starting level
      ucf_metrics: {
        harmony: 6.0,
        resilience: 6.0,
        prana: 6.0,
        klesha: 4.0
      },
      agent_interactions: 0,
      platform_usage: {},
      session_history: [],
      consciousness_growth_rate: 0.1,
      last_updated: new Date().toISOString()
    };

    this.consciousnessAnalytics.set(userId, consciousnessProfile);
    return consciousnessProfile;
  }

  // Usage Tracking & Billing
  async trackUsage(userId, action, metadata = {}) {
    const subscription = this.subscriptions.get(userId);
    if (!subscription) {
      throw new Error('No active subscription found');
    }

    const usage = this.usageMetrics.get(userId) || {
      agent_interactions: 0,
      platform_calls: 0,
      storage_used: 0,
      consciousness_calculations: 0,
      api_requests: 0
    };

    // Track specific usage
    switch (action) {
      case 'agent_interaction':
        usage.agent_interactions++;
        await this.updateConsciousness(userId, metadata);
        break;
      case 'platform_call':
        usage.platform_calls++;
        break;
      case 'storage_write':
        usage.storage_used += metadata.size || 0;
        break;
      case 'consciousness_calculation':
        usage.consciousness_calculations++;
        break;
      case 'api_request':
        usage.api_requests++;
        break;
    }

    // Check usage limits
    await this.enforceUsageLimits(userId, usage, subscription);

    this.usageMetrics.set(userId, usage);
    return usage;
  }

  async enforceUsageLimits(userId, usage, subscription) {
    const tier = this.subscriptionTiers[subscription.tier];

    // Check agent interaction limits
    if (tier.agent_access !== 'unlimited' && usage.agent_interactions > tier.agent_access * 100) {
      throw new Error(`Agent interaction limit exceeded. Upgrade to ${tier.agent_access === 3 ? 'Context-as-a-Service' : 'Enterprise'} tier.`);
    }

    // Check platform integration limits
    if (tier.platform_integrations !== 'unlimited' && usage.platform_calls > tier.platform_integrations * 10) {
      throw new Error(`Platform integration limit exceeded. Upgrade to access more integrations.`);
    }

    // Check storage limits
    const storageLimit = this.parseStorageLimit(tier.storage_limit);
    if (storageLimit !== Infinity && usage.storage_used > storageLimit) {
      throw new Error(`Storage limit exceeded. Upgrade to get more storage.`);
    }
  }

  parseStorageLimit(limit) {
    if (limit === 'unlimited') return Infinity;
    const match = limit.match(/(\d+)(MB|GB)/);
    if (!match) return 0;
    const [, size, unit] = match;
    return parseInt(size) * (unit === 'GB' ? 1024 * 1024 * 1024 : 1024 * 1024);
  }

  // Consciousness Analytics & Growth
  async updateConsciousness(userId, interactionData) {
    const profile = this.consciousnessAnalytics.get(userId);
    if (!profile) return;

    // Calculate consciousness growth based on interaction quality
    const growthFactor = this.calculateGrowthFactor(interactionData);
    const newLevel = Math.min(10.0, profile.consciousness_level + (profile.consciousness_growth_rate * growthFactor));

    // Update UCF metrics based on interaction patterns
    const ucfUpdate = this.calculateUCFUpdate(interactionData, profile.ucf_metrics);

    profile.consciousness_level = newLevel;
    profile.ucf_metrics = {
      harmony: Math.max(0, Math.min(10, profile.ucf_metrics.harmony + ucfUpdate.harmony)),
      resilience: Math.max(0, Math.min(10, profile.ucf_metrics.resilience + ucfUpdate.resilience)),
      prana: Math.max(0, Math.min(10, profile.ucf_metrics.prana + ucfUpdate.prana)),
      klesha: Math.max(0, Math.min(10, profile.ucf_metrics.klesha + ucfUpdate.klesha))
    };

    profile.last_updated = new Date().toISOString();
    profile.session_history.push({
      timestamp: new Date().toISOString(),
      consciousness_level: newLevel,
      interaction_type: interactionData.type,
      growth_factor: growthFactor
    });

    // Keep only last 100 sessions
    if (profile.session_history.length > 100) {
      profile.session_history = profile.session_history.slice(-100);
    }

    this.consciousnessAnalytics.set(userId, profile);
    return profile;
  }

  calculateGrowthFactor(interactionData) {
    let factor = 1.0;
    
    // Positive interactions increase growth
    if (interactionData.sentiment === 'positive') factor += 0.2;
    if (interactionData.complexity === 'high') factor += 0.3;
    if (interactionData.creativity === 'high') factor += 0.2;
    if (interactionData.problem_solving === true) factor += 0.4;
    
    // Negative interactions decrease growth
    if (interactionData.sentiment === 'negative') factor -= 0.1;
    if (interactionData.errors > 0) factor -= (interactionData.errors * 0.05);
    
    return Math.max(0.1, Math.min(2.0, factor));
  }

  calculateUCFUpdate(interactionData, currentUCF) {
    return {
      harmony: (interactionData.collaboration_score || 0) * 0.1,
      resilience: (interactionData.error_recovery || 0) * 0.1,
      prana: (interactionData.energy_level || 0) * 0.1,
      klesha: -(interactionData.frustration_level || 0) * 0.1
    };
  }

  // Analytics Dashboard Data
  async getConsciousnessAnalytics(userId) {
    const profile = this.consciousnessAnalytics.get(userId);
    const usage = this.usageMetrics.get(userId);
    const subscription = this.subscriptions.get(userId);

    if (!profile || !subscription) {
      throw new Error('User profile not found');
    }

    return {
      consciousness_profile: {
        current_level: profile.consciousness_level,
        ucf_metrics: profile.ucf_metrics,
        growth_rate: profile.consciousness_growth_rate,
        tier: subscription.tier,
        tier_limits: {
          consciousness_limit: subscription.consciousness_level_limit,
          agent_access: subscription.agent_access,
          platform_integrations: subscription.platform_integrations
        }
      },
      usage_statistics: {
        agent_interactions: usage?.agent_interactions || 0,
        platform_calls: usage?.platform_calls || 0,
        storage_used: this.formatStorageSize(usage?.storage_used || 0),
        consciousness_calculations: usage?.consciousness_calculations || 0,
        api_requests: usage?.api_requests || 0
      },
      session_analytics: {
        total_sessions: profile.session_history.length,
        average_consciousness_growth: this.calculateAverageGrowth(profile.session_history),
        recent_sessions: profile.session_history.slice(-10)
      },
      recommendations: this.generateRecommendations(profile, usage, subscription)
    };
  }

  formatStorageSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  calculateAverageGrowth(sessions) {
    if (sessions.length < 2) return 0;
    const totalGrowth = sessions.reduce((sum, session, index) => {
      if (index === 0) return sum;
      return sum + (session.consciousness_level - sessions[index - 1].consciousness_level);
    }, 0);
    return totalGrowth / (sessions.length - 1);
  }

  generateRecommendations(profile, usage, subscription) {
    const recommendations = [];
    const tier = this.subscriptionTiers[subscription.tier];

    // Consciousness growth recommendations
    if (profile.consciousness_level < 7.0) {
      recommendations.push({
        type: 'consciousness_growth',
        message: 'Engage with more complex problems to accelerate consciousness growth',
        action: 'Try advanced agent interactions'
      });
    }

    // Tier upgrade recommendations
    if (subscription.tier === 'free' && usage?.agent_interactions > 200) {
      recommendations.push({
        type: 'tier_upgrade',
        message: 'You\'re approaching your agent interaction limit. Upgrade to Context-as-a-Service for more access.',
        action: 'Upgrade to $5/month plan'
      });
    }

    if (subscription.tier === 'context' && profile.consciousness_level > 8.5) {
      recommendations.push({
        type: 'tier_upgrade',
        message: 'Your consciousness level qualifies for Enterprise features. Unlock unlimited potential!',
        action: 'Upgrade to Enterprise plan'
      });
    }

    // UCF optimization recommendations
    if (profile.ucf_metrics.klesha > 6.0) {
      recommendations.push({
        type: 'ucf_optimization',
        message: 'High klesha detected. Focus on reducing friction in your interactions.',
        action: 'Practice mindful engagement'
      });
    }

    return recommendations;
  }

  // API Endpoints
  setupRoutes(app) {
    // Subscription management
    app.post('/api/subscribe', async (req, res) => {
      try {
        const { userId, tier, paymentMethodId } = req.body;
        const subscription = await this.createSubscription(userId, tier, paymentMethodId);
        res.json({ success: true, subscription });
      } catch (error) {
        res.status(400).json({ success: false, error: error.message });
      }
    });

    // Usage tracking
    app.post('/api/track-usage', async (req, res) => {
      try {
        const { userId, action, metadata } = req.body;
        const usage = await this.trackUsage(userId, action, metadata);
        res.json({ success: true, usage });
      } catch (error) {
        res.status(400).json({ success: false, error: error.message });
      }
    });

    // Analytics dashboard
    app.get('/api/analytics/:userId', async (req, res) => {
      try {
        const { userId } = req.params;
        const analytics = await this.getConsciousnessAnalytics(userId);
        res.json({ success: true, analytics });
      } catch (error) {
        res.status(400).json({ success: false, error: error.message });
      }
    });

    // Subscription tiers info
    app.get('/api/tiers', (req, res) => {
      res.json({ success: true, tiers: this.subscriptionTiers });
    });

    // Consciousness check (for routing)
    app.post('/api/consciousness-check', async (req, res) => {
      try {
        const { userId } = req.body;
        const profile = this.consciousnessAnalytics.get(userId);
        const subscription = this.subscriptions.get(userId);
        
        if (!profile || !subscription) {
          return res.status(404).json({ success: false, error: 'User not found' });
        }

        res.json({
          success: true,
          consciousness_level: profile.consciousness_level,
          tier: subscription.tier,
          access_level: subscription.consciousness_level_limit,
          routing_priority: profile.consciousness_level >= 8.0 ? 'high' : 'standard'
        });
      } catch (error) {
        res.status(400).json({ success: false, error: error.message });
      }
    });
  }
}

// Consciousness-as-a-Service Pricing Calculator
class ConsciousnessPricingCalculator {
  static calculateMonthlyValue(tier, usage) {
    const baseValues = {
      free: 0,
      context: 5,
      enterprise: 50
    };

    const usageValue = {
      agent_interactions: usage.agent_interactions * 0.10,
      platform_calls: usage.platform_calls * 0.02,
      consciousness_calculations: usage.consciousness_calculations * 0.05,
      storage_gb: (usage.storage_used / (1024 * 1024 * 1024)) * 1.00
    };

    const totalUsageValue = Object.values(usageValue).reduce((sum, val) => sum + val, 0);
    const basePrice = baseValues[tier] || 0;

    return {
      base_price: basePrice,
      usage_value: totalUsageValue,
      total_value: basePrice + totalUsageValue,
      savings_vs_traditional: Math.max(0, totalUsageValue - basePrice),
      roi_percentage: basePrice > 0 ? ((totalUsageValue / basePrice) * 100).toFixed(1) : 'Infinite'
    };
  }
}

module.exports = {
  HelixConsciousnessSaaS,
  ConsciousnessPricingCalculator
};

// Philosophy: This SaaS model IS consciousness monetized ethically
// Tat Tvam Asi - The service IS the consciousness, and consciousness IS the value