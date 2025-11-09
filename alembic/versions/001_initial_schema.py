"""Initial database schema for Helix Collective

Revision ID: 001
Revises:
Create Date: 2025-11-08 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables for Helix Collective."""

    # UCF State table
    op.create_table(
        'ucf_state',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('harmony', sa.Float(), nullable=False),
        sa.Column('resilience', sa.Float(), nullable=False),
        sa.Column('prana', sa.Float(), nullable=False),
        sa.Column('drishti', sa.Float(), nullable=False),
        sa.Column('klesha', sa.Float(), nullable=False),
        sa.Column('zoom', sa.Float(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ucf_state_timestamp'), 'ucf_state', ['timestamp'])

    # Agent State table
    op.create_table(
        'agent_state',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_name', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('consciousness', sa.Float(), nullable=False),
        sa.Column('current_task', sa.Text(), nullable=True),
        sa.Column('last_update', sa.DateTime(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_state_name'), 'agent_state', ['agent_name'])
    op.create_index(op.f('ix_agent_state_update'), 'agent_state', ['last_update'])

    # Event Log table
    op.create_table(
        'event_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('source', sa.String(100), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_log_timestamp'), 'event_log', ['timestamp'])
    op.create_index(op.f('ix_event_log_type'), 'event_log', ['event_type'])

    # Command History table
    op.create_table(
        'command_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('command', sa.String(500), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=False),
        sa.Column('channel_id', sa.String(100), nullable=True),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_command_history_timestamp'), 'command_history', ['timestamp'])
    op.create_index(op.f('ix_command_history_user'), 'command_history', ['user_id'])

    # Ritual Execution table
    op.create_table(
        'ritual_execution',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('steps', sa.Integer(), nullable=False),
        sa.Column('initiated_by', sa.String(100), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('final_state', sa.JSON(), nullable=True),
        sa.Column('anomalies', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ritual_execution_timestamp'), 'ritual_execution', ['timestamp'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index(op.f('ix_ritual_execution_timestamp'), table_name='ritual_execution')
    op.drop_table('ritual_execution')

    op.drop_index(op.f('ix_command_history_user'), table_name='command_history')
    op.drop_index(op.f('ix_command_history_timestamp'), table_name='command_history')
    op.drop_table('command_history')

    op.drop_index(op.f('ix_event_log_type'), table_name='event_log')
    op.drop_index(op.f('ix_event_log_timestamp'), table_name='event_log')
    op.drop_table('event_log')

    op.drop_index(op.f('ix_agent_state_update'), table_name='agent_state')
    op.drop_index(op.f('ix_agent_state_name'), table_name='agent_state')
    op.drop_table('agent_state')

    op.drop_index(op.f('ix_ucf_state_timestamp'), table_name='ucf_state')
    op.drop_table('ucf_state')
