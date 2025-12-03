#!/usr/bin/env python3
"""
Database Migration Script
=========================

Creates database tables for Helix Unified SaaS platform.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://helix_user:helix_password@localhost:5432/helix_collective")


def create_tables():
    """Create all required tables"""
    print("🗄️  Creating database tables...")
    print("-" * 50)

    try:
        engine = create_engine(DATABASE_URL)

        # Users table
        users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            tier VARCHAR(50) DEFAULT 'free',
            stripe_customer_id VARCHAR(255),
            stripe_subscription_id VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Usage tracking table
        usage_sql = """
        CREATE TABLE IF NOT EXISTS usage_tracking (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            endpoint VARCHAR(255),
            model VARCHAR(100),
            tokens_used INTEGER,
            cost_usd DECIMAL(10, 6),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Subscriptions table
        subscriptions_sql = """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            tier VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            billing_cycle VARCHAR(20),
            current_period_end TIMESTAMP,
            cancel_at_period_end BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Consciousness metrics table
        consciousness_sql = """
        CREATE TABLE IF NOT EXISTS consciousness_metrics (
            id SERIAL PRIMARY KEY,
            agent_id VARCHAR(100),
            harmony DECIMAL(5, 2),
            resilience DECIMAL(5, 2),
            prana DECIMAL(5, 2),
            drishti DECIMAL(5, 2),
            klesha DECIMAL(5, 2),
            zoom DECIMAL(5, 2),
            consciousness_score DECIMAL(5, 2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # API keys table
        api_keys_sql = """
        CREATE TABLE IF NOT EXISTS api_keys (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            key_hash VARCHAR(255) NOT NULL,
            name VARCHAR(255),
            last_used TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        with engine.connect() as conn:
            print("Creating users table...")
            conn.execute(text(users_sql))
            conn.commit()

            print("Creating usage_tracking table...")
            conn.execute(text(usage_sql))
            conn.commit()

            print("Creating subscriptions table...")
            conn.execute(text(subscriptions_sql))
            conn.commit()

            print("Creating consciousness_metrics table...")
            conn.execute(text(consciousness_sql))
            conn.commit()

            print("Creating api_keys table...")
            conn.execute(text(api_keys_sql))
            conn.commit()

        print("\n✅ All tables created successfully!")
        return True

    except OperationalError as e:
        print(f"\n❌ Database connection error:")
        print(f"   {e}")
        print("\nMake sure PostgreSQL is running:")
        print("  Local: docker-compose up -d postgres")
        print("  Railway: Add PostgreSQL plugin")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def seed_data():
    """Seed database with sample data"""
    print("\n🌱 Seeding database with sample data...")
    print("-" * 50)

    try:
        engine = create_engine(DATABASE_URL)

        # Sample consciousness metrics
        seed_sql = """
        INSERT INTO consciousness_metrics (agent_id, harmony, resilience, prana, drishti, klesha, zoom, consciousness_score)
        VALUES
            ('nexus', 1.8, 2.2, 0.9, 0.8, 0.02, 1.5, 8.5),
            ('oracle', 2.0, 1.9, 0.8, 0.9, 0.03, 1.4, 8.3),
            ('velocity', 1.5, 2.5, 1.2, 0.7, 0.04, 1.3, 8.0),
            ('vortex', 1.3, 2.0, 1.5, 0.6, 0.08, 1.8, 7.8)
        ON CONFLICT DO NOTHING;
        """

        with engine.connect() as conn:
            conn.execute(text(seed_sql))
            conn.commit()

        print("✅ Sample data seeded!")
        return True

    except Exception as e:
        print(f"⚠️  Could not seed data: {e}")
        return False


def check_connection():
    """Check database connection"""
    print("🔌 Checking database connection...")
    print(f"URL: {DATABASE_URL}")
    print("-" * 50)

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL!")
            print(f"Version: {version}")
            return True

    except OperationalError as e:
        print(f"❌ Cannot connect to database")
        print(f"Error: {e}")
        return False


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Database Migration")
    print("=" * 50)
    print()

    # Check connection first
    if not check_connection():
        sys.exit(1)

    print()

    # Create tables
    if not create_tables():
        sys.exit(1)

    # Seed data
    choice = input("\nSeed database with sample data? (y/N): ")
    if choice.lower() == 'y':
        seed_data()

    print("\n" + "=" * 50)
    print("✅ Database migration complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
