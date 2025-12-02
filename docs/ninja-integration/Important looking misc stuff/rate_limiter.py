"""
Rate limiting system for API endpoints and Discord commands
"""
import time
import asyncio
import hashlib
import json
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from collections import defaultdict, deque
import logging
from fastapi import HTTPException, Request
from functools import wraps

logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    """Rate limit configuration"""
    max_requests: int
    window_seconds: int
    scope: str = "global"  # global, user, ip, guild, channel
    penalty_seconds: int = 0  # Ban duration after limit exceeded

class RateLimiter:
    """Advanced rate limiting system with multiple strategies"""
    
    def __init__(self):
        self.trackers = defaultdict(lambda: defaultdict(deque))
        self.blocked_until = defaultdict(float)
        self.configs = {}
        self.default_config = RateLimitConfig(
            max_requests=100,
            window_seconds=60,
            scope="global"
        )
        
        # Predefined configurations
        self.configs = {
            'api_endpoints': RateLimitConfig(
                max_requests=1000,
                window_seconds=60,
                scope="ip"
            ),
            'discord_commands': RateLimitConfig(
                max_requests=10,
                window_seconds=60,
                scope="user"
            ),
            'message_processing': RateLimitConfig(
                max_requests=5,
                window_seconds=10,
                scope="channel"
            ),
            'voice_operations': RateLimitConfig(
                max_requests=3,
                window_seconds=30,
                scope="guild"
            ),
            'llm_requests': RateLimitConfig(
                max_requests=20,
                window_seconds=60,
                scope="user",
                penalty_seconds=300  # 5 minute ban
            ),
            'tts_requests': RateLimitConfig(
                max_requests=10,
                window_seconds=60,
                scope="user"
            ),
            'admin_commands': RateLimitConfig(
                max_requests=50,
                window_seconds=60,
                scope="user"
            )
        }
    
    def _get_key(self, scope: str, identifier: str, endpoint: str) -> str:
        """Generate rate limit key"""
        key_data = f"{scope}:{identifier}:{endpoint}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_identifier(self, request: Request = None, **kwargs) -> str:
        """Get identifier based on scope"""
        scope = kwargs.get('scope', 'global')
        
        if scope == 'ip' and request:
            return request.client.host if request.client else 'unknown'
        elif scope == 'user':
            return str(kwargs.get('user_id', 'unknown'))
        elif scope == 'guild':
            return str(kwargs.get('guild_id', 'unknown'))
        elif scope == 'channel':
            return str(kwargs.get('channel_id', 'unknown'))
        else:
            return 'global'
    
    def is_allowed(
        self, 
        endpoint: str, 
        request: Request = None,
        config: Optional[RateLimitConfig] = None,
        **kwargs
    ) -> tuple[bool, Dict[str, Any]]:
        """Check if request is allowed under rate limit"""
        
        if config is None:
            config = self.configs.get(endpoint, self.default_config)
        
        current_time = time.time()
        identifier = self._get_identifier(request, scope=config.scope, **kwargs)
        key = self._get_key(config.scope, identifier, endpoint)
        
        # Check if currently blocked (penalty)
        if key in self.blocked_until:
            if current_time < self.blocked_until[key]:
                remaining_penalty = int(self.blocked_until[key] - current_time)
                return False, {
                    'allowed': False,
                    'message': f'Rate limit exceeded. Try again in {remaining_penalty} seconds.',
                    'retry_after': remaining_penalty,
                    'limit': config.max_requests,
                    'remaining': 0,
                    'reset_time': int(self.blocked_until[key])
                }
            else:
                # Penalty expired, remove block
                del self.blocked_until[key]
        
        # Clean old requests outside the window
        request_times = self.trackers[endpoint][key]
        while request_times and request_times[0] <= current_time - config.window_seconds:
            request_times.popleft()
        
        # Check if under limit
        if len(request_times) < config.max_requests:
            request_times.append(current_time)
            remaining = config.max_requests - len(request_times)
            reset_time = int(current_time + config.window_seconds)
            
            return True, {
                'allowed': True,
                'remaining': remaining,
                'limit': config.max_requests,
                'reset_time': reset_time
            }
        else:
            # Limit exceeded - apply penalty if configured
            if config.penalty_seconds > 0:
                self.blocked_until[key] = current_time + config.penalty_seconds
                logger.warning(f"Applied rate limit penalty to {identifier} for {config.penalty_seconds} seconds")
            
            # Calculate retry after
            oldest_request = request_times[0] if request_times else current_time
            retry_after = int(oldest_request + config.window_seconds - current_time)
            
            return False, {
                'allowed': False,
                'message': f'Rate limit exceeded. Try again in {retry_after} seconds.',
                'retry_after': retry_after,
                'limit': config.max_requests,
                'remaining': 0,
                'reset_time': int(oldest_request + config.window_seconds)
            }
    
    def get_status(self, endpoint: str, identifier: str) -> Dict[str, Any]:
        """Get current rate limit status"""
        config = self.configs.get(endpoint, self.default_config)
        key = self._get_key(config.scope, identifier, endpoint)
        current_time = time.time()
        
        request_times = self.trackers[endpoint][key]
        
        # Clean old requests
        while request_times and request_times[0] <= current_time - config.window_seconds:
            request_times.popleft()
        
        remaining = max(0, config.max_requests - len(request_times))
        reset_time = int(current_time + config.window_seconds)
        
        if key in self.blocked_until and current_time < self.blocked_until[key]:
            remaining_penalty = int(self.blocked_until[key] - current_time)
            return {
                'blocked': True,
                'retry_after': remaining_penalty,
                'remaining': 0,
                'limit': config.max_requests,
                'reset_time': int(self.blocked_until[key])
            }
        
        return {
            'blocked': False,
            'remaining': remaining,
            'limit': config.max_requests,
            'reset_time': reset_time,
            'used': len(request_times)
        }
    
    def reset(self, endpoint: str, identifier: str = None):
        """Reset rate limit for endpoint or specific identifier"""
        if identifier:
            # Reset specific identifier
            for scope in self.trackers[endpoint]:
                if identifier in scope:
                    del self.trackers[endpoint][scope]
        else:
            # Reset all for endpoint
            self.trackers[endpoint].clear()
        
        logger.info(f"Rate limit reset for endpoint: {endpoint}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics"""
        total_requests = 0
        blocked_count = len(self.blocked_until)
        
        for endpoint, trackers in self.trackers.items():
            for identifier, requests in trackers.items():
                total_requests += len(requests)
        
        return {
            'total_active_requests': total_requests,
            'blocked_identifiers': blocked_count,
            'active_endpoints': len(self.trackers),
            'configs_count': len(self.configs)
        }

# Global rate limiter instance
rate_limiter = RateLimiter()

# Decorators for easy usage
def rate_limit(endpoint: str, config: Optional[RateLimitConfig] = None):
    """Rate limiting decorator for functions"""
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            allowed, info = rate_limiter.is_allowed(endpoint, config=config, **kwargs)
            
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail=info['message'],
                    headers={'Retry-After': str(info['retry_after'])}
                )
            
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, we can't easily handle async rate limiting
            # This is a simplified version
            allowed, info = rate_limiter.is_allowed(endpoint, config=config, **kwargs)
            
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail=info['message'],
                    headers={'Retry-After': str(info['retry_after'])}
                )
            
            return func(*args, **kwargs)
        
        import asyncio
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def discord_rate_limit(command_type: str = "general"):
    """Rate limiting decorator for Discord commands"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, message, *args, **kwargs):
            # Extract Discord context
            context = {
                'user_id': message.author.id,
                'guild_id': message.guild.id if message.guild else 'dm',
                'channel_id': message.channel.id
            }
            
            # Map command types to rate limit configs
            endpoint_map = {
                'general': 'discord_commands',
                'admin': 'admin_commands',
                'voice': 'voice_operations',
                'message': 'message_processing',
                'llm': 'llm_requests',
                'tts': 'tts_requests'
            }
            
            endpoint = endpoint_map.get(command_type, 'discord_commands')
            allowed, info = rate_limiter.is_allowed(endpoint, **context)
            
            if not allowed:
                await message.channel.send(f"⚠️ {info['message']}")
                return
            
            return await func(self, message, *args, **kwargs)
        
        return wrapper
    return decorator

# FastAPI middleware for rate limiting
async def rate_limit_middleware(request: Request, call_next):
    """FastAPI middleware for rate limiting"""
    # Get endpoint path
    path = request.url.path
    
    # Skip rate limiting for health checks and static files
    if path in ['/health', '/metrics', '/docs', '/openapi.json']:
        return await call_next(request)
    
    # Apply rate limiting
    allowed, info = rate_limiter.is_allowed('api_endpoints', request=request)
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                'error': info['message'],
                'retry_after': info['retry_after']
            },
            headers={'Retry-After': str(info['retry_after'])}
        )
    
    response = await call_next(request)
    
    # Add rate limit headers to response
    response.headers['X-RateLimit-Limit'] = str(info['limit'])
    response.headers['X-RateLimit-Remaining'] = str(info['remaining'])
    response.headers['X-RateLimit-Reset'] = str(info['reset_time'])
    
    return response

from fastapi.responses import JSONResponse