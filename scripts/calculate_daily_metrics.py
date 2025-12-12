#!/usr/bin/env python3
"""
📊 Daily Metrics Calculation Cron Job
Automatically calculate and store daily metrics for dashboard performance

Run this daily via cron or scheduler to pre-calculate metrics.

Usage:
    python scripts/calculate_daily_metrics.py [--date YYYY-MM-DD] [--days N]

Examples:
    # Calculate metrics for yesterday (default)
    python scripts/calculate_daily_metrics.py

    # Calculate for specific date
    python scripts/calculate_daily_metrics.py --date 2025-12-10

    # Calculate for last 7 days
    python scripts/calculate_daily_metrics.py --days 7

VILLAIN CRON: AUTOMATED METRICS DOMINATION 😈
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal
from backend.saas.metrics_calculator import MetricsCalculator


def calculate_metrics_for_date(date: datetime):
    """Calculate metrics for a specific date"""
    print(f"📊 Calculating metrics for {date.strftime('%Y-%m-%d')}...")

    db = SessionLocal()
    try:
        calculator = MetricsCalculator(db)
        metrics = calculator.calculate_and_store_daily_metrics(date)

        print(f"✅ Metrics calculated successfully!")
        print(f"   Signups: {metrics.new_signups}")
        print(f"   DAU: {metrics.daily_active_users}")
        print(f"   MAU: {metrics.monthly_active_users}")
        print(f"   MRR: ${metrics.mrr:,.2f}")
        print(f"   ARR: ${metrics.arr:,.2f}")
        print(f"   API Calls: {metrics.api_calls_total:,}")
        print(f"   Error Rate: {metrics.error_rate}%")
        print(f"   NPS Score: {metrics.nps_score}")

        return True
    except Exception as e:
        print(f"❌ Error calculating metrics: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Calculate daily metrics for Helix dashboard"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Specific date to calculate (YYYY-MM-DD). Defaults to yesterday."
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Calculate for last N days"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force recalculation even if metrics already exist"
    )

    args = parser.parse_args()

    if args.days:
        # Calculate for multiple days
        print(f"📊 Calculating metrics for last {args.days} days...")
        end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=args.days)

        success_count = 0
        fail_count = 0

        current_date = start_date
        while current_date < end_date:
            if calculate_metrics_for_date(current_date):
                success_count += 1
            else:
                fail_count += 1
            current_date += timedelta(days=1)

        print(f"\n📊 Batch calculation complete!")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ❌ Failed: {fail_count}")

    else:
        # Calculate for single date
        if args.date:
            target_date = datetime.fromisoformat(args.date)
        else:
            # Default to yesterday
            target_date = datetime.utcnow() - timedelta(days=1)

        target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)

        success = calculate_metrics_for_date(target_date)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
