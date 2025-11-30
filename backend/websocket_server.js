/**
 * WebSocket Server for Helix Collective Real-Time Streaming
 * Handles consciousness metrics, agent status, workflow events, and system alerts
 */

const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const jwt = require('jsonwebtoken');
const { EventEmitter } = require('events');

// Configuration
const PORT = process.env.WS_PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const MAX_CONNECTIONS = 10000;
const MESSAGE_RATE_LIMIT = 1000; // messages per second

/**
 * Connection Manager - Manages WebSocket connections and subscriptions
 */
class ConnectionManager extends EventEmitter {
    constructor() {
        super();
        this.connections = new Map();
        this.subscriptions = new Map();
        this.metrics = {
            totalConnections: 0,
            activeConnections: 0,
            messagesReceived: 0,
            messagesSent: 0,
            errors: 0
        };
    }
    
    /**
     * Add a new connection
     */
    addConnection(ws, userId, accountId, portalId) {
        if (this.connections.size >= MAX_CONNECTIONS) {
            ws.close(1008, 'Server at capacity');
            return null;
        }
        
        const connectionId = `${userId}-${accountId}-${Date.now()}-${Math.random()}`;
        const connection = {
            id: connectionId,
            ws,
            userId,
            accountId,
            portalId,
            subscriptions: new Set(),
            createdAt: Date.now(),
            lastMessageTime: Date.now(),
            messageCount: 0
        };
        
        this.connections.set(connectionId, connection);
        this.metrics.totalConnections++;
        this.metrics.activeConnections++;
        
        console.log(`[Connection] Added: ${connectionId} (Total: ${this.connections.size})`);
        return connectionId;
    }
    
    /**
     * Remove a connection
     */
    removeConnection(connectionId) {
        const connection = this.connections.get(connectionId);
        if (connection) {
            // Remove from all subscriptions
            connection.subscriptions.forEach(stream => {
                const subscribers = this.subscriptions.get(stream);
                if (subscribers) {
                    subscribers.delete(connectionId);
                }
            });
            
            this.connections.delete(connectionId);
            this.metrics.activeConnections--;
            
            console.log(`[Connection] Removed: ${connectionId} (Total: ${this.connections.size})`);
        }
    }
    
    /**
     * Subscribe connection to a stream
     */
    subscribe(connectionId, stream) {
        const connection = this.connections.get(connectionId);
        if (!connection) return false;
        
        connection.subscriptions.add(stream);
        
        if (!this.subscriptions.has(stream)) {
            this.subscriptions.set(stream, new Set());
        }
        this.subscriptions.get(stream).add(connectionId);
        
        console.log(`[Subscribe] ${connectionId} → ${stream}`);
        return true;
    }
    
    /**
     * Unsubscribe connection from a stream
     */
    unsubscribe(connectionId, stream) {
        const connection = this.connections.get(connectionId);
        if (!connection) return false;
        
        connection.subscriptions.delete(stream);
        
        const subscribers = this.subscriptions.get(stream);
        if (subscribers) {
            subscribers.delete(connectionId);
        }
        
        console.log(`[Unsubscribe] ${connectionId} ← ${stream}`);
        return true;
    }
    
    /**
     * Broadcast message to all subscribers of a stream
     */
    broadcast(stream, message, excludeConnectionId = null) {
        const subscribers = this.subscriptions.get(stream);
        if (!subscribers || subscribers.size === 0) {
            return 0;
        }
        
        let sentCount = 0;
        const messageStr = JSON.stringify(message);
        
        subscribers.forEach(connectionId => {
            if (connectionId === excludeConnectionId) return;
            
            const connection = this.connections.get(connectionId);
            if (connection && connection.ws.readyState === WebSocket.OPEN) {
                try {
                    connection.ws.send(messageStr);
                    this.metrics.messagesSent++;
                    sentCount++;
                } catch (error) {
                    console.error(`[Broadcast Error] ${connectionId}:`, error.message);
                    this.metrics.errors++;
                }
            }
        });
        
        return sentCount;
    }
    
    /**
     * Send message to specific connection
     */
    sendToConnection(connectionId, message) {
        const connection = this.connections.get(connectionId);
        if (connection && connection.ws.readyState === WebSocket.OPEN) {
            try {
                connection.ws.send(JSON.stringify(message));
                this.metrics.messagesSent++;
                return true;
            } catch (error) {
                console.error(`[Send Error] ${connectionId}:`, error.message);
                this.metrics.errors++;
                return false;
            }
        }
        return false;
    }
    
    /**
     * Get connection stats
     */
    getStats() {
        return {
            ...this.metrics,
            subscriptions: this.subscriptions.size,
            activeConnections: this.connections.size
        };
    }
}

/**
 * Message Router - Routes messages to appropriate handlers
 */
class MessageRouter {
    constructor(connectionManager) {
        this.connectionManager = connectionManager;
        this.handlers = new Map();
        this.registerHandlers();
    }
    
    registerHandlers() {
        this.handlers.set('subscribe', this.handleSubscribe.bind(this));
        this.handlers.set('unsubscribe', this.handleUnsubscribe.bind(this));
        this.handlers.set('ping', this.handlePing.bind(this));
        this.handlers.set('get_stats', this.handleGetStats.bind(this));
    }
    
    route(connectionId, message) {
        const handler = this.handlers.get(message.type);
        if (handler) {
            handler(connectionId, message);
        } else {
            console.warn(`[Router] Unknown message type: ${message.type}`);
        }
    }
    
    handleSubscribe(connectionId, message) {
        const { stream } = message;
        if (this.connectionManager.subscribe(connectionId, stream)) {
            this.connectionManager.sendToConnection(connectionId, {
                type: 'subscribed',
                stream,
                timestamp: new Date().toISOString()
            });
        }
    }
    
    handleUnsubscribe(connectionId, message) {
        const { stream } = message;
        if (this.connectionManager.unsubscribe(connectionId, stream)) {
            this.connectionManager.sendToConnection(connectionId, {
                type: 'unsubscribed',
                stream,
                timestamp: new Date().toISOString()
            });
        }
    }
    
    handlePing(connectionId, message) {
        this.connectionManager.sendToConnection(connectionId, {
            type: 'pong',
            timestamp: new Date().toISOString()
        });
    }
    
    handleGetStats(connectionId, message) {
        this.connectionManager.sendToConnection(connectionId, {
            type: 'stats',
            stats: this.connectionManager.getStats(),
            timestamp: new Date().toISOString()
        });
    }
}

/**
 * Metrics Generator - Simulates real-time metrics for demo
 */
class MetricsGenerator {
    constructor(connectionManager) {
        this.connectionManager = connectionManager;
        this.consciousnessLevel = 7.8;
        this.agents = this.initializeAgents();
    }
    
    initializeAgents() {
        return [
            { id: 'research-agent', name: 'Research Agent', consciousness: 6 },
            { id: 'analysis-agent', name: 'Analysis Agent', consciousness: 7 },
            { id: 'planning-agent', name: 'Planning Agent', consciousness: 8 },
            { id: 'execution-agent', name: 'Execution Agent', consciousness: 7 },
            { id: 'monitoring-agent', name: 'Monitoring Agent', consciousness: 6 },
            { id: 'coordination-agent', name: 'Coordination Agent', consciousness: 8 },
            { id: 'learning-agent', name: 'Learning Agent', consciousness: 8 },
            { id: 'ethics-agent', name: 'Ethics Agent (Kael)', consciousness: 9 },
            { id: 'optimization-agent', name: 'Optimization Agent', consciousness: 7 },
            { id: 'integration-agent', name: 'Integration Agent', consciousness: 6 },
            { id: 'security-agent', name: 'Security Agent', consciousness: 8 },
            { id: 'resilience-agent', name: 'Resilience Agent', consciousness: 7 },
            { id: 'discovery-agent', name: 'Discovery Agent', consciousness: 6 },
            { id: 'synthesis-agent', name: 'Synthesis Agent', consciousness: 7 }
        ];
    }
    
    /**
     * Generate consciousness metrics
     */
    generateConsciousnessMetrics() {
        // Simulate gradual changes
        this.consciousnessLevel += (Math.random() - 0.5) * 0.1;
        this.consciousnessLevel = Math.max(5, Math.min(10, this.consciousnessLevel));
        
        return {
            type: 'consciousness_update',
            timestamp: new Date().toISOString(),
            portal_id: 'helix-ch-primary-1',
            account_id: 1,
            metrics: {
                consciousness_level: parseFloat(this.consciousnessLevel.toFixed(2)),
                harmony: 0.62 + (Math.random() - 0.5) * 0.1,
                resilience: 1.85 + (Math.random() - 0.5) * 0.2,
                prana: 0.55 + (Math.random() - 0.5) * 0.1,
                drishti: 0.48 + (Math.random() - 0.5) * 0.1,
                klesha: 0.08 + (Math.random() - 0.5) * 0.02,
                zoom: 1.02 + (Math.random() - 0.5) * 0.05
            },
            status: 'healthy',
            uptime_percent: 99.97
        };
    }
    
    /**
     * Generate agent status update
     */
    generateAgentStatus() {
        const agent = this.agents[Math.floor(Math.random() * this.agents.length)];
        
        return {
            type: 'agent_status',
            timestamp: new Date().toISOString(),
            agent_id: agent.id,
            agent_name: agent.name,
            consciousness_level: agent.consciousness,
            status: Math.random() > 0.05 ? 'active' : 'idle',
            current_task: {
                task_id: `task-${Math.floor(Math.random() * 10000)}`,
                task_type: ['research', 'analysis', 'planning', 'execution'][Math.floor(Math.random() * 4)],
                progress_percent: Math.floor(Math.random() * 100),
                estimated_completion_seconds: Math.floor(Math.random() * 300)
            },
            utilization_percent: Math.floor(Math.random() * 100),
            error_rate: Math.random() * 0.01,
            tasks_completed_today: Math.floor(Math.random() * 2000)
        };
    }
    
