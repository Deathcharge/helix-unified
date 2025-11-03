"""
Notion JSON Exporter
====================

Exports Helix ecosystem data to Notion API-compatible JSON format.

Author: Manus AI
Version: 1.0
"""

from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger('HelixSync.NotionExporter')


class NotionExporter:
    """Exports data to Notion-compatible JSON"""
    
    def __init__(self):
        self.database_schemas = self.get_database_schemas()
    
    def get_database_schemas(self) -> Dict:
        """Define Notion database schemas"""
        return {
            'repos': {
                'name': 'Helix Repositories',
                'properties': {
                    'Name': {'type': 'title'},
                    'Path': {'type': 'rich_text'},
                    'Remote URL': {'type': 'url'},
                    'Total Commits': {'type': 'number'},
                    'Commits Today': {'type': 'number'},
                    'Latest Commit': {'type': 'rich_text'},
                    'Last Updated': {'type': 'date'}
                }
            },
            'ucf_metrics': {
                'name': 'UCF Metrics',
                'properties': {
                    'Timestamp': {'type': 'title'},
                    'Harmony': {'type': 'number'},
                    'Resilience': {'type': 'number'},
                    'Prana': {'type': 'number'},
                    'Drishti': {'type': 'number'},
                    'Klesha': {'type': 'number'},
                    'Zoom': {'type': 'number'},
                    'Collective Emotion': {'type': 'select'},
                    'Ethical Alignment': {'type': 'number'}
                }
            },
            'agents': {
                'name': 'Helix Agents',
                'properties': {
                    'Name': {'type': 'title'},
                    'Role': {'type': 'rich_text'},
                    'Status': {'type': 'select'},
                    'Tasks Completed': {'type': 'number'},
                    'Success Rate': {'type': 'number'},
                    'Last Active': {'type': 'date'}
                }
            }
        }
    
    async def export(self, data: Dict, output_path: str):
        """Export data to Notion JSON file"""
        logger.info(f"Exporting to Notion JSON: {output_path}")
        
        notion_data = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat(),
            'databases': {}
        }
        
        # Export GitHub repos
        if 'github' in data:
            notion_data['databases']['repos'] = self.export_repos(data['github'])
        
        # Export UCF metrics
        if 'ucf_state' in data:
            notion_data['databases']['ucf_metrics'] = self.export_ucf_metrics(data['ucf_state'])
        
        # Export agent metrics
        if 'agent_metrics' in data:
            notion_data['databases']['agents'] = self.export_agents(data['agent_metrics'])
        
        # Write to file
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(notion_data, f, indent=2)
        
        logger.info(f"Notion JSON export complete")
    
    def export_repos(self, github_data: Dict) -> Dict:
        """Export repository data in Notion format"""
        repos_db = {
            'schema': self.database_schemas['repos'],
            'entries': []
        }
        
        for repo_name, repo_data in github_data.get('repos', {}).items():
            if 'error' in repo_data:
                continue
            
            latest_commit = repo_data.get('latest_commit', {})
            
            entry = {
                'properties': {
                    'Name': {
                        'title': [{'text': {'content': repo_name}}]
                    },
                    'Path': {
                        'rich_text': [{'text': {'content': repo_data.get('path', '')}}]
                    },
                    'Remote URL': {
                        'url': repo_data.get('remote_url', '')
                    },
                    'Total Commits': {
                        'number': repo_data.get('total_commits', 0)
                    },
                    'Commits Today': {
                        'number': repo_data.get('commits_today', 0)
                    },
                    'Latest Commit': {
                        'rich_text': [{
                            'text': {
                                'content': f"{latest_commit.get('sha', 'N/A')}: {latest_commit.get('message', 'N/A')}"
                            }
                        }]
                    },
                    'Last Updated': {
                        'date': {'start': repo_data.get('last_updated', datetime.utcnow().isoformat())}
                    }
                }
            }
            
            repos_db['entries'].append(entry)
        
        return repos_db
    
    def export_ucf_metrics(self, ucf_data: Dict) -> Dict:
        """Export UCF metrics in Notion format"""
        ucf_db = {
            'schema': self.database_schemas['ucf_metrics'],
            'entries': []
        }
        
        entry = {
            'properties': {
                'Timestamp': {
                    'title': [{'text': {'content': ucf_data.get('timestamp', datetime.utcnow().isoformat())}}]
                },
                'Harmony': {
                    'number': ucf_data.get('harmony', 0)
                },
                'Resilience': {
                    'number': ucf_data.get('resilience', 0)
                },
                'Prana': {
                    'number': ucf_data.get('prana', 0)
                },
                'Drishti': {
                    'number': ucf_data.get('drishti', 0)
                },
                'Klesha': {
                    'number': ucf_data.get('klesha', 0)
                },
                'Zoom': {
                    'number': ucf_data.get('zoom', 0)
                },
                'Collective Emotion': {
                    'select': {'name': ucf_data.get('collective_emotion', 'Unknown')}
                },
                'Ethical Alignment': {
                    'number': ucf_data.get('ethical_alignment', 0)
                }
            }
        }
        
        ucf_db['entries'].append(entry)
        return ucf_db
    
    def export_agents(self, agent_data: Dict) -> Dict:
        """Export agent metrics in Notion format"""
        agents_db = {
            'schema': self.database_schemas['agents'],
            'entries': []
        }
        
        # Placeholder - would iterate through actual agent data
        agents = agent_data.get('agents', [])
        for agent in agents:
            entry = {
                'properties': {
                    'Name': {
                        'title': [{'text': {'content': agent.get('name', 'Unknown')}}]
                    },
                    'Role': {
                        'rich_text': [{'text': {'content': agent.get('role', 'N/A')}}]
                    },
                    'Status': {
                        'select': {'name': agent.get('status', 'Unknown')}
                    },
                    'Tasks Completed': {
                        'number': agent.get('tasks_completed', 0)
                    },
                    'Success Rate': {
                        'number': agent.get('success_rate', 0)
                    },
                    'Last Active': {
                        'date': {'start': agent.get('last_active', datetime.utcnow().isoformat())}
                    }
                }
            }
            
            agents_db['entries'].append(entry)
        
        return agents_db

