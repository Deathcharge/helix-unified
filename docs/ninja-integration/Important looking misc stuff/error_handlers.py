import asyncio
import functools
import logging
import traceback
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from discord import DiscordException
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

class HelixError(Exception):
    """Base exception class for Helix Unified system"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.utcnow()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'error': str(self),
            'error_code': self.error_code,
            'context': self.context,
            'timestamp': self.timestamp.isoformat()
        }

class DiscordError(HelixError):
    """Discord-specific errors"""
    pass

class AgentError(HelixError):
    """Agent-specific errors"""
    pass

class VoiceError(HelixError):
    """Voice system errors"""
    pass

class APIError(HelixError):
    """API-related errors"""
    pass

def error_boundary(
    error_type: Optional[type] = HelixError,
    fallback_value: Any = None,
    log_error: bool = True,
    reraise: bool = False
):
    """Decorator for handling errors with logging and fallback"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(
                        f"Error in {func.__name__}: {str(e)}",
                        extra={
                            'function': func.__name__,
                            'args': str(args)[:200],
                            'kwargs': str(kwargs)[:200],
                            'traceback': traceback.format_exc()
                        },
                        exc_info=True
                    )
                
                if isinstance(e, error_type) or error_type is None:
                    if reraise:
                        raise
                    return fallback_value
                else:
                    raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(
                        f"Error in {func.__name__}: {str(e)}",
                        extra={
                            'function': func.__name__,
                            'args': str(args)[:200],
                            'kwargs': str(kwargs)[:200],
                            'traceback': traceback.format_exc()
                        },
                        exc_info=True
                    )
                
                if isinstance(e, error_type) or error_type is None:
                    if reraise:
                        raise
                    return fallback_value
                else:
                    raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

class ErrorTracker:
    """Track and analyze errors across the system"""
    
    def __init__(self):
        self.error_counts = {}
        self.error_details = {}
        self.recent_errors = []
        self.max_recent = 100
    
    def track_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Track an error occurrence"""
        error_type = type(error).__name__
        
        # Increment count
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Store details
        if error_type not in self.error_details:
            self.error_details[error_type] = {
                'first_seen': datetime.utcnow(),
                'last_seen': datetime.utcnow(),
                'total_count': 0,
                'contexts': []
            }
        
        self.error_details[error_type]['last_seen'] = datetime.utcnow()
        self.error_details[error_type]['total_count'] += 1
        
        if context:
            self.error_details[error_type]['contexts'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'context': context
            })
            # Keep only last 10 contexts
            self.error_details[error_type]['contexts'] = self.error_details[error_type]['contexts'][-10:]
        
        # Add to recent errors
        self.recent_errors.append({
            'timestamp': datetime.utcnow().isoformat(),
            'type': error_type,
            'message': str(error),
            'context': context
        })
        
        # Keep only recent errors
        self.recent_errors = self.recent_errors[-self.max_recent:]
        
        logger.warning(f"Tracked error: {error_type} - {str(error)}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of tracked errors"""
        return {
            'total_error_types': len(self.error_counts),
            'error_counts': self.error_counts,
            'recent_errors_count': len(self.recent_errors),
            'most_common_error': max(self.error_counts.items(), key=lambda x: x[1])[0] if self.error_counts else None
        }
    
    def clear_history(self):
        """Clear error history"""
        self.error_counts.clear()
        self.error_details.clear()
        self.recent_errors.clear()

# Global error tracker
error_tracker = ErrorTracker()

# FastAPI error handler
async def api_exception_handler(request: Request, exc: HTTPException):
    """Handle API exceptions with logging"""
    error_tracker.track_error(exc, {'path': request.url.path, 'method': request.method})
    
    logger.error(
        f"API Error: {exc.status_code} - {exc.detail}",
        extra={
            'status_code': exc.status_code,
            'path': request.url.path,
            'method': request.method,
            'client_ip': request.client.host if request.client else None
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.detail,
            'status_code': exc.status_code,
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.url.path
        }
    )

async def general_api_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions in API"""
    error_tracker.track_error(exc, {'path': request.url.path, 'method': request.method})
    
    logger.error(
        f"Unhandled API Error: {str(exc)}",
        extra={
            'path': request.url.path,
            'method': request.method,
            'client_ip': request.client.host if request.client else None,
            'traceback': traceback.format_exc()
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            'error': 'Internal server error',
            'status_code': 500,
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.url.path
        }
    )

def setup_fastapi_error_handlers(app):
    """Setup error handlers for FastAPI app"""
    app.add_exception_handler(HTTPException, api_exception_handler)
    app.add_exception_handler(Exception, general_api_exception_handler)