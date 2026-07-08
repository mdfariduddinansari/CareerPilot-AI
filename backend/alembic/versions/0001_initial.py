"""initial schema"""

from alembic import op
import sqlalchemy as sa


revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def _timestamp_columns():
    return [
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        *_timestamp_columns(),
    )

    for table_name, extra_columns in [
        ('resumes', [sa.Column('resume_text', sa.Text(), nullable=False), sa.Column('overall_score', sa.Integer(), nullable=True), sa.Column('ats_score', sa.Integer(), nullable=True)]),
        ('ats_reports', [sa.Column('resume_text', sa.Text(), nullable=False), sa.Column('job_description', sa.Text(), nullable=False), sa.Column('match_percent', sa.Integer(), nullable=False)]),
        ('cover_letters', [sa.Column('company', sa.String(150), nullable=False), sa.Column('role', sa.String(150), nullable=False), sa.Column('tone', sa.String(50), nullable=False), sa.Column('content', sa.Text(), nullable=False)]),
        ('interviews', [sa.Column('company', sa.String(150), nullable=False), sa.Column('round_type', sa.String(50), nullable=False), sa.Column('questions', sa.Text(), nullable=False)]),
        ('interview_evaluations', [sa.Column('question', sa.Text(), nullable=False), sa.Column('answer', sa.Text(), nullable=False), sa.Column('overall_score', sa.Float(), nullable=False)]),
        ('job_applications', [sa.Column('company', sa.String(150), nullable=False), sa.Column('role', sa.String(150), nullable=False), sa.Column('status', sa.String(50), nullable=False, server_default='Wishlist')]),
        ('skills', [sa.Column('target_role', sa.String(150), nullable=False), sa.Column('current_skills', sa.Text(), nullable=False), sa.Column('analysis', sa.Text(), nullable=False)]),
        ('roadmaps', [sa.Column('target_role', sa.String(150), nullable=False), sa.Column('roadmap', sa.Text(), nullable=False)]),
        ('ai_usage', [sa.Column('feature', sa.String(100), nullable=False), sa.Column('provider', sa.String(50), nullable=False), sa.Column('metadata', sa.Text(), nullable=True)]),
        ('settings', [sa.Column('theme', sa.String(20), nullable=False, server_default='light')]),
    ]:
        op.create_table(
            table_name,
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
            *extra_columns,
            *_timestamp_columns(),
        )


def downgrade() -> None:
    for table in ['settings', 'ai_usage', 'roadmaps', 'skills', 'job_applications', 'interview_evaluations', 'interviews', 'cover_letters', 'ats_reports', 'resumes', 'users']:
        op.drop_table(table)
