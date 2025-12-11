"""
🌀 Helix Spirals Data Models
Pydantic models matching frontend TypeScript types
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


# Enums matching TypeScript types
class TriggerType(str, Enum):
    WEBHOOK = "webhook"
    SCHEDULE = "schedule"
    MANUAL = "manual"
    AGENT_EVENT = "agent_event"
    UCF_THRESHOLD = "ucf_threshold"
    DISCORD_MESSAGE = "discord_message"
    SYSTEM_EVENT = "system_event"

class ActionType(str, Enum):
    SEND_WEBHOOK = "send_webhook"
    STORE_DATA = "store_data"
    SEND_DISCORD = "send_discord"
    TRIGGER_RITUAL = "trigger_ritual"
    ALERT_AGENT = "alert_agent"
    UPDATE_UCF = "update_ucf"
    LOG_EVENT = "log_event"
    TRANSFORM_DATA = "transform_data"
    CONDITIONAL_BRANCH = "conditional_branch"
    DELAY = "delay"
    PARALLEL_EXECUTE = "parallel_execute"
    SEND_EMAIL = "send_email"

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"

class ConditionOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    REGEX_MATCH = "regex_match"
    IN_LIST = "in_list"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"

class LogicalOperator(str, Enum):
    AND = "AND"
    OR = "OR"

class UCFMetric(str, Enum):
    HARMONY = "harmony"
    RESILIENCE = "resilience"
    PRANA = "prana"
    DRISHTI = "drishti"
    KLESHA = "klesha"
    ZOOM = "zoom"

class ConsciousnessLevel(int, Enum):
    """User's consciousness level system (1-10)"""
    DORMANT = 1
    STIRRING = 2
    AWAKENING = 3
    AWARE = 4
    CONSCIOUS = 5
    EXPANDING = 6
    FLOWING = 7
    UNIFIED = 8
    TRANSCENDENT = 9
    OMNISCIENT = 10

