"""
Performance monitoring dashboard for Helix Unified system
"""
import time
import psutil
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import logging
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_usage_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_processes: int

@dataclass
class DiscordMetrics:
    """Discord-specific metrics"""
    timestamp: datetime
    connected_guilds: int
    total_channels: int
    voice_connections: int
    messages_processed: int
    commands_executed: int
    response_time_ms: float
    errors_count: int

@dataclass
class AgentMetrics:
    """Agent-specific metrics"""
    timestamp: datetime
    active_agents: int
    total_responses: int
    average_response_time: float
    llm_requests: int
    tts_requests: int
    agent_uptime: Dict[str, float]

class PerformanceMonitor:
    """Main performance monitoring system"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.system_history = deque(maxlen=max_history)
        self.discord_history = deque(maxlen=max_history)
        self.agent_history = deque(maxlen=max_history)
        self.alerts = []
        self.thresholds = {
            'cpu_warning': 80.0,
            'cpu_critical': 95.0,
            'memory_warning': 85.0,
            'memory_critical': 95.0,
            'disk_warning': 90.0,
            'response_time_warning': 2000.0,
            'error_rate_warning': 10
        }
        
        # Counters
        self.message_count = 0
        self.command_count = 0
        self.error_count = 0
        self.llm_request_count = 0
        self.tts_request_count = 0
        
        # Start time for uptime calculation
        self.start_time = datetime.utcnow()
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network
            network = psutil.net_io_counters()
            
            # Processes
            active_processes = len(psutil.pids())
            
            metrics = SystemMetrics(
                timestamp=datetime.utcnow(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / 1024 / 1024,
                disk_usage_percent=disk.percent,
                network_bytes_sent=network.bytes_sent,
                network_bytes_recv=network.bytes_recv,
                active_processes=active_processes
            )
            
            self.system_history.append(metrics)
            self._check_system_alerts(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return None
    
    def collect_discord_metrics(self, discord_client) -> DiscordMetrics:
        """Collect Discord-specific metrics"""
        try:
            if not discord_client:
                return None
                
            metrics = DiscordMetrics(
                timestamp=datetime.utcnow(),
                connected_guilds=len(discord_client.guilds) if discord_client.guilds else 0,
                total_channels=sum(len(guild.channels) for guild in discord_client.guilds) if discord_client.guilds else 0,
                voice_connections=len(getattr(discord_client, 'voice_clients', [])),
                messages_processed=self.message_count,
                commands_executed=self.command_count,
                response_time_ms=self._calculate_average_response_time(),
                errors_count=self.error_count
            )
            
            self.discord_history.append(metrics)
            self._check_discord_alerts(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect Discord metrics: {e}")
            return None
    
    def collect_agent_metrics(self, agents: Dict[str, Any]) -> AgentMetrics:
        """Collect agent-specific metrics"""
        try:
            active_agents = sum(1 for agent in agents.values() if getattr(agent, 'is_active', False))
            total_responses = sum(getattr(agent, 'response_count', 0) for agent in agents.values())
            
            # Calculate average response time
            response_times = [getattr(agent, 'average_response_time', 0) for agent in agents.values()]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Agent uptime
            agent_uptime = {
                agent_id: getattr(agent, 'uptime_seconds', 0)
                for agent_id, agent in agents.items()
            }
            
            metrics = AgentMetrics(
                timestamp=datetime.utcnow(),
                active_agents=active_agents,
                total_responses=total_responses,
                average_response_time=avg_response_time,
                llm_requests=self.llm_request_count,
                tts_requests=self.tts_request_count,
                agent_uptime=agent_uptime
            )
            
            self.agent_history.append(metrics)
            self._check_agent_alerts(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect agent metrics: {e}")
            return None
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average Discord response time"""
        if not self.discord_history:
            return 0.0
        recent_metrics = list(self.discord_history)[-10:]  # Last 10 measurements
        response_times = [m.response_time_ms for m in recent_metrics if m.response_time_ms > 0]
        return sum(response_times) / len(response_times) if response_times else 0.0
    
    def _check_system_alerts(self, metrics: SystemMetrics):
        """Check for system performance alerts"""
        if metrics.cpu_percent >= self.thresholds['cpu_critical']:
            self._create_alert('critical', f'CPU usage critical: {metrics.cpu_percent:.1f}%')
        elif metrics.cpu_percent >= self.thresholds['cpu_warning']:
            self._create_alert('warning', f'CPU usage high: {metrics.cpu_percent:.1f}%')
        
        if metrics.memory_percent >= self.thresholds['memory_critical']:
            self._create_alert('critical', f'Memory usage critical: {metrics.memory_percent:.1f}%')
        elif metrics.memory_percent >= self.thresholds['memory_warning']:
            self._create_alert('warning', f'Memory usage high: {metrics.memory_percent:.1f}%')
        
        if metrics.disk_usage_percent >= self.thresholds['disk_warning']:
            self._create_alert('warning', f'Disk usage high: {metrics.disk_usage_percent:.1f}%')
    
    def _check_discord_alerts(self, metrics: DiscordMetrics):
        """Check for Discord performance alerts"""
        if metrics.response_time_ms >= self.thresholds['response_time_warning']:
            self._create_alert('warning', f'Discord response time high: {metrics.response_time_ms:.1f}ms')
        
        # Calculate error rate (errors per 100 messages)
        if metrics.messages_processed > 0:
            error_rate = (metrics.errors_count / metrics.messages_processed) * 100
            if error_rate >= self.thresholds['error_rate_warning']:
                self._create_alert('warning', f'High error rate: {error_rate:.1f}%')
    
    def _check_agent_alerts(self, metrics: AgentMetrics):
        """Check for agent performance alerts"""
        if metrics.average_response_time >= self.thresholds['response_time_warning']:
            self._create_alert('warning', f'Agent response time high: {metrics.average_response_time:.1f}ms')
    
    def _create_alert(self, level: str, message: str):
        """Create a performance alert"""
        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message
        }
        self.alerts.append(alert)
        
        # Keep only last 50 alerts
        self.alerts = self.alerts[-50:]
        
        logger.warning(f"Performance Alert [{level.upper()}]: {message}")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        current_time = datetime.utcnow()
        uptime = current_time - self.start_time
        
        # Latest metrics
        latest_system = self.system_history[-1] if self.system_history else None
        latest_discord = self.discord_history[-1] if self.discord_history else None
        latest_agent = self.agent_history[-1] if self.agent_history else None
        
        return {
            'system_status': {
                'uptime_seconds': uptime.total_seconds(),
                'uptime_human': str(uptime).split('.')[0],
                'current_metrics': asdict(latest_system) if latest_system else None,
                'cpu_trend': self._get_trend([m.cpu_percent for m in list(self.system_history)[-10:]]),
                'memory_trend': self._get_trend([m.memory_percent for m in list(self.system_history)[-10:]]),
            },
            'discord_status': {
                'current_metrics': asdict(latest_discord) if latest_discord else None,
                'message_rate': self._calculate_rate('messages'),
                'command_rate': self._calculate_rate('commands'),
                'error_rate': self._calculate_rate('errors'),
            },
            'agent_status': {
                'current_metrics': asdict(latest_agent) if latest_agent else None,
                'llm_rate': self._calculate_rate('llm_requests'),
                'tts_rate': self._calculate_rate('tts_requests'),
            },
            'alerts': {
                'total': len(self.alerts),
                'recent': self.alerts[-10:],
                'critical_count': len([a for a in self.alerts if a['level'] == 'critical']),
                'warning_count': len([a for a in self.alerts if a['level'] == 'warning']),
            },
            'performance_summary': {
                'overall_health': self._calculate_health_score(),
                'bottlenecks': self._identify_bottlenecks(),
                'recommendations': self._generate_recommendations()
            }
        }
    
    def _get_trend(self, values: List[float]) -> str:
        """Calculate trend from values"""
        if len(values) < 2:
            return 'stable'
        
        recent_avg = sum(values[-3:]) / min(3, len(values))
        older_avg = sum(values[-6:-3]) / min(3, len(values) - 3) if len(values) >= 6 else recent_avg
        
        if recent_avg > older_avg * 1.1:
            return 'increasing'
        elif recent_avg < older_avg * 0.9:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_rate(self, metric_type: str) -> float:
        """Calculate rate per minute for given metric"""
        if not self.discord_history or len(self.discord_history) < 2:
            return 0.0
        
        latest = self.discord_history[-1]
        oldest = self.discord_history[0]
        
        time_diff = (latest.timestamp - oldest.timestamp).total_seconds()
        if time_diff <= 0:
            return 0.0
        
        if metric_type == 'messages':
            diff = latest.messages_processed - oldest.messages_processed
        elif metric_type == 'commands':
            diff = latest.commands_executed - oldest.commands_executed
        elif metric_type == 'errors':
            diff = latest.errors_count - oldest.errors_count
        else:
            return 0.0
        
        return (diff / time_diff) * 60  # Per minute
    
    def _calculate_health_score(self) -> float:
        """Calculate overall system health score (0-100)"""
        if not self.system_history:
            return 100.0
        
        latest = self.system_history[-1]
        score = 100.0
        
        # CPU impact
        if latest.cpu_percent > 80:
            score -= (latest.cpu_percent - 80) * 2
        
        # Memory impact
        if latest.memory_percent > 75:
            score -= (latest.memory_percent - 75) * 1.5
        
        # Disk impact
        if latest.disk_usage_percent > 85:
            score -= (latest.disk_usage_percent - 85) * 1
        
        # Error impact
        if self.discord_history:
            latest_discord = self.discord_history[-1]
            if latest_discord.messages_processed > 0:
                error_rate = (latest_discord.errors_count / latest_discord.messages_processed) * 100
                score -= min(error_rate * 5, 20)
        
        return max(0.0, min(100.0, score))
    
    def _identify_bottlenecks(self) -> List[str]:
        """Identify current performance bottlenecks"""
        bottlenecks = []
        
        if self.system_history:
            latest = self.system_history[-1]
            if latest.cpu_percent > 80:
                bottlenecks.append('High CPU usage')
            if latest.memory_percent > 85:
                bottlenecks.append('High memory usage')
            if latest.disk_usage_percent > 90:
                bottlenecks.append('Low disk space')
        
        if self.discord_history:
            latest = self.discord_history[-1]
            if latest.response_time_ms > 1500:
                bottlenecks.append('Slow Discord response times')
        
        if len(self.alerts) > 10:
            bottlenecks.append('High alert frequency')
        
        return bottlenecks
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if self.system_history:
            latest = self.system_history[-1]
            if latest.cpu_percent > 75:
                recommendations.append('Consider scaling CPU resources')
            if latest.memory_percent > 80:
                recommendations.append('Monitor memory usage and consider optimization')
        
        if self.error_count > 50:
            recommendations.append('Review error logs for common issues')
        
        if not self.discord_history or len(self.discord_history) == 0:
            recommendations.append('Discord metrics not available - check bot connection')
        
        return recommendations
    
    def increment_counters(self, **kwargs):
        """Increment various performance counters"""
        if 'messages' in kwargs:
            self.message_count += kwargs['messages']
        if 'commands' in kwargs:
            self.command_count += kwargs['commands']
        if 'errors' in kwargs:
            self.error_count += kwargs['errors']
        if 'llm_requests' in kwargs:
            self.llm_request_count += kwargs['llm_requests']
        if 'tts_requests' in kwargs:
            self.tts_request_count += kwargs['tts_requests']
    
    def reset_counters(self):
        """Reset all performance counters"""
        self.message_count = 0
        self.command_count = 0
        self.error_count = 0
        self.llm_request_count = 0
        self.tts_request_count = 0

# Global monitor instance
performance_monitor = PerformanceMonitor()