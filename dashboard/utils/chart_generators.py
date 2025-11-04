#!/usr/bin/env python3
"""
🌀 Helix Collective v15.3 — Chart Generators
dashboard/utils/chart_generators.py

Visualization utilities for creating beautiful charts and graphs:
- UCF gauge charts
- Radar charts
- Agent health bars
- Ritual timelines
- Sync operation trends

Author: Manus AI
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generate beautiful charts for dashboard."""
    
    @staticmethod
    def create_ucf_gauge(value: float, name: str, min_val: float = 0, max_val: float = 1) -> go.Figure:
        """
        Create a gauge chart for UCF metrics.
        
        Args:
            value: Current metric value
            name: Metric name
            min_val: Minimum value for gauge
            max_val: Maximum value for gauge
        
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=[go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={'text': name, 'font': {'size': 20}},
            delta={'reference': (min_val + max_val) / 2},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [min_val, max_val * 0.33], 'color': "lightgray"},
                    {'range': [max_val * 0.33, max_val * 0.66], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_val * 0.8
                }
            }
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def create_ucf_radar(ucf_state: Dict[str, Any]) -> go.Figure:
        """
        Create a radar chart showing all UCF metrics.
        
        Args:
            ucf_state: Dictionary with UCF metrics
        
        Returns:
            Plotly figure
        """
        metrics = ['harmony', 'resilience', 'prana', 'drishti', 'klesha', 'zoom']
        values = [ucf_state.get(m, 0) for m in metrics]
        
        # Normalize resilience and zoom to 0-1 range for radar
        if values[1] > 1:  # resilience
            values[1] = min(1, values[1] / 2)
        if values[5] > 1:  # zoom
            values[5] = min(1, values[5] / 2)
        
        # Invert klesha (lower is better)
        values[4] = 1 - values[4]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=[m.capitalize() for m in metrics],
            fill='toself',
            name='Current State',
            line=dict(color='#8A2BE2'),
            fillcolor='rgba(138, 43, 226, 0.3)'
        ))
        
        # Add target line
        targets = [0.60, 0.45, 0.70, 0.80, 0.10, 0.575]  # Normalized targets
        fig.add_trace(go.Scatterpolar(
            r=targets,
            theta=[m.capitalize() for m in metrics],
            fill='toself',
            name='Target State',
            line=dict(color='#FFD700'),
            fillcolor='rgba(255, 215, 0, 0.1)'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def create_agent_health_chart(agents: List[Dict[str, Any]]) -> go.Figure:
        """
        Create a bar chart showing agent health scores.
        
        Args:
            agents: List of agent dictionaries
        
        Returns:
            Plotly figure
        """
        if not agents:
            return go.Figure()
        
        df = pd.DataFrame(agents)
        
        fig = px.bar(
            df,
            x='name',
            y='health',
            color='health',
            color_continuous_scale='RdYlGn',
            title='Agent Health Scores',
            labels={'health': 'Health Score (%)', 'name': 'Agent'},
            height=400
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            margin=dict(l=20, r=20, t=40, b=80),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def create_agent_status_pie(agents: List[Dict[str, Any]]) -> go.Figure:
        """
        Create a pie chart showing agent status distribution.
        
        Args:
            agents: List of agent dictionaries
        
        Returns:
            Plotly figure
        """
        if not agents:
            return go.Figure()
        
        status_counts = {}
        for agent in agents:
            status = agent.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig = go.Figure(data=[go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            hole=0.3
        )])
        
        fig.update_layout(
            title='Agent Status Distribution',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def create_ritual_timeline(rituals: pd.DataFrame) -> go.Figure:
        """
        Create a timeline of ritual executions.
        
        Args:
            rituals: DataFrame with ritual history
        
        Returns:
            Plotly figure
        """
        if rituals.empty:
            return go.Figure()
        
        # Ensure we have timestamp column
        if 'timestamp' not in rituals.columns:
            return go.Figure()
        
        rituals_sorted = rituals.sort_values('timestamp', ascending=False).head(20)
        
        fig = px.scatter(
            rituals_sorted,
            x='timestamp',
            y='steps',
            size='steps',
            color='steps',
            hover_data=['timestamp', 'steps'],
            title='Ritual Execution Timeline (Last 20)',
            labels={'timestamp': 'Time', 'steps': 'Steps'},
            height=400
        )
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def create_sync_trend(sync_logs: Dict[str, Any]) -> go.Figure:
        """
        Create a trend chart for sync operations.
        
        Args:
            sync_logs: Dictionary with sync history
        
        Returns:
            Plotly figure
        """
        history = sync_logs.get('sync_history', [])
        
        if not history:
            return go.Figure()
        
        # Extract data for chart
        cycles = []
        success_counts = []
        
        for sync in history[-20:]:  # Last 20 syncs
            cycles.append(sync.get('cycle_number', 0))
            
            results = sync.get('results', {})
            success = sum(1 for r in results.values() if r.get('status') == 'success')
            success_counts.append(success)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=cycles,
            y=success_counts,
            mode='lines+markers',
            name='Successful Operations',
            line=dict(color='#00FF00', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Sync Operation Success Rate',
            xaxis_title='Cycle Number',
            yaxis_title='Successful Operations',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def create_ucf_history(ucf_history: List[Dict[str, Any]]) -> go.Figure:
        """
        Create a line chart showing UCF metrics history.
        
        Args:
            ucf_history: List of historical UCF states
        
        Returns:
            Plotly figure
        """
        if not ucf_history:
            return go.Figure()
        
        df = pd.DataFrame(ucf_history)
        
        fig = go.Figure()
        
        metrics = ['harmony', 'resilience', 'prana', 'drishti', 'klesha', 'zoom']
        colors = ['#8A2BE2', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for metric, color in zip(metrics, colors):
            if metric in df.columns:
                fig.add_trace(go.Scatter(
                    y=df[metric],
                    name=metric.capitalize(),
                    line=dict(color=color, width=2),
                    mode='lines'
                ))
        
        fig.update_layout(
            title='UCF Metrics History',
            xaxis_title='Time',
            yaxis_title='Metric Value',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_system_health_gauge(health_score: float) -> go.Figure:
        """
        Create a gauge chart for overall system health.
        
        Args:
            health_score: Overall health score (0-100)
        
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=[go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "System Health", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "lightcoral"},
                    {'range': [33, 66], 'color': "lightyellow"},
                    {'range': [66, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        )])
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig

