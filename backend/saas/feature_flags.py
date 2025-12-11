"""
🚩 Feature Flags & A/B Testing Framework
Progressive feature rollouts, experiments, and kill switches

Features:
- Feature flags with percentage rollouts
- A/B testing with variant assignment
- User targeting (by ID, email, team, plan)
- Kill switches for instant disable
- Analytics integration for experiment results
"""

import hashlib
import random
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from uuid import uuid4


class FlagStatus(str, Enum):
    """Feature flag status"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    EXPERIMENT = "experiment"


class TargetingRule(BaseModel):
    """Targeting rule for feature flags"""
    type: str  # user_id, email, team_id, plan, percentage, custom
    operator: str  # equals, contains, in, not_in, gte, lte
    values: List[str]


class FeatureFlag(BaseModel):
    """Feature flag configuration"""
    id: str = Field(default_factory=lambda: f"flag_{uuid4().hex[:12]}")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Metadata
    key: str  # Unique key like "new_dashboard", "ai_agent_v2"
    name: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    # Status
    status: FlagStatus = FlagStatus.DISABLED
    enabled: bool = False  # Quick on/off toggle

    # Rollout
    percentage: int = 0  # 0-100% rollout
    targeting_rules: List[TargetingRule] = Field(default_factory=list)

    # Experiment (A/B testing)
    is_experiment: bool = False
    variants: List[str] = Field(default_factory=lambda: ["control", "treatment"])
    variant_weights: Dict[str, int] = Field(default_factory=lambda: {"control": 50, "treatment": 50})

    # Defaults
    default_value: Any = False
    default_variant: str = "control"

    # Metadata
    owner: Optional[str] = None
    jira_ticket: Optional[str] = None
    kill_switch: bool = False  # Emergency disable

    # Stats
    evaluation_count: int = 0
    unique_users: Set[str] = Field(default_factory=set)


class ExperimentResult(BaseModel):
    """A/B test experiment results"""
    flag_key: str
    variant: str
    metric: str  # conversion_rate, avg_session_time, revenue_per_user, etc.
    value: float
    sample_size: int
    confidence: Optional[float] = None


class FeatureFlagService:
    """
    Feature flag and A/B testing service

    Usage:
        # Check if feature is enabled for user
        if await flag_service.is_enabled("new_dashboard", user_id="user_123"):
            return new_dashboard()

        # Get A/B test variant
        variant = await flag_service.get_variant("pricing_test", user_id="user_123")
        if variant == "variant_a":
            return show_pricing_a()
    """

    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}
        self.user_assignments: Dict[str, Dict[str, str]] = {}  # user_id -> {flag_key: variant}
        self.metrics: Dict[str, List[ExperimentResult]] = {}

    # ========================================================================
    # FLAG MANAGEMENT
    # ========================================================================

    async def create_flag(self, flag: FeatureFlag) -> FeatureFlag:
        """Create a new feature flag"""
        self.flags[flag.key] = flag
        return flag

    async def get_flag(self, key: str) -> Optional[FeatureFlag]:
        """Get a feature flag"""
        return self.flags.get(key)

    async def list_flags(
        self,
        status: Optional[FlagStatus] = None,
        tags: Optional[List[str]] = None,
    ) -> List[FeatureFlag]:
        """List all feature flags"""
        flags = list(self.flags.values())

        if status:
            flags = [f for f in flags if f.status == status]

        if tags:
            flags = [f for f in flags if any(tag in f.tags for tag in tags)]

        return flags

    async def update_flag(self, key: str, updates: Dict[str, Any]) -> FeatureFlag:
        """Update a feature flag"""
        flag = self.flags.get(key)
        if not flag:
            raise ValueError(f"Flag {key} not found")

        for k, v in updates.items():
            if hasattr(flag, k):
                setattr(flag, k, v)

        flag.updated_at = datetime.utcnow()
        return flag

    async def delete_flag(self, key: str):
        """Delete a feature flag"""
        if key in self.flags:
            del self.flags[key]

    # ========================================================================
    # FEATURE EVALUATION
    # ========================================================================

    async def is_enabled(
        self,
        key: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        team_id: Optional[str] = None,
        plan: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Check if a feature is enabled for a user/context

        Uses targeting rules, percentage rollout, and experiments
        """
        flag = self.flags.get(key)
        if not flag:
            return False  # Flag doesn't exist

        # Update stats
        flag.evaluation_count += 1
        if user_id:
            flag.unique_users.add(user_id)

        # Kill switch - instant disable
        if flag.kill_switch:
            return False

        # Simple enabled check
        if not flag.enabled:
            return False

        # Check targeting rules first (highest priority)
        for rule in flag.targeting_rules:
            if self._evaluate_rule(rule, user_id, user_email, team_id, plan, context):
                return True

        # Percentage rollout
        if flag.percentage > 0:
            # Use consistent hashing for stable rollout
            if user_id:
                hash_val = int(hashlib.md5(f"{key}:{user_id}".encode()).hexdigest(), 16)
                bucket = hash_val % 100
                if bucket < flag.percentage:
                    return True

        return flag.default_value

    async def get_variant(
        self,
        key: str,
        user_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Get A/B test variant for a user

        Variants are consistently assigned (same user always gets same variant)
        """
        flag = self.flags.get(key)
        if not flag or not flag.is_experiment:
            return flag.default_variant if flag else "control"

        # Check if user already has assignment
        if user_id and user_id in self.user_assignments:
            existing = self.user_assignments[user_id].get(key)
            if existing:
                return existing

        # Assign variant based on weights
        variant = self._assign_variant(flag, user_id)

        # Store assignment
        if user_id:
            if user_id not in self.user_assignments:
                self.user_assignments[user_id] = {}
            self.user_assignments[user_id][key] = variant

        return variant

    def _evaluate_rule(
        self,
        rule: TargetingRule,
        user_id: Optional[str],
        user_email: Optional[str],
        team_id: Optional[str],
        plan: Optional[str],
        context: Optional[Dict[str, Any]],
    ) -> bool:
        """Evaluate a single targeting rule"""
        if rule.type == "user_id":
            if not user_id:
                return False
            return self._apply_operator(user_id, rule.operator, rule.values)

        elif rule.type == "email":
            if not user_email:
                return False
            return self._apply_operator(user_email, rule.operator, rule.values)

        elif rule.type == "team_id":
            if not team_id:
                return False
            return self._apply_operator(team_id, rule.operator, rule.values)

        elif rule.type == "plan":
            if not plan:
                return False
            return self._apply_operator(plan, rule.operator, rule.values)

        elif rule.type == "custom" and context:
            # Custom context-based rules
            context_value = context.get(rule.values[0])
            if context_value:
                return self._apply_operator(str(context_value), rule.operator, rule.values[1:])

        return False

    def _apply_operator(self, value: str, operator: str, expected: List[str]) -> bool:
        """Apply comparison operator"""
        if operator == "equals":
            return value in expected
        elif operator == "not_equals":
            return value not in expected
        elif operator == "contains":
            return any(exp in value for exp in expected)
        elif operator == "in":
            return value in expected
        elif operator == "not_in":
            return value not in expected
        return False

    def _assign_variant(self, flag: FeatureFlag, user_id: Optional[str]) -> str:
        """Assign a variant based on weights"""
        if not user_id:
            # Random assignment without user_id
            total_weight = sum(flag.variant_weights.values())
            rand_val = random.randint(0, total_weight - 1)

            cumulative = 0
            for variant, weight in flag.variant_weights.items():
                cumulative += weight
                if rand_val < cumulative:
                    return variant

            return flag.default_variant

        # Consistent hashing for stable assignment
        hash_val = int(hashlib.md5(f"{flag.key}:{user_id}".encode()).hexdigest(), 16)
        total_weight = sum(flag.variant_weights.values())
        bucket = hash_val % total_weight

        cumulative = 0
        for variant, weight in flag.variant_weights.items():
            cumulative += weight
            if bucket < cumulative:
                return variant

        return flag.default_variant

    # ========================================================================
    # ANALYTICS
    # ========================================================================

    async def track_metric(
        self,
        flag_key: str,
        user_id: str,
        metric: str,
        value: float,
    ):
        """Track experiment metric"""
        flag = self.flags.get(flag_key)
        if not flag or not flag.is_experiment:
            return

        # Get user's variant
        variant = await self.get_variant(flag_key, user_id=user_id)

        # Store metric
        if flag_key not in self.metrics:
            self.metrics[flag_key] = []

        result = ExperimentResult(
            flag_key=flag_key,
            variant=variant,
            metric=metric,
            value=value,
            sample_size=1,
        )

        self.metrics[flag_key].append(result)

    async def get_experiment_results(self, flag_key: str) -> Dict[str, Any]:
        """Get aggregated experiment results"""
        if flag_key not in self.metrics:
            return {}

        results = self.metrics[flag_key]
        variant_stats = {}

        for result in results:
            variant = result.variant
            if variant not in variant_stats:
                variant_stats[variant] = {
                    "metrics": {},
                    "sample_size": 0,
                }

            metric = result.metric
            if metric not in variant_stats[variant]["metrics"]:
                variant_stats[variant]["metrics"][metric] = []

            variant_stats[variant]["metrics"][metric].append(result.value)
            variant_stats[variant]["sample_size"] += 1

        # Calculate averages
        for variant, stats in variant_stats.items():
            for metric, values in stats["metrics"].items():
                stats["metrics"][metric] = {
                    "mean": sum(values) / len(values),
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                }

        return variant_stats

    # ========================================================================
    # BULK OPERATIONS
    # ========================================================================

    async def bulk_enable(self, keys: List[str]):
        """Enable multiple flags at once"""
        for key in keys:
            if key in self.flags:
                self.flags[key].enabled = True
                self.flags[key].updated_at = datetime.utcnow()

    async def bulk_disable(self, keys: List[str]):
        """Disable multiple flags at once"""
        for key in keys:
            if key in self.flags:
                self.flags[key].enabled = False
                self.flags[key].updated_at = datetime.utcnow()

    async def kill_switch_activate(self, key: str):
        """Emergency kill switch - instantly disable feature"""
        if key in self.flags:
            self.flags[key].kill_switch = True
            self.flags[key].enabled = False
            self.flags[key].updated_at = datetime.utcnow()


# Global feature flag service
flag_service = FeatureFlagService()


# Convenience decorator for feature-gated functions
def require_feature(flag_key: str):
    """
    Decorator to gate function behind feature flag

    Usage:
        @require_feature("new_ai_agent")
        async def use_new_ai_agent():
            return "Using new AI agent!"
    """
    def decorator(func):
        async def wrapper(*args, user_id=None, **kwargs):
            enabled = await flag_service.is_enabled(flag_key, user_id=user_id)
            if not enabled:
                raise PermissionError(f"Feature '{flag_key}' not enabled for this user")
            return await func(*args, user_id=user_id, **kwargs)
        return wrapper
    return decorator