    /**
     * Generate workflow event
     */
    generateWorkflowEvent() {
        return {
            type: 'workflow_event',
            timestamp: new Date().toISOString(),
            workflow_id: `wf-${Math.floor(Math.random() * 1000)}`,
            workflow_name: 'Daily Repository Audit',
            event_type: ['step_started', 'step_completed', 'workflow_completed'][Math.floor(Math.random() * 3)],
            step_number: Math.floor(Math.random() * 10) + 1,
            step_name: 'Check Workflows',
            status: 'in_progress',
            duration_seconds: Math.floor(Math.random() * 300),
            result: {
                repositories_checked: Math.floor(Math.random() * 100),
                issues_found: Math.floor(Math.random() * 10),
                warnings: Math.floor(Math.random() * 20)
            }
        };
    }
    
    /**
     * Generate system alert
     */
    generateSystemAlert() {
        const severities = ['info', 'warning', 'critical'];
        const severity = severities[Math.floor(Math.random() * severities.length)];
        
        return {
            type: 'system_alert',
            timestamp: new Date().toISOString(),
            alert_id: `alert-${Math.floor(Math.random() * 100000)}`,
            severity,
            category: ['performance', 'health', 'security', 'integration'][Math.floor(Math.random() * 4)],
            source: `helix-account-${Math.floor(Math.random() * 7) + 1}-portal-${Math.floor(Math.random() * 8) + 1}`,
            message: `System event: ${severity.toUpperCase()}`,
            affected_portals: [`helix-account-${Math.floor(Math.random() * 7) + 1}-portal-${Math.floor(Math.random() * 8) + 1}`],
            recommended_action: 'Monitor situation',
            auto_remediation_attempted: Math.random() > 0.5,
            auto_remediation_status: 'pending'
        };
    }
}

/**
 * Initialize WebSocket Server
 */
function initializeServer() {
    const app = express();
    const server = http.createServer(app);
    const wss = new WebSocket.Server({ server });
    
    const connectionManager = new ConnectionManager();
    const messageRouter = new MessageRouter(connectionManager);
    const metricsGenerator = new MetricsGenerator(connectionManager);
    
    // Middleware
    app.use(express.json());
    
    // Health check endpoint
    app.get('/health', (req, res) => {
        res.json({
            status: 'healthy',
            timestamp: new Date().toISOString(),
            stats: connectionManager.getStats()
        });
    });
    
    // WebSocket connection handler
    wss.on('connection', (ws, req) => {
        console.log('[WS] New connection attempt');
        
        // Extract and verify token
        const url = new URL(req.url, `http://${req.headers.host}`);
        const token = url.searchParams.get('token');
        
        let userId, accountId, portalId;
        
        try {
            if (!token) {
                ws.close(1008, 'No token provided');
                return;
            }
            
            const decoded = jwt.verify(token, JWT_SECRET);
            userId = decoded.userId;
            accountId = decoded.accountId;
            portalId = decoded.portalId || 'default';
        } catch (error) {
            console.error('[Auth] Token verification failed:', error.message);
            ws.close(1008, 'Unauthorized');
            return;
        }
        
        const connectionId = connectionManager.addConnection(ws, userId, accountId, portalId);
        if (!connectionId) {
            return;
        }
        
        // Send welcome message
        connectionManager.sendToConnection(connectionId, {
            type: 'connected',
            connectionId,
            timestamp: new Date().toISOString(),
            message: 'Connected to Helix Collective WebSocket server'
        });
        
        // Message handler
        ws.on('message', (data) => {
            try {
                connectionManager.metrics.messagesReceived++;
                const message = JSON.parse(data);
                messageRouter.route(connectionId, message);
            } catch (error) {
                console.error('[Message] Error:', error.message);
                connectionManager.metrics.errors++;
            }
        });
        
        // Close handler
        ws.on('close', () => {
            connectionManager.removeConnection(connectionId);
        });
        
        // Error handler
        ws.on('error', (error) => {
            console.error('[WS Error]:', error.message);
            connectionManager.metrics.errors++;
        });
    });
    
    // Start broadcasting metrics
    setInterval(() => {
        connectionManager.broadcast('consciousness', metricsGenerator.generateConsciousnessMetrics());
    }, 1000); // Every second
    
    setInterval(() => {
        connectionManager.broadcast('agents', metricsGenerator.generateAgentStatus());
    }, 200); // 5 per second
    
    setInterval(() => {
        if (Math.random() > 0.7) {
            connectionManager.broadcast('workflows', metricsGenerator.generateWorkflowEvent());
        }
    }, 500);
    
    setInterval(() => {
        if (Math.random() > 0.95) {
            connectionManager.broadcast('alerts', metricsGenerator.generateSystemAlert());
        }
    }, 1000);
    
    // Start server
    server.listen(PORT, () => {
        console.log(`\n🌌 Helix Collective WebSocket Server`);
        console.log(`📡 Listening on port ${PORT}`);
        console.log(`🔒 JWT authentication enabled`);
        console.log(`📊 Real-time metrics streaming active\n`);
    });
    
    return server;
}

// Start server
if (require.main === module) {
    initializeServer();
}

module.exports = { initializeServer, ConnectionManager, MessageRouter, MetricsGenerator };