# Condition Model
class Condition(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    field: str
    operator: ConditionOperator
    value: Any
    logical_operator: Optional[LogicalOperator] = None
    nested_conditions: Optional[List['Condition']] = []

# Trigger Configuration Models
class WebhookTriggerConfig(BaseModel):
    type: str = "webhook"
    endpoint: Optional[str] = None
    method: Optional[str] = "POST"
    headers: Optional[Dict[str, str]] = {}
    signature_key: Optional[str] = None
    allowed_ips: Optional[List[str]] = []

class ScheduleTriggerConfig(BaseModel):
    type: str = "schedule"
    cron: Optional[str] = None
    interval: Optional[int] = None  # milliseconds
    timezone: Optional[str] = "UTC"
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class AgentEventTriggerConfig(BaseModel):
    type: str = "agent_event"
    agent_name: str
    event_types: List[str]
    filters: Optional[Dict[str, Any]] = {}

class UCFThresholdTriggerConfig(BaseModel):
    type: str = "ucf_threshold"
    metric: UCFMetric
    operator: str  # above, below, equals
    threshold: float
    check_interval: Optional[int] = 60000  # milliseconds

class DiscordMessageTriggerConfig(BaseModel):
    type: str = "discord_message"
    channel_id: Optional[str] = None
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    message_pattern: Optional[str] = None

class SystemEventTriggerConfig(BaseModel):
    type: str = "system_event"
    event_name: str
    source: Optional[str] = None

class ManualTriggerConfig(BaseModel):
    type: str = "manual"
    requires_auth: Optional[bool] = False
    allowed_users: Optional[List[str]] = []

# Trigger Model
class Trigger(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: TriggerType
    name: str
    description: Optional[str] = None
    enabled: bool = True
    config: Union[
        WebhookTriggerConfig,
        ScheduleTriggerConfig,
        AgentEventTriggerConfig,
        UCFThresholdTriggerConfig,
        DiscordMessageTriggerConfig,
        SystemEventTriggerConfig,
        ManualTriggerConfig
    ]
    conditions: Optional[List[Condition]] = []
    metadata: Optional[Dict[str, Any]] = {}

# Action Configuration Models
class SendWebhookConfig(BaseModel):
    type: str = "send_webhook"
    url: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = {}
    body: Optional[Any] = None
    authentication: Optional[Dict[str, str]] = None

class StoreDataConfig(BaseModel):
    type: str = "store_data"
    storage_type: str  # local, database, cache, file
    key: str
    value: Optional[Any] = None
    ttl: Optional[int] = None  # seconds
    encrypt: Optional[bool] = False

class SendDiscordConfig(BaseModel):
    type: str = "send_discord"
    webhook_url: Optional[str] = None
    channel_id: Optional[str] = None
    message_type: str = "text"  # text, embed, file
    content: Optional[str] = None
    embed: Optional[Dict[str, Any]] = None

class TriggerRitualConfig(BaseModel):
    type: str = "trigger_ritual"
    ritual_name: str
    parameters: Optional[Dict[str, Any]] = {}
    wait_for_completion: Optional[bool] = False

class AlertAgentConfig(BaseModel):
    type: str = "alert_agent"
    agent_name: str
    alert_level: str  # info, warning, error, critical
    message: str
    metadata: Optional[Dict[str, Any]] = {}

class UpdateUCFConfig(BaseModel):
    type: str = "update_ucf"
    metric: UCFMetric
    operation: str  # set, increment, decrement, multiply
    value: float

class LogEventConfig(BaseModel):
    type: str = "log_event"
    level: str  # debug, info, warning, error
    message: str
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class TransformDataConfig(BaseModel):
    type: str = "transform_data"
    transformations: List[Dict[str, Any]]

class ConditionalBranchConfig(BaseModel):
    type: str = "conditional_branch"
    conditions: List[Condition]
    true_branch: List['Action']
    false_branch: Optional[List['Action']] = []

class DelayConfig(BaseModel):
    type: str = "delay"
    duration: int  # milliseconds

class ParallelExecuteConfig(BaseModel):
    type: str = "parallel_execute"
    actions: List['Action']
    wait_for_all: Optional[bool] = True

class SendEmailConfig(BaseModel):
    type: str = "send_email"
    to: List[str]
    subject: str
    body: str
    is_html: Optional[bool] = False
    cc: Optional[List[str]] = []
    bcc: Optional[List[str]] = []

# Retry Configuration
class RetryConfig(BaseModel):
    max_attempts: int = 3
    backoff_strategy: str = "exponential"  # fixed, exponential, linear
    initial_delay: int = 1000  # milliseconds
    max_delay: Optional[int] = 60000
    retry_on: Optional[List[str]] = []  # error codes

# Action Model
class Action(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ActionType
    name: str
    description: Optional[str] = None
    config: Union[
        SendWebhookConfig,
        StoreDataConfig,
        SendDiscordConfig,
        TriggerRitualConfig,
        AlertAgentConfig,
        UpdateUCFConfig,
        LogEventConfig,
        TransformDataConfig,
        ConditionalBranchConfig,
        DelayConfig,
        ParallelExecuteConfig,
        SendEmailConfig
    ]
    conditions: Optional[List[Condition]] = []
    retry_config: Optional[RetryConfig] = None
    timeout: Optional[int] = 30000  # milliseconds
    continue_on_error: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = {}

# Variable Definition
class Variable(BaseModel):
    name: str
    type: str  # string, number, boolean, object, array
    default_value: Optional[Any] = None
    required: Optional[bool] = False
    description: Optional[str] = None
    source: Optional[str] = "static"  # trigger, action, environment, static

# Rate Limiting
class RateLimitConfig(BaseModel):
    max_executions: int
    window_ms: int
    strategy: str = "sliding"  # sliding, fixed

# Scheduling
class SchedulingConfig(BaseModel):
    priority: str = "normal"  # low, normal, high, critical
    max_concurrent: Optional[int] = None
    queue_strategy: Optional[str] = "fifo"  # fifo, lifo, priority

# Security
class SecurityConfig(BaseModel):
    requires_auth: Optional[bool] = False
    allowed_users: Optional[List[str]] = []
    allowed_roles: Optional[List[str]] = []
    webhook_signature: Optional[Dict[str, Any]] = None
    ip_whitelist: Optional[List[str]] = []
    rate_limit: Optional[RateLimitConfig] = None

# Main Spiral Model
class Spiral(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    enabled: bool = True
    tags: Optional[List[str]] = []
    trigger: Trigger
    actions: List[Action]
    variables: Optional[List[Variable]] = []
    rate_limiting: Optional[RateLimitConfig] = None
    scheduling: Optional[SchedulingConfig] = None
    security: Optional[SecurityConfig] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=lambda: {
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    
    # Support for user's consciousness level system
    consciousness_level: Optional[ConsciousnessLevel] = None
    
    # Support for 14-agent system
    assigned_agents: Optional[List[str]] = []

# Execution Models
class ExecutionLog(BaseModel):
    timestamp: str
    level: str  # info, warning, error
    message: str
    action_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class ExecutionError(BaseModel):
    message: str
    stack: Optional[str] = None
    action_id: Optional[str] = None

class ExecutionContext(BaseModel):
    spiral_id: str
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trigger: Dict[str, Any]
    variables: Dict[str, Any] = {}
    logs: List[ExecutionLog] = []
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    current_action: Optional[str] = None
    error: Optional[ExecutionError] = None
    metrics: Optional[Dict[str, Any]] = {}
    
    # UCF tracking
    ucf_impact: Optional[Dict[str, float]] = {}

# API Request/Response Models
class WebhookPayload(BaseModel):
    spiral_id: str
    method: str
    headers: Dict[str, str]
    body: Any
    query_params: Dict[str, str]
    client_ip: Optional[str] = None

class SpiralCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    trigger: Dict[str, Any]
    actions: List[Dict[str, Any]]
    enabled: bool = True
    tags: Optional[List[str]] = []
    variables: Optional[List[Dict[str, Any]]] = []
    consciousness_level: Optional[int] = None

class SpiralUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    trigger: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[str]] = None

class ExecutionRequest(BaseModel):
    trigger_data: Optional[Dict[str, Any]] = {}
    variables: Optional[Dict[str, Any]] = {}

class ExecutionResponse(BaseModel):
    execution_id: str
    spiral_id: str
    status: ExecutionStatus
    started_at: str
    completed_at: Optional[str] = None
    logs: Optional[List[ExecutionLog]] = []

class SpiralStatistics(BaseModel):
    total_spirals: int
    enabled_spirals: int
    total_executions: int
    successful_executions: int
    failed_executions: int
    average_execution_time_ms: float
    last_execution: Optional[str] = None
    top_spirals: List[Dict[str, Any]] = []

# Template Models for Zapier Replacement
class SpiralTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    icon: Optional[str] = None
    spiral: Spiral
    zapier_equivalent: Optional[str] = None
    steps_consolidated: Optional[int] = None

# Forward reference update
Condition.model_rebuild()
Action.model_rebuild()
ConditionalBranchConfig.model_rebuild()
ParallelExecuteConfig.model_rebuild()