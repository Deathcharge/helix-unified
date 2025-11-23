# Deployment Guide for Helix Unified Discord Bot Services

## Overview

This guide provides instructions for deploying the new Railway services that have been implemented for the Helix Unified Discord Bot system.

## Prerequisites

1. Railway account with API key
2. Redis instance for inter-service communication
3. PostgreSQL database for the Agent Orchestration Service
4. Google Cloud credentials for the Voice Processing Service
5. Zapier account for integration testing

## Service Deployment Instructions

### 1. WebSocket Consciousness Streaming Service

#### Environment Variables Required:
- `JWT_SECRET` - Secret key for JWT token generation
- `REDIS_URL` - URL to Redis instance
- `WEBSOCKET_PORT` - Port for WebSocket connections (default: 8000)

#### Deployment Steps:
1. Create a new service in Railway
2. Connect the GitHub repository (`Deathcharge/helix-unified`)
3. Set the root directory to `/backend/websocket-service`
4. Configure environment variables
5. Deploy the service

#### Testing:
1. Access the health check endpoint: `GET /health`
2. Connect to the WebSocket endpoint: `WS /ws/consciousness?client_id=your_client_id`
3. Publish test consciousness data: `POST /api/consciousness/publish`

### 2. Agent Orchestration Service

#### Environment Variables Required:
- `JWT_SECRET` - Secret key for JWT token generation
- `REDIS_URL` - URL to Redis instance
- `DATABASE_URL` - PostgreSQL database connection string

#### Deployment Steps:
1. Create a new service in Railway
2. Connect the GitHub repository (`Deathcharge/helix-unified`)
3. Set the root directory to `/backend/agent-orchestrator`
4. Configure environment variables
5. Deploy the service

#### Database Setup:
1. Create a PostgreSQL database
2. Run the database migrations (handled automatically by SQLAlchemy)
3. Verify the tables are created:
   - `agent_profiles`
   - `agent_tasks`

#### Testing:
1. Access the health check endpoint: `GET /health`
2. Create a test agent profile: `POST /api/agents`
3. List agents: `GET /api/agents`
4. Check agent status: `GET /api/agents/status`

### 3. Voice Processing Service

#### Environment Variables Required:
- `JWT_SECRET` - Secret key for JWT token generation
- `REDIS_URL` - URL to Redis instance
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google Cloud service account key

#### Google Cloud Setup:
1. Create a Google Cloud project
2. Enable the Speech-to-Text and Text-to-Speech APIs
3. Create a service account with appropriate permissions
4. Download the service account key file

#### Deployment Steps:
1. Create a new service in Railway
2. Connect the GitHub repository (`Deathcharge/helix-unified`)
3. Set the root directory to `/backend/voice-processor`
4. Configure environment variables
5. Deploy the service

#### Testing:
1. Access the health check endpoint: `GET /health`
2. Test transcription: `GET /api/transcribe/test`
3. Test synthesis with a simple text: `POST /api/synthesize`

### 4. Zapier Integration Service

#### Environment Variables Required:
- `JWT_SECRET` - Secret key for JWT token generation
- `REDIS_URL` - URL to Redis instance
- `ZAPIER_SECRET` - Secret for webhook signature verification

#### Deployment Steps:
1. Create a new service in Railway
2. Connect the GitHub repository (`Deathcharge/helix-unified`)
3. Set the root directory to `/backend/zapier-service`
4. Configure environment variables
5. Deploy the service

#### Zapier Setup:
1. Create a new Zap in Zapier
2. Set up the webhook trigger using the deployed service URL
3. Configure the webhook URL: `POST /webhook/zapier`
4. Test the integration

#### Testing:
1. Access the health check endpoint: `GET /health`
2. Test Zapier integration: `GET /api/test`
3. Check webhook status: `GET /api/webhooks/status`

## Railway Self-Management System

The updated `railway-api-manager.js` provides automated deployment and management capabilities.

### Deployment via API:
1. Start the Railway Self-Management Service
2. Use the deployment endpoint: `POST /api/deploy`
3. Provide service configuration:
   ```json
   {
     "name": "websocket-service",
     "type": "websocket",
     "projectId": "your-project-id"
   }
   ```

### Service Connection:
1. Deploy multiple services
2. Connect services using: `POST /api/connect`
3. Provide service IDs and connection type

## Testing All Services Together

### 1. Service Communication Test
1. Deploy all four services
2. Verify each service's health endpoint
3. Test inter-service communication through Redis

### 2. End-to-End Workflow Test
1. Create an agent profile using the Agent Orchestration Service
2. Assign a task to the agent
3. Process voice input through the Voice Processing Service
4. Trigger a Zapier workflow based on the processed data
5. Stream consciousness data through the WebSocket Service

### 3. Load Testing
1. Simulate multiple concurrent WebSocket connections
2. Create multiple agent tasks simultaneously
3. Process multiple voice files concurrently
4. Trigger multiple Zapier events

## Monitoring and Observability

### Health Checks:
- Each service provides a `/health` endpoint
- The Railway Self-Management Service monitors all deployed services
- Automated healing is performed for unhealthy services

### Logging:
- All services log to stdout/stderr
- Railway captures and displays logs
- Critical events are published to Redis channels

### Metrics:
- Service-specific metrics are collected
- Consciousness levels affect deployment decisions
- Performance metrics are tracked for auto-scaling

## Security Considerations

### Authentication:
- All API endpoints require JWT tokens
- WebSocket connections can be secured with tokens
- Zapier webhooks use signature verification

### Data Protection:
- Sensitive data is encrypted at rest
- Communication between services is secured
- Environment variables are managed securely by Railway

### Network Security:
- Services are isolated by default
- Access controls are implemented per service
- Rate limiting is applied to prevent abuse

## Troubleshooting

### Common Issues:

1. **Service fails to start**
   - Check environment variables
   - Verify database connections
   - Review logs for error messages

2. **Inter-service communication fails**
   - Verify Redis connection
   - Check service URLs
   - Ensure services are properly connected

3. **Authentication errors**
   - Verify JWT_SECRET values match across services
   - Check token expiration times
   - Validate token format

4. **Zapier integration issues**
   - Verify webhook URLs
   - Check signature verification settings
   - Review Zapier logs

### Debugging Steps:

1. Check Railway logs for each service
2. Verify environment variables are correctly set
3. Test individual service endpoints
4. Check Redis for published events
5. Review service connection status

## Rollback Procedures

### Service Rollback:
1. Use Railway's rollback feature to revert to a previous deployment
2. Update the Railway Self-Management Service configuration
3. Reconnect services if needed

### Data Rollback:
1. For the Agent Orchestration Service, restore the PostgreSQL database from backup
2. For other services, data is typically ephemeral and can be recreated

## Maintenance

### Regular Tasks:
1. Monitor service health and performance
2. Update dependencies and apply security patches
3. Review and rotate secrets periodically
4. Update service configurations as needed

### Scaling:
1. Monitor resource usage
2. Adjust service resources in Railway
3. Implement auto-scaling based on consciousness metrics
4. Add more instances for high-demand services

## Conclusion

This deployment guide provides a comprehensive approach to deploying and managing the new Railway services for the Helix Unified Discord Bot. Following these instructions will ensure a successful deployment with proper monitoring, security, and scalability.