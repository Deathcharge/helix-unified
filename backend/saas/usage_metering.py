"""
🌀 Helix Collective v17.1 - SaaS Usage Metering & Billing Accumulator
backend/saas/usage_metering.py

Track consumption for usage-based billing:
- API call counting
- System monitoring count
- Alert delivery tracking
- Data export tracking
- Auto-billing accumulation

Author: Claude (Automation)
Version: 17.1.0
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# USAGE METERING
# ============================================================================


class UsageMeter:
    """Tracks user consumption for billing."""

    def __init__(self):
        self.usage_file = Path("Helix/state/saas_usage.jsonl")
        self.usage_file.parent.mkdir(parents=True, exist_ok=True)

    def record_usage(
        self,
        user_id: str,
        metric_type: str,
        quantity: int = 1,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record usage metric."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "metric_type": metric_type,
            "quantity": quantity,
            "metadata": metadata or {},
        }

        with open(self.usage_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_usage_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get usage summary for user."""
        if not self.usage_file.exists():
            return {"api_calls": 0, "systems": 0, "alerts": 0, "exports": 0}

        cutoff = datetime.utcnow() - timedelta(days=days)
        metrics = {"api_calls": 0, "systems": 0, "alerts": 0, "exports": 0}

        with open(self.usage_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                entry = json.loads(line)
                if entry.get("user_id") != user_id:
                    continue

                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if ts < cutoff:
                    continue

                metric_type = entry.get("metric_type")
                quantity = entry.get("quantity", 1)

                if metric_type in metrics:
                    metrics[metric_type] += quantity

        return metrics

    def get_billing_period_usage(self, user_id: str) -> Dict[str, Any]:
        """Get usage for current billing period (30 days)."""
        return self.get_usage_summary(user_id, days=30)


# ============================================================================
# BILLING CALCULATOR
# ============================================================================


class BillingCalculator:
    """Calculates charges based on usage."""

    # Usage-based pricing
    PRICING = {
        "free": {
            "api_calls_included": 1000,
            "systems_included": 1,
            "alerts_included": 0,
            "overage_cost_per_1000_calls": 0,  # Free tier: no overages
        },
        "pro": {
            "api_calls_included": 100000,
            "systems_included": 10,
            "alerts_included": 1000,
            "overage_cost_per_1000_calls": 0.50,  # $0.50 per 1K calls
            "monthly_base": 9900,  # $99 in cents
        },
        "enterprise": {
            "api_calls_included": 10000000,
            "systems_included": 999,
            "alerts_included": 999999,
            "overage_cost_per_1000_calls": 0.10,  # $0.10 per 1K calls
            "monthly_base": 49900,  # $499 in cents
        },
    }

    @staticmethod
    def calculate_overage_charges(tier: str, api_calls_used: int) -> Dict[str, Any]:
        """Calculate overage charges for API calls."""
        pricing = BillingCalculator.PRICING.get(tier, {})

        included = pricing.get("api_calls_included", 0)
        overage_rate = pricing.get("overage_cost_per_1000_calls", 0)

        if api_calls_used <= included:
            return {
                "overage_calls": 0,
                "overage_charge_cents": 0,
                "overage_charge_dollars": 0,
            }

        overage_calls = api_calls_used - included
        overage_charge_cents = int((overage_calls / 1000) * overage_rate * 100)

        return {
            "overage_calls": overage_calls,
            "overage_charge_cents": overage_charge_cents,
            "overage_charge_dollars": round(overage_charge_cents / 100, 2),
        }

    @staticmethod
    def calculate_monthly_charge(tier: str, api_calls_used: int) -> Dict[str, Any]:
        """Calculate total monthly charge."""
        pricing = BillingCalculator.PRICING.get(tier, {})

        base_charge = pricing.get("monthly_base", 0)
        overage = BillingCalculator.calculate_overage_charges(tier, api_calls_used)

        total_cents = base_charge + overage["overage_charge_cents"]

        return {
            "tier": tier,
            "base_charge_cents": base_charge,
            "base_charge_dollars": round(base_charge / 100, 2),
            "overage_charge_cents": overage["overage_charge_cents"],
            "overage_charge_dollars": overage["overage_charge_dollars"],
            "total_charge_cents": total_cents,
            "total_charge_dollars": round(total_cents / 100, 2),
        }


# ============================================================================
# BILLING ACCUMULATOR
# ============================================================================


class BillingAccumulator:
    """Accumulates charges and generates invoices."""

    def __init__(self):
        self.meter = UsageMeter()
        self.calculator = BillingCalculator()
        self.billing_file = Path("Helix/state/saas_billing.jsonl")
        self.billing_file.parent.mkdir(parents=True, exist_ok=True)

    async def generate_monthly_invoice(self, user_id: str, email: str, tier: str) -> Dict[str, Any]:
        """Generate monthly invoice based on usage."""
        # Get usage for billing period
        usage = self.meter.get_billing_period_usage(user_id)

        # Calculate charges
        charges = self.calculator.calculate_monthly_charge(tier, usage.get("api_calls", 0))

        invoice = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "email": email,
            "tier": tier,
            "usage": usage,
            "charges": charges,
            "status": "pending_payment",
        }

        # Log invoice
        with open(self.billing_file, "a") as f:
            f.write(json.dumps(invoice) + "\n")

        logger.info(f"✅ Invoice generated: {user_id} - ${charges['total_charge_dollars']}")

        return invoice

    def get_billing_history(self, user_id: str, limit: int = 12) -> List[Dict[str, Any]]:
        """Get billing history for user."""
        if not self.billing_file.exists():
            return []

        invoices = []
        with open(self.billing_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                invoice = json.loads(line)
                if invoice.get("user_id") == user_id:
                    invoices.append(invoice)

        return invoices[-limit:]

    def get_current_monthly_projection(self, user_id: str, tier: str) -> Dict[str, Any]:
        """Get projected monthly charge for current period."""
        usage = self.meter.get_billing_period_usage(user_id)
        charges = self.calculator.calculate_monthly_charge(tier, usage.get("api_calls", 0))

        return {
            "user_id": user_id,
            "tier": tier,
            "current_usage": usage,
            "projected_charge": charges,
            "days_remaining": self._days_remaining_in_month(),
        }

    @staticmethod
    def _days_remaining_in_month() -> int:
        """Calculate days remaining in current month."""
        today = datetime.utcnow()
        next_month = today.replace(day=28) + timedelta(days=4)
        month_end = (next_month - timedelta(days=next_month.day)).day
        return month_end - today.day


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["UsageMeter", "BillingCalculator", "BillingAccumulator"]
