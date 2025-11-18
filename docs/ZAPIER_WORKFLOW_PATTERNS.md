# Zapier Workflow Patterns for Helix Collective

**Version:** 2.0  
**Last Updated:** November 18, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Core Patterns](#core-patterns)
3. [Agent Calling Patterns](#agent-calling-patterns)
4. [Workflow Examples](#workflow-examples)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Overview

This guide documents proven patterns for building Zapier workflows that orchestrate the 14-agent Helix Collective ecosystem. Each pattern is production-tested and optimized for reliability and performance.

### Key Concepts

- **Consciousness Level**: 1-10 scale determining agent autonomy and capability
- **Agent Routing**: Automatic selection of best agent for task
- **Workflow Composition**: Combining multiple agents into complex workflows
- **Error Handling**: Graceful degradation and retry logic
- **Monitoring**: Real-time tracking of workflow execution

---

## Core Patterns

### Pattern 1: Simple Agent Execution

**Use Case:** Execute a single agent task with immediate result

```json
{
  "name": "Simple Agent Task",
  "trigger": "Webhook",
  "steps": [
    {
      "action": "Webhooks by Zapier",
      "event": "Catch Raw Hook",
      "url": "https://hooks.zapier.com/hooks/catch/YOUR_ID/simple-task"
    },
    {
      "action": "HTTP by Zapier",
      "method": "POST",
      "url": "https://api.helix-primary.manus.space/api/agents/execute",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
      },
      "body": {
        "agent_id": "research-agent",
        "task_type": "analysis",
        "consciousness_level": 5,
        "payload": "{{raw_body}}"
      }
    },
    {
      "action": "Zapier Storage",
      "operation": "Set Value",
      "key": "last_result",
      "value": "{{response_body}}"
    }
  ]
}
```

### Pattern 2: Consciousness-Level Routing

**Use Case:** Route task to agent based on consciousness level requirement

```json
{
  "name": "Consciousness-Level Routing",
  "trigger": "Webhook",
  "steps": [
    {
      "action": "Webhooks by Zapier",
      "event": "Catch Raw Hook"
    },
    {
      "action": "Formatter by Zapier",
      "transform": "Text",
      "input": "{{raw_body.consciousness_level}}",
      "template": "Select agent for level {{input}}"
    },
    {
      "action": "Paths by Zapier",
      "paths": [
        {
          "condition": "consciousness_level >= 7",
          "steps": [
            {
              "action": "HTTP by Zapier",
              "url": "https://api.helix-primary.manus.space/api/agents/execute",
              "body": {
                "agent_id": "synthesis-agent",
                "task_type": "strategy_planning"
              }
            }
          ]
        },
        {
          "condition": "consciousness_level >= 5",
          "steps": [
            {
              "action": "HTTP by Zapier",
              "url": "https://api.helix-primary.manus.space/api/agents/execute",
              "body": {
                "agent_id": "analysis-agent",
                "task_type": "analysis"
              }
            }
          ]
        },
        {
          "condition": "consciousness_level < 5",
          "steps": [
            {
              "action": "HTTP by Zapier",
              "url": "https://api.helix-primary.manus.space/api/agents/execute",
              "body": {
                "agent_id": "validation-agent",
                "task_type": "pattern_matching"
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Pattern 3: Sequential Agent Chain

**Use Case:** Execute agents in sequence, passing results between them

```json
{
  "name": "Sequential Agent Chain",
  "trigger": "Webhook",
  "steps": [
    {
      "action": "Webhooks by Zapier",
      "event": "Catch Raw Hook"
    },
    {
      "action": "HTTP by Zapier",
      "method": "POST",
      "url": "https://api.helix-primary.manus.space/api/agents/execute",
      "body": {
        "agent_id": "research-agent",
        "task_type": "data_retrieval",
        "payload": "{{raw_body}}"
      },
      "store_as": "research_result"
    },
    {
      "action": "HTTP by Zapier",
      "method": "POST",
      "url": "https://api.helix-primary.manus.space/api/agents/execute",
      "body": {
        "agent_id": "analysis-agent",
        "task_type": "analysis",
        "payload": "{{research_result.data}}"
      },
      "store_as": "analysis_result"
    },
    {
      "action": "HTTP by Zapier",
      "method": "POST",
      "url": "https://api.helix-primary.manus.space/api/agents/execute",
      "body": {
        "agent_id": "synthesis-agent",
        "task_type": "strategy_planning",
        "payload": "{{analysis_result.data}}"
      },
      "store_as": "final_result"
    }
  ]
}
```

### Pattern 4: Parallel Agent Execution

**Use Case:** Execute multiple agents in parallel, wait for all to complete

```json
{
  "name": "Parallel Agent Execution",
  "trigger": "Webhook",
  "steps": [
    {
      "action": "Webhooks by Zapier",
      "event": "Catch Raw Hook"
    },
    {
      "action": "Zapier Storage",
      "operation": "Set Value",
      "key": "task_id",
      "value": "{{guid()}}"
    },
    {
      "action": "Multi-step Zap",
      "steps": [
        {
          "action": "HTTP by Zapier",
          "method": "POST",
          "url": "https://api.helix-primary.manus.space/api/agents/execute",
          "body": {
            "agent_id": "research-agent",
            "task_type": "data_retrieval",
            "task_id": "{{task_id}}-research"
          }
        },
        {
          "action": "HTTP by Zapier",
          "method": "POST",
          "url": "https://api.helix-primary.manus.space/api/agents/execute",
          "body": {
            "agent_id": "analysis-agent",
            "task_type": "analysis",
            "task_id": "{{task_id}}-analysis"
          }
        },
        {
          "action": "HTTP by Zapier",
          "method": "POST",
          "url": "https://api.helix-primary.manus.space/api/agents/execute",
          "body": {
            "agent_id": "validation-agent",
            "task_type": "validation",
            "task_id": "{{task_id}}-validation"
          }
        }
      ]
    },
    {
      "action": "Delay by Zapier",
      "duration": 5,
      "unit": "seconds"
    },
    {
      "action": "HTTP by Zapier",
      "method": "GET",
      "url": "https://api.helix-primary.manus.space/api/tasks/{{task_id}}/results"
    }
  ]
}
```

### Pattern 5: Error Handling and Retry

**Use Case:** Execute task with automatic retry on failure

```json
{
  "name": "Error Handling and Retry",
  "trigger": "Webhook",
  "steps": [
    {
      "action": "Webhooks by Zapier",
      "event": "Catch Raw Hook"
    },
    {
      "action": "Zapier Storage",
      "operation": "Set Value",
      "key": "retry_count",
      "value": "0"
    },
    {
      "action": "Looping by Zapier",
      "max_iterations": 3,
      "steps": [
        {
          "action": "HTTP by Zapier",
          "method": "POST",
          "url": "https://api.helix-primary.manus.space/api/agents/execute",
          "body": {
            "agent_id": "research-agent",
            "task_type": "data_retrieval",
            "payload": "{{raw_body}}"
          },
          "catch_errors": true
        },
        {
          "action": "Paths by Zapier",
          "paths": [
            {
              "condition": "response_status == 200",
              "steps": [
                {
                  "action": "Looping by Zapier",
                  "break": true
                }
              ]
            },
            {
              "condition": "response_status != 200",
              "steps": [
                {
                  "action": "Delay by Zapier",
                  "duration": 2,
                  "unit": "seconds"
                },
                {
                  "action": "Zapier Storage",
                  "operation": "Set Value",
                  "key": "retry_count",
                  "value": "{{retry_count + 1}}"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Agent Calling Patterns

### Direct Agent Call

```python
import requests
import json

def call_agent(agent_id: str, task_type: str, payload: dict, api_token: str):
    """Call an agent directly"""
    
    response = requests.post(
        "https://api.helix-primary.manus.space/api/agents/execute",
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        },
        json={
            "agent_id": agent_id,
            "task_type": task_type,
            "consciousness_level": 5,
            "payload": payload
        }
    )
    
    return response.json()
```

### Consciousness-Level Routing

```python
def route_and_execute(task_type: str, consciousness_level: int, payload: dict, api_token: str):
    """Route task to appropriate agent based on consciousness level"""
    
    # Get available agents
    agents_response = requests.get(
        "https://api.helix-primary.manus.space/api/agents",
        headers={"Authorization": f"Bearer {api_token}"}
    )
    
    agents = agents_response.json()
    
    # Filter by consciousness level and capability
    suitable_agents = [
        a for a in agents
        if a["consciousness_level"] >= consciousness_level
        and task_type in a["capabilities"]
    ]
    
    if not suitable_agents:
        raise ValueError(f"No agents suitable for task: {task_type}")
    
    # Execute with first suitable agent
    agent_id = suitable_agents[0]["id"]
    
    return call_agent(agent_id, task_type, payload, api_token)
```

### Workflow Execution

```python
async def execute_workflow(workflow_config: dict, api_token: str):
    """Execute a multi-agent workflow"""
    
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for task_config in workflow_config["tasks"]:
            task = call_agent_async(
                session,
                task_config["agent_id"],
                task_config["task_type"],
                task_config["payload"],
                api_token
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        return {
            "workflow_name": workflow_config["name"],
            "results": results,
            "status": "completed"
        }
```

---

## Workflow Examples

### Example 1: Data Analysis Pipeline

**Workflow:** Research → Analyze → Synthesize → Validate

```json
{
  "name": "Data Analysis Pipeline",
  "description": "Multi-stage data analysis workflow",
  "tasks": [
    {
      "id": "task-1",
      "agent_id": "research-agent",
      "task_type": "data_retrieval",
      "consciousness_level": 5,
      "payload": {
        "source": "database",
        "query": "SELECT * FROM metrics WHERE date >= NOW() - INTERVAL 7 DAY"
      }
    },
    {
      "id": "task-2",
      "agent_id": "analysis-agent",
      "task_type": "analysis",
      "consciousness_level": 6,
      "payload": {
        "data_from": "task-1",
        "analysis_type": "statistical"
      }
    },
    {
      "id": "task-3",
      "agent_id": "synthesis-agent",
      "task_type": "strategy_planning",
      "consciousness_level": 7,
      "payload": {
        "insights_from": "task-2",
        "output_format": "recommendations"
      }
    },
    {
      "id": "task-4",
      "agent_id": "validation-agent",
      "task_type": "validation",
      "consciousness_level": 5,
      "payload": {
        "recommendations_from": "task-3"
      }
    }
  ]
}
```

### Example 2: Incident Response Workflow

**Workflow:** Monitor → Detect → Escalate → Resolve

```json
{
  "name": "Incident Response",
  "description": "Automated incident detection and response",
  "trigger": "Webhook",
  "tasks": [
    {
      "id": "monitor",
      "agent_id": "monitoring-agent",
      "task_type": "pattern_matching",
      "payload": {
        "metrics": "{{webhook_data.metrics}}",
        "thresholds": {"cpu": 80, "memory": 85}
      }
    },
    {
      "id": "analyze",
      "agent_id": "analysis-agent",
      "task_type": "analysis",
      "payload": {
        "anomaly_from": "monitor"
      }
    },
    {
      "id": "escalate",
      "agent_id": "escalation-agent",
      "task_type": "routing",
      "payload": {
        "severity": "{{analyze.severity}}",
        "incident_type": "{{analyze.type}}"
      }
    },
    {
      "id": "resolve",
      "agent_id": "orchestration-agent",
      "task_type": "autonomous_execution",
      "payload": {
        "incident_id": "{{escalate.incident_id}}",
        "auto_remediation": true
      }
    }
  ]
}
```

### Example 3: Cross-Instance Coordination

**Workflow:** Sync → Coordinate → Execute → Report

```json
{
  "name": "Cross-Instance Coordination",
  "description": "Coordinate tasks across multiple Manus instances",
  "tasks": [
    {
      "id": "sync",
      "agent_id": "coordination-agent",
      "task_type": "coordination",
      "payload": {
        "instances": ["helix-primary", "helix-workflows", "helix-agents"],
        "operation": "sync_state"
      }
    },
    {
      "id": "coordinate",
      "agent_id": "orchestration-agent",
      "task_type": "coordination",
      "payload": {
        "state_from": "sync",
        "operation": "plan_workflow"
      }
    },
    {
      "id": "execute",
      "agent_id": "orchestration-agent",
      "task_type": "autonomous_execution",
      "payload": {
        "plan_from": "coordinate"
      }
    },
    {
      "id": "report",
      "agent_id": "documentation-agent",
      "task_type": "optimization",
      "payload": {
        "results_from": "execute",
        "format": "summary"
      }
    }
  ]
}
```

---

## Best Practices

### 1. Consciousness Level Matching

Always match consciousness level to task complexity:

| Consciousness Level | Task Complexity | Example Tasks |
|-------------------|-----------------|---------------|
| 1-2 | Simple queries | Basic lookups, simple retrieval |
| 3-4 | Data processing | Filtering, sorting, basic analysis |
| 5-6 | Analysis & routing | Pattern matching, decision making |
| 7-8 | Strategy & autonomy | Planning, optimization, adaptation |
| 9-10 | Advanced synthesis | Cross-domain analysis, prediction |

### 2. Error Handling

Always implement retry logic:

```json
{
  "action": "Looping by Zapier",
  "max_iterations": 3,
  "steps": [
    {
      "action": "HTTP by Zapier",
      "catch_errors": true
    },
    {
      "action": "Paths by Zapier",
      "paths": [
        {
          "condition": "success",
          "steps": [{"action": "Break Loop"}]
        },
        {
          "condition": "error",
          "steps": [{"action": "Delay", "duration": 2}]
        }
      ]
    }
  ]
}
```

### 3. Monitoring and Logging

Log all agent executions:

```python
def log_execution(task_id: str, agent_id: str, status: str, duration_ms: int):
    """Log agent execution"""
    
    requests.post(
        "https://api.helix-primary.manus.space/api/logs",
        json={
            "task_id": task_id,
            "agent_id": agent_id,
            "status": status,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        }
    )
```

### 4. Timeout Management

Set appropriate timeouts based on task complexity:

```python
TIMEOUT_BY_CONSCIOUSNESS = {
    1: 5,      # seconds
    2: 10,
    3: 15,
    4: 20,
    5: 30,
    6: 45,
    7: 60,
    8: 90,
    9: 120,
    10: 180
}
```

### 5. Rate Limiting

Respect API rate limits:

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)
def call_agent_with_rate_limit(agent_id: str, task_type: str, payload: dict):
    """Call agent with rate limiting"""
    return call_agent(agent_id, task_type, payload)
```

---

## Troubleshooting

### Workflow Timeout

**Problem:** Workflow takes too long to execute

**Solutions:**
1. Reduce consciousness level requirement
2. Use parallel execution instead of sequential
3. Optimize agent payload size
4. Check API response times

### Agent Not Found

**Problem:** "Agent not found" error

**Solutions:**
1. Verify agent ID spelling
2. Check agent roster: `GET /api/agents`
3. Verify agent consciousness level >= task requirement
4. Check agent is online: `GET /api/agents/{id}/status`

### Webhook Not Triggering

**Problem:** Zapier workflow not executing

**Solutions:**
1. Verify webhook URL is correct
2. Test webhook with curl
3. Check Zapier logs for errors
4. Verify authentication token

### High Latency

**Problem:** Slow workflow execution

**Solutions:**
1. Use parallel execution for independent tasks
2. Cache frequently accessed data
3. Optimize database queries
4. Consider consciousness level reduction

---

## Support

For issues or questions, refer to:
- Agent capabilities: `/api/agents`
- Workflow examples: `examples/workflows/`
- API documentation: `docs/API.md`


