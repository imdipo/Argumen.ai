"""add_column_to_table

Revision ID: 400ec43261a5
Revises: 798880f8f92b
Create Date: 2026-09-17 10:58:22.452674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '400ec43261a5'
down_revision: Union[str, Sequence[str], None] = '798880f8f92b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """--sql
        ALTER TABLE debate_topics
            ADD COLUMN IF NOT EXISTS bot_a VARCHAR(50) NOT NULL DEFAULT '',
            ADD COLUMN IF NOT EXISTS bot_b VARCHAR(50) NOT NULL DEFAULT '';
        """
    )


def downgrade() -> None:
    op.execute(
        """--sql
        ALTER TABLE debate_topics
            DROP COLUMN IF EXISTS bot_a,
            DROP COLUMN IF EXISTS bot_b;
        """
    )
