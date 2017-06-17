"""Create reminders table

Revision ID: d93e41375c88
Revises: 
Create Date: 2017-06-18 00:05:48.201116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd93e41375c88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reminders',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('chat_id', sa.BigInteger, index=True),
        sa.Column('message_text', sa.Text),
        sa.Column('remind_at', sa.DateTime, index=True),
        sa.Column('is_repeatable', sa.Boolean),
        sa.Column('interval_text', sa.Unicode(100))
    )


def downgrade():
    op.drop_table('reminders')
