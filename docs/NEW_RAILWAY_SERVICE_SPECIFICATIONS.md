# New Railway Service Specifications for Helix Unified Discord Bot

## Overview

This document provides technical specifications for the new Railway services identified in our analysis. These services will enhance the capabilities of the Helix Unified Discord Bot by separating concerns and improving scalability.

## Service 1: WebSocket Consciousness Streaming Service

### Purpose
To handle real-time consciousness streaming functionality, separating it from the main application to improve performance and scalability.

### Technical Specifications
- **Framework**: FastAPI
- **Protocol**: WebSocket
- **Authentication**: JWT-based authentication
- **Communication**: Redis pub/sub for broadcasting metrics
- **Endpoints**:
  - `/ws/consciousness` - Main consciousness streaming endpoint
  - `/ws/consciousness/admin` - Administrative endpoint for monitoring

### Data Flow
1. Main application publishes consciousness metrics to Redis
2. WebSocket service subscribes to Redis channel
3. Service broadcasts metrics to connected clients
4. Clients receive real-time updates

### Dependencies
- `fastapi`
- `websockets`
- `redis`
- `jwt`

## Service 2: Agent Orchestration Service

### Purpose
To manage agent profiles, configurations, and coordination logic separately from the main application.

### Technical Specifications
- **Framework**: FastAPI
- **Protocol**: RESTful HTTP
- **Database**: PostgreSQL for agent profiles
- **Communication**: Redis pub/sub for status updates
- **Endpoints**:
  - `GET /agents` - List all agents
  - `POST /agents` - Create new agent
  - `GET /agents/{agent_id}` - Get agent details
  - `PUT /agents/{agent_id}` - Update agent
  - `DELETE /agents/{agent_id}` - Remove agent
  - `POST /agents/{agent_id}/command` - Send command to agent

### Data Models
- **Agent Profile**:
  - `id` (UUID)
  - `name` (string)
  - `description` (string)
  - `capabilities` (array of strings)
  - `status` (enum: active, inactive, busy)
  - `last_updated` (timestamp)

### Dependencies
- `fastapi`
- `sqlalchemy`
- `psycopg2`
- `redis`

## Service 3: Voice Processing Service

### Purpose
To handle all voice-related functionality including speech-to-text and text-to-speech processing.

### Technical Specifications
- **Framework**: FastAPI
- **Protocol**: RESTful HTTP
- **Audio Processing**: Google Cloud Speech-to-Text API
- **Text-to-Speech**: Google Cloud Text-to-Speech API
- **Communication**: Redis pub/sub for event notifications
- **Endpoints**:
  - `POST /transcribe` - Convert speech to text
  - `POST /synthesize` - Convert text to speech
  - `POST /voice-command` - Process voice command

### Dependencies
- `fastapi`
- `google-cloud-speech`
- `google-cloud-texttospeech`
- `redis`

## Service 4: Zapier Integration Service

### Purpose
To handle Zapier webhook processing and integration logic separately from the main application.

### Technical Specifications
- **Framework**: FastAPI
- **Protocol**: RESTful HTTP
- **Event Queue**: Redis for queuing incoming events
- **Endpoints**:
  - `POST /zapier/webhook` - Handle incoming Zapier webhooks
  - `POST /zapier/trigger` - Trigger outgoing Zapier events

### Data Flow
1. Zapier sends webhook to service
2. Service validates and processes webhook
3. Events are queued in Redis
4. Main application processes events from queue

### Dependencies
- `fastapi`
- `redis`
- `requests`

## Deployment Configuration

### Environment Variables
Each service will require the following environment variables:
- `DATABASE_URL` - PostgreSQL connection string (for services that need it)
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - Secret key for JWT authentication (WebSocket service)
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google Cloud credentials (Voice service)

### Docker Configuration
Each service will have its own Dockerfile with specific dependencies and startup commands.

### Railway Setup
Each service will be deployed as a separate Railway project with:
- Automatic deployments from GitHub
- Environment variable configuration
- Custom domain setup
- Resource scaling configuration