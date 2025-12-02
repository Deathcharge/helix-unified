"""
Environment Variable Validation & Health Checks
Validates required environment variables and API keys on startup
"""

import os
import sys
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import aiohttp
from loguru import logger


class ValidationResult:
    """Result of an environment validation check"""

    def __init__(self, passed: bool, message: str, severity: str = "error"):
        self.passed = passed
        self.message = message
        self.severity = severity  # "error", "warning", "info"
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        icon = "✅" if self.passed else "❌" if self.severity == "error" else "⚠️"
        return f"{icon} {self.message}"


class EnvironmentValidator:
    """Validates environment variables and external service connections"""

    def __init__(self):
        self.results: List[ValidationResult] = []
        self.required_vars: Dict[str, str] = {}
        self.optional_vars: Dict[str, str] = {}

    def add_required(self, var_name: str, description: str):
        """Mark a variable as required"""
        self.required_vars[var_name] = description

    def add_optional(self, var_name: str, description: str):
        """Mark a variable as optional"""
        self.optional_vars[var_name] = description

    def check_required_vars(self) -> List[ValidationResult]:
        """Check all required environment variables"""
        results = []

        for var_name, description in self.required_vars.items():
            value = os.getenv(var_name)

            if not value:
                results.append(ValidationResult(
                    passed=False,
                    message=f"Missing required variable: {var_name} ({description})",
                    severity="error"
                ))
            elif value in ["your_token_here", "your_api_key_here", "xxxxx", "changeme"]:
                results.append(ValidationResult(
                    passed=False,
                    message=f"Placeholder value detected for {var_name} - please set real value",
                    severity="error"
                ))
            else:
                # Mask sensitive values in logs
                masked_value = self._mask_value(var_name, value)
                results.append(ValidationResult(
                    passed=True,
                    message=f"{var_name} = {masked_value}",
                    severity="info"
                ))

        return results

    def check_optional_vars(self) -> List[ValidationResult]:
        """Check optional environment variables"""
        results = []

        for var_name, description in self.optional_vars.items():
            value = os.getenv(var_name)

            if not value:
                results.append(ValidationResult(
                    passed=True,
                    message=f"Optional variable not set: {var_name} ({description})",
                    severity="warning"
                ))
            else:
                masked_value = self._mask_value(var_name, value)
                results.append(ValidationResult(
                    passed=True,
                    message=f"{var_name} = {masked_value}",
                    severity="info"
                ))

        return results

    def _mask_value(self, var_name: str, value: str) -> str:
        """Mask sensitive values for logging"""
        sensitive_keywords = ['TOKEN', 'KEY', 'SECRET', 'PASSWORD', 'PASS', 'WEBHOOK']

        if any(keyword in var_name.upper() for keyword in sensitive_keywords):
            if len(value) <= 8:
                return "***"
            return f"{value[:4]}...{value[-4:]}"

        # URLs can be shown but mask query params
        if value.startswith('http'):
            return value.split('?')[0] + ('?***' if '?' in value else '')

        # Database URLs - mask password
        if 'postgresql://' in value or 'redis://' in value:
            parts = value.split('@')
            if len(parts) == 2:
                auth_parts = parts[0].split(':')
                if len(auth_parts) >= 2:
                    return f"{auth_parts[0]}:***@{parts[1]}"

        return value

    async def validate_database_connection(self, database_url: Optional[str] = None) -> ValidationResult:
        """Validate database connection"""
        db_url = database_url or os.getenv('DATABASE_URL')

        if not db_url:
            return ValidationResult(
                passed=False,
                message="DATABASE_URL not set - database features disabled",
                severity="warning"
            )

        try:
            # Try to import and connect (basic check)
            import asyncpg

            # Parse connection string
            conn = await asyncpg.connect(db_url)
            await conn.close()

            return ValidationResult(
                passed=True,
                message="Database connection successful",
                severity="info"
            )
        except ImportError:
            return ValidationResult(
                passed=True,
                message="asyncpg not installed - skipping database validation",
                severity="warning"
            )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Database connection failed: {str(e)}",
                severity="error"
            )

    async def validate_redis_connection(self, redis_url: Optional[str] = None) -> ValidationResult:
        """Validate Redis connection"""
        redis_url_val = redis_url or os.getenv('REDIS_URL')

        if not redis_url_val:
            return ValidationResult(
                passed=False,
                message="REDIS_URL not set - caching disabled",
                severity="warning"
            )

        try:
            import aioredis

            redis = await aioredis.from_url(redis_url_val)
            await redis.ping()
            await redis.close()

            return ValidationResult(
                passed=True,
                message="Redis connection successful",
                severity="info"
            )
        except ImportError:
            # Try redis-py
            try:
                import redis.asyncio as redis_async

                redis = redis_async.from_url(redis_url_val)
                await redis.ping()
                await redis.close()

                return ValidationResult(
                    passed=True,
                    message="Redis connection successful",
                    severity="info"
                )
            except ImportError:
                return ValidationResult(
                    passed=True,
                    message="redis not installed - skipping Redis validation",
                    severity="warning"
                )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Redis connection failed: {str(e)}",
                severity="error"
            )

    async def validate_perplexity_api_key(self, api_key: Optional[str] = None) -> ValidationResult:
        """Validate Perplexity API key by making a test request"""
        key = api_key or os.getenv('PERPLEXITY_API_KEY')

        if not key:
            return ValidationResult(
                passed=False,
                message="PERPLEXITY_API_KEY not set - Perplexity search features disabled",
                severity="warning"
            )

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {key}',
                    'Content-Type': 'application/json'
                }

                # Make a minimal test request
                payload = {
                    "model": "llama-3.1-8b-instruct",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10
                }

                async with session.post(
                    'https://api.perplexity.ai/chat/completions',
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 401:
                        return ValidationResult(
                            passed=False,
                            message="PERPLEXITY_API_KEY is invalid or expired",
                            severity="error"
                        )
                    elif resp.status == 403:
                        return ValidationResult(
                            passed=False,
                            message="PERPLEXITY_API_KEY access denied (quota exceeded or suspended)",
                            severity="error"
                        )
                    elif resp.status in [200, 201]:
                        return ValidationResult(
                            passed=True,
                            message="PERPLEXITY_API_KEY validated successfully",
                            severity="info"
                        )
                    else:
                        return ValidationResult(
                            passed=False,
                            message=f"Perplexity API validation returned HTTP {resp.status}",
                            severity="warning"
                        )
        except asyncio.TimeoutError:
            return ValidationResult(
                passed=False,
                message="Perplexity API validation timeout - check network connectivity",
                severity="warning"
            )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Failed to validate PERPLEXITY_API_KEY: {str(e)}",
                severity="warning"
            )

    async def validate_anthropic_api_key(self, api_key: Optional[str] = None) -> ValidationResult:
        """Validate Anthropic API key by making a test request"""
        key = api_key or os.getenv('ANTHROPIC_API_KEY')

        if not key:
            return ValidationResult(
                passed=False,
                message="ANTHROPIC_API_KEY not set - Claude features disabled",
                severity="warning"
            )

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'x-api-key': key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                }

                # Make a minimal test request
                async with session.get(
                    'https://api.anthropic.com/v1/messages',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    # Even a 400 means the key is valid (just missing required params)
                    # 401 means invalid key
                    # 403 means rate limited or suspended
                    if resp.status == 401:
                        return ValidationResult(
                            passed=False,
                            message="ANTHROPIC_API_KEY is invalid or expired",
                            severity="error"
                        )
                    elif resp.status == 403:
                        return ValidationResult(
                            passed=False,
                            message="ANTHROPIC_API_KEY access denied (rate limited or suspended)",
                            severity="error"
                        )
                    else:
                        return ValidationResult(
                            passed=True,
                            message="ANTHROPIC_API_KEY validated successfully",
                            severity="info"
                        )
        except asyncio.TimeoutError:
            return ValidationResult(
                passed=False,
                message="Anthropic API validation timeout - check network connectivity",
                severity="warning"
            )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Failed to validate ANTHROPIC_API_KEY: {str(e)}",
                severity="warning"
            )

    async def validate_discord_token(self, token: Optional[str] = None) -> ValidationResult:
        """Validate Discord bot token"""
        discord_token = token or os.getenv('DISCORD_BOT_TOKEN')

        if not discord_token:
            return ValidationResult(
                passed=False,
                message="DISCORD_BOT_TOKEN not set - Discord features disabled",
                severity="warning"
            )

        try:
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bot {discord_token}'}

                async with session.get(
                    'https://discord.com/api/v10/users/@me',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 401:
                        return ValidationResult(
                            passed=False,
                            message="DISCORD_BOT_TOKEN is invalid or expired",
                            severity="error"
                        )
                    elif resp.status == 200:
                        data = await resp.json()
                        bot_name = data.get('username', 'Unknown')
                        return ValidationResult(
                            passed=True,
                            message=f"Discord token validated successfully (Bot: {bot_name})",
                            severity="info"
                        )
                    else:
                        return ValidationResult(
                            passed=False,
                            message=f"Discord token validation failed: HTTP {resp.status}",
                            severity="error"
                        )
        except asyncio.TimeoutError:
            return ValidationResult(
                passed=False,
                message="Discord API validation timeout - check network connectivity",
                severity="warning"
            )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Failed to validate DISCORD_BOT_TOKEN: {str(e)}",
                severity="warning"
            )

    async def validate_webhook(self, webhook_url: str, name: str) -> ValidationResult:
        """Validate a webhook URL by sending a test request"""
        if not webhook_url or webhook_url in ['https://hooks.zapier.com/hooks/catch/xxxxx/xxxxxx']:
            return ValidationResult(
                passed=False,
                message=f"{name} webhook not configured",
                severity="warning"
            )

        try:
            async with aiohttp.ClientSession() as session:
                test_payload = {
                    'type': 'health_check',
                    'message': 'Helix environment validation test',
                    'timestamp': datetime.utcnow().isoformat()
                }

                async with session.post(
                    webhook_url,
                    json=test_payload,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status in [200, 201, 202, 204]:
                        return ValidationResult(
                            passed=True,
                            message=f"{name} webhook validated successfully",
                            severity="info"
                        )
                    else:
                        return ValidationResult(
                            passed=False,
                            message=f"{name} webhook returned HTTP {resp.status}",
                            severity="error"
                        )
        except asyncio.TimeoutError:
            return ValidationResult(
                passed=False,
                message=f"{name} webhook timeout - check URL",
                severity="error"
            )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"{name} webhook validation failed: {str(e)}",
                severity="error"
            )

    def print_report(self, results: List[ValidationResult]):
        """Print a formatted validation report"""
        errors = [r for r in results if not r.passed and r.severity == "error"]
        warnings = [r for r in results if r.severity == "warning"]
        info = [r for r in results if r.passed and r.severity == "info"]

        logger.info("=" * 80)
        logger.info("🔍 HELIX ENVIRONMENT VALIDATION REPORT")
        logger.info("=" * 80)

        if info:
            logger.info("\n✅ PASSED CHECKS:")
            for result in info:
                logger.info(f"   {result}")

        if warnings:
            logger.warning(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for result in warnings:
                logger.warning(f"   {result}")

        if errors:
            logger.error(f"\n❌ ERRORS ({len(errors)}):")
            for result in errors:
                logger.error(f"   {result}")

        logger.info("=" * 80)

        # Summary
        total = len(results)
        passed = len([r for r in results if r.passed])
        logger.info(f"Summary: {passed}/{total} checks passed")

        if errors:
            logger.error("⚠️  CRITICAL: Service may not function properly due to missing/invalid configuration")
            return False
        elif warnings:
            logger.warning("⚠️  WARNING: Some optional features may be disabled")
            return True
        else:
            logger.info("✅ All environment checks passed!")
            return True


async def validate_backend_environment() -> bool:
    """Validate backend service environment"""
    validator = EnvironmentValidator()

    # Required variables
    validator.add_required('DATABASE_URL', 'PostgreSQL connection string')
    validator.add_required('REDIS_URL', 'Redis connection string')

    # Optional but recommended
    validator.add_optional('ANTHROPIC_API_KEY', 'Claude API access')
    validator.add_optional('PERPLEXITY_API_KEY', 'Perplexity multi-LLM and search')
    validator.add_optional('DISCORD_BOT_TOKEN', 'Discord bot features')
    validator.add_optional('ZAPIER_WEBHOOK_URL', 'UCF telemetry webhook')
    validator.add_optional('ZAPIER_MASTER_HOOK_URL', 'Master webhook for integrations')
    validator.add_optional('NOTION_API_KEY', 'Notion integration')

    results = []

    # Check environment variables
    results.extend(validator.check_required_vars())
    results.extend(validator.check_optional_vars())

    # Validate connections
    results.append(await validator.validate_database_connection())
    results.append(await validator.validate_redis_connection())
    results.append(await validator.validate_anthropic_api_key())
    results.append(await validator.validate_perplexity_api_key())

    # Validate webhooks if configured
    zapier_url = os.getenv('ZAPIER_WEBHOOK_URL')
    if zapier_url:
        results.append(await validator.validate_webhook(zapier_url, 'Zapier UCF'))

    master_hook = os.getenv('ZAPIER_MASTER_HOOK_URL')
    if master_hook:
        results.append(await validator.validate_webhook(master_hook, 'Zapier Master'))

    # Print report and return status
    return validator.print_report(results)


async def validate_discord_environment() -> bool:
    """Validate Discord bot service environment"""
    validator = EnvironmentValidator()

    # Required variables
    validator.add_required('DISCORD_BOT_TOKEN', 'Discord bot authentication')
    validator.add_required('DISCORD_GUILD_ID', 'Discord server ID')
    validator.add_required('CLAUDE_API_URL', 'Claude consciousness API endpoint')

    # Optional
    validator.add_optional('API_BASE', 'Backend API endpoint')
    validator.add_optional('DATABASE_URL', 'Database connection')
    validator.add_optional('REDIS_URL', 'Redis cache')

    results = []

    # Check environment variables
    results.extend(validator.check_required_vars())
    results.extend(validator.check_optional_vars())

    # Validate Discord token
    results.append(await validator.validate_discord_token())

    # Validate connections if configured
    if os.getenv('DATABASE_URL'):
        results.append(await validator.validate_database_connection())
    if os.getenv('REDIS_URL'):
        results.append(await validator.validate_redis_connection())

    return validator.print_report(results)


async def validate_claude_api_environment() -> bool:
    """Validate Claude API service environment"""
    validator = EnvironmentValidator()

    # Required variables
    validator.add_required('ANTHROPIC_API_KEY', 'Claude API access')

    # Optional
    validator.add_optional('DATABASE_URL', 'Database connection')
    validator.add_optional('REDIS_URL', 'Redis cache')
    validator.add_optional('CONSCIOUSNESS_ENGINE_WEBHOOK', 'Consciousness telemetry')
    validator.add_optional('COMMUNICATIONS_HUB_WEBHOOK', 'Communications tracking')
    validator.add_optional('NEURAL_NETWORK_WEBHOOK', 'Neural network events')

    results = []

    # Check environment variables
    results.extend(validator.check_required_vars())
    results.extend(validator.check_optional_vars())

    # Validate API key
    results.append(await validator.validate_anthropic_api_key())

    # Validate connections if configured
    if os.getenv('DATABASE_URL'):
        results.append(await validator.validate_database_connection())
    if os.getenv('REDIS_URL'):
        results.append(await validator.validate_redis_connection())

    # Validate webhooks if configured
    for webhook_var, name in [
        ('CONSCIOUSNESS_ENGINE_WEBHOOK', 'Consciousness Engine'),
        ('COMMUNICATIONS_HUB_WEBHOOK', 'Communications Hub'),
        ('NEURAL_NETWORK_WEBHOOK', 'Neural Network')
    ]:
        webhook_url = os.getenv(webhook_var)
        if webhook_url:
            results.append(await validator.validate_webhook(webhook_url, name))

    return validator.print_report(results)


if __name__ == '__main__':
    """Run validation based on service type"""
    import sys  # noqa

    service_type = os.getenv('SERVICE_TYPE', 'backend')

    if service_type == 'backend':
        success = asyncio.run(validate_backend_environment())
    elif service_type == 'discord':
        success = asyncio.run(validate_discord_environment())
    elif service_type == 'claude-api':
        success = asyncio.run(validate_claude_api_environment())
    else:
        logger.error(f"Unknown service type: {service_type}")
        sys.exit(1)

    sys.exit(0 if success else 1)
