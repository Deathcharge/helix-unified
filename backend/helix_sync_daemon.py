"""
Helix Ecosystem Sync Daemon
============================

Central orchestration service for synchronizing the Helix ecosystem across
GitHub, Notion, Discord, and web portals.

Author: Manus AI
Version: 1.0
Date: 2025-11-01
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Setup logging
# Create logs directory if it doesn't exist
import os
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/helix_sync.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('HelixSync')


class SyncMetadata:
    """Tracks sync operation metadata"""
    
    def __init__(self):
        self.last_sync: Optional[datetime] = None
        self.next_sync: Optional[datetime] = None
        self.sync_count: int = 0
        self.success_count: int = 0
        self.failure_count: int = 0
        self.last_error: Optional[str] = None
        self.sync_history: List[Dict] = []
    
    def record_sync(self, success: bool, duration: float, error: Optional[str] = None):
        """Record a sync operation"""
        self.sync_count += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
            self.last_error = error
        
        self.last_sync = datetime.utcnow()
        self.sync_history.append({
            'timestamp': self.last_sync.isoformat(),
            'success': success,
            'duration': duration,
            'error': error
        })
        
        # Keep only last 100 records
        if len(self.sync_history) > 100:
            self.sync_history = self.sync_history[-100:]
    
    def get_success_rate(self) -> float:
        """Calculate success rate"""
        if self.sync_count == 0:
            return 0.0
        return self.success_count / self.sync_count
    
    def get_avg_duration(self) -> float:
        """Calculate average sync duration"""
        if not self.sync_history:
            return 0.0
        durations = [s['duration'] for s in self.sync_history if s['success']]
        return sum(durations) / len(durations) if durations else 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'next_sync': self.next_sync.isoformat() if self.next_sync else None,
            'sync_count': self.sync_count,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'success_rate': self.get_success_rate(),
            'avg_duration': self.get_avg_duration(),
            'last_error': self.last_error,
            'recent_history': self.sync_history[-10:]  # Last 10 syncs
        }


class HelixSyncDaemon:
    """Main sync daemon orchestrator"""
    
    def __init__(self, config_path: str = 'config/sync_config.json'):
        self.config_path = config_path
        self.config: Dict = {}
        self.metadata = SyncMetadata()
        self.running = False
        self.sources_status: Dict[str, str] = {}
        self.targets_status: Dict[str, str] = {}
        
        # Load configuration
        self.load_config()
        
        # Create necessary directories
        self.ensure_directories()
    
    def load_config(self):
        """Load sync configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Loaded config from {self.config_path}")
            else:
                # Use default config
                self.config = self.get_default_config()
                logger.warning(f"Config file not found, using defaults")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'version': '1.0',
            'sync_schedule': {
                'interval_seconds': int(os.getenv('HELIX_SYNC_INTERVAL', '3600')),
                'on_ritual': True,
                'on_deploy': True
            },
            'sources': {
                'github': {
                    'enabled': True,
                    'repos': ['helix-unified', 'Helix', 'Helix-Collective-Web']
                },
                'ucf_state': {
                    'enabled': True
                },
                'agent_metrics': {
                    'enabled': True
                }
            },
            'exporters': {
                'notion': {'enabled': True},
                'markdown': {'enabled': True},
                'json': {'enabled': True},
                'html': {'enabled': False}
            },
            'publishers': {
                'discord': {'enabled': True},
                'notion': {'enabled': True},
                'portal': {'enabled': True}
            }
        }
    
    def ensure_directories(self):
        """Create necessary directories"""
        dirs = ['logs', 'exports', 'exports/notion', 'exports/markdown', 
                'exports/json', 'exports/html']
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
    
    async def collect_from_sources(self) -> Dict[str, Any]:
        """Collect data from all enabled sources"""
        logger.info("Collecting from sources...")
        collected_data = {}
        
        try:
            # GitHub
            if self.config['sources']['github']['enabled']:
                logger.info("Collecting from GitHub...")
                collected_data['github'] = await self.collect_github()
                self.sources_status['github'] = 'ok'
            
            # UCF State
            if self.config['sources']['ucf_state']['enabled']:
                logger.info("Collecting UCF state...")
                collected_data['ucf_state'] = await self.collect_ucf_state()
                self.sources_status['ucf_state'] = 'ok'
            
            # Agent Metrics
            if self.config['sources']['agent_metrics']['enabled']:
                logger.info("Collecting agent metrics...")
                collected_data['agent_metrics'] = await self.collect_agent_metrics()
                self.sources_status['agent_metrics'] = 'ok'
            
            logger.info(f"Collected data from {len(collected_data)} sources")
            return collected_data
            
        except Exception as e:
            logger.error(f"Error collecting from sources: {e}")
            raise
    
    async def collect_github(self) -> Dict:
        """Collect data from GitHub repositories"""
        # Placeholder - will be implemented in next phase
        return {
            'repos': self.config['sources']['github']['repos'],
            'last_commits': {},
            'open_issues': 0,
            'open_prs': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def collect_ucf_state(self) -> Dict:
        """Collect current UCF state"""
        # Placeholder - will read from z88_ritual_engine
        return {
            'harmony': 0.8547,
            'resilience': 1.1191,
            'prana': 0.5175,
            'drishti': 0.5023,
            'klesha': 0.0100,
            'zoom': 1.0228,
            'collective_emotion': 'Calm',
            'ethical_alignment': 0.85,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def collect_agent_metrics(self) -> Dict:
        """Collect agent performance metrics"""
        # Placeholder - will read from agent_profiles
        return {
            'total_agents': 11,
            'active_agents': 11,
            'total_tasks': 0,
            'success_rate': 0.0,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def export_data(self, data: Dict) -> Dict[str, str]:
        """Export collected data to all enabled formats"""
        logger.info("Exporting data...")
        export_paths = {}
        
        try:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            
            # Notion JSON
            if self.config['exporters']['notion']['enabled']:
                path = f"exports/notion/helix_sync_{timestamp}.json"
                await self.export_notion(data, path)
                export_paths['notion'] = path
                logger.info(f"Exported to Notion format: {path}")
            
            # Markdown
            if self.config['exporters']['markdown']['enabled']:
                path = f"exports/markdown/helix_sync_{timestamp}.md"
                await self.export_markdown(data, path)
                export_paths['markdown'] = path
                logger.info(f"Exported to Markdown: {path}")
            
            # JSON
            if self.config['exporters']['json']['enabled']:
                path = f"exports/json/helix_sync_{timestamp}.json"
                await self.export_json(data, path)
                export_paths['json'] = path
                logger.info(f"Exported to JSON: {path}")
            
            # HTML
            if self.config['exporters']['html']['enabled']:
                path = f"exports/html/helix_sync_{timestamp}.html"
                await self.export_html(data, path)
                export_paths['html'] = path
                logger.info(f"Exported to HTML: {path}")
            
            return export_paths
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise
    
    async def export_notion(self, data: Dict, path: str):
        """Export to Notion-compatible JSON"""
        # Placeholder - will be implemented in next phase
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def export_markdown(self, data: Dict, path: str):
        """Export to Markdown"""
        # Placeholder - will be implemented in next phase
        with open(path, 'w') as f:
            f.write(f"# Helix Ecosystem Sync\n\n")
            f.write(f"**Generated:** {datetime.utcnow().isoformat()}\n\n")
            f.write(f"```json\n{json.dumps(data, indent=2)}\n```\n")
    
    async def export_json(self, data: Dict, path: str):
        """Export to JSON"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def export_html(self, data: Dict, path: str):
        """Export to HTML"""
        # Placeholder - will be implemented in next phase
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Helix Ecosystem Sync</title>
            <style>
                body {{ font-family: monospace; padding: 20px; }}
                pre {{ background: #f4f4f4; padding: 10px; }}
            </style>
        </head>
        <body>
            <h1>Helix Ecosystem Sync</h1>
            <p>Generated: {datetime.utcnow().isoformat()}</p>
            <pre>{json.dumps(data, indent=2)}</pre>
        </body>
        </html>
        """
        with open(path, 'w') as f:
            f.write(html)
    
    async def publish_to_targets(self, data: Dict, export_paths: Dict):
        """Publish to all enabled targets"""
        logger.info("Publishing to targets...")
        
        try:
            # Discord
            if self.config['publishers']['discord']['enabled']:
                await self.publish_discord(data, export_paths)
                self.targets_status['discord'] = 'ok'
                logger.info("Published to Discord")
            
            # Notion
            if self.config['publishers']['notion']['enabled']:
                await self.publish_notion(data, export_paths)
                self.targets_status['notion'] = 'ok'
                logger.info("Published to Notion")
            
            # Portal
            if self.config['publishers']['portal']['enabled']:
                await self.publish_portal(data, export_paths)
                self.targets_status['portal'] = 'ok'
                logger.info("Published to Portal")
            
        except Exception as e:
            logger.error(f"Error publishing to targets: {e}")
            raise
    
    async def publish_discord(self, data: Dict, export_paths: Dict):
        """Publish summary to Discord"""
        # Placeholder - will use Discord webhook
        logger.info("Discord publish (placeholder)")
    
    async def publish_notion(self, data: Dict, export_paths: Dict):
        """Publish to Notion"""
        # Placeholder - will use Notion API
        logger.info("Notion publish (placeholder)")
    
    async def publish_portal(self, data: Dict, export_paths: Dict):
        """Publish to web portal"""
        # Placeholder - will update portal JSON feeds
        logger.info("Portal publish (placeholder)")
    
    async def run_sync_cycle(self) -> bool:
        """Run a complete sync cycle"""
        start_time = datetime.utcnow()
        logger.info("=" * 60)
        logger.info("Starting sync cycle...")
        
        try:
            # 1. Collect from sources
            collected_data = await self.collect_from_sources()
            
            # 2. Export to formats
            export_paths = await self.export_data(collected_data)
            
            # 3. Publish to targets
            await self.publish_to_targets(collected_data, export_paths)
            
            # 4. Record success
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.metadata.record_sync(True, duration)
            
            logger.info(f"Sync cycle completed successfully in {duration:.2f}s")
            logger.info("=" * 60)
            return True
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.metadata.record_sync(False, duration, str(e))
            logger.error(f"Sync cycle failed after {duration:.2f}s: {e}")
            logger.info("=" * 60)
            return False
    
    async def run(self):
        """Main daemon loop"""
        self.running = True
        interval = self.config['sync_schedule']['interval_seconds']
        
        logger.info("🌀 Helix Sync Daemon starting...")
        logger.info(f"Sync interval: {interval}s ({interval/3600:.1f}h)")
        
        # Run initial sync
        await self.run_sync_cycle()
        
        # Schedule next sync
        self.metadata.next_sync = datetime.utcnow() + timedelta(seconds=interval)
        
        # Main loop
        while self.running:
            try:
                # Wait until next sync time
                now = datetime.utcnow()
                if self.metadata.next_sync and now >= self.metadata.next_sync:
                    await self.run_sync_cycle()
                    self.metadata.next_sync = datetime.utcnow() + timedelta(seconds=interval)
                
                # Sleep for a short interval
                await asyncio.sleep(10)
                
            except KeyboardInterrupt:
                logger.info("Received shutdown signal")
                self.running = False
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    def get_status(self) -> Dict:
        """Get current daemon status"""
        return {
            'running': self.running,
            'sources': self.sources_status,
            'targets': self.targets_status,
            'metadata': self.metadata.to_dict()
        }
    
    async def trigger_manual_sync(self):
        """Trigger a manual sync"""
        logger.info("Manual sync triggered")
        return await self.run_sync_cycle()


async def main():
    """Main entry point"""
    config_path = os.getenv('HELIX_SYNC_CONFIG', 'config/sync_config.json')
    daemon = HelixSyncDaemon(config_path)
    
    try:
        await daemon.run()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())

