"""create_news_table

Revision ID: 798880f8f92b
Revises: a91b80e0e206
Create Date: 2026-09-14 21:31:41.820559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '798880f8f92b'
down_revision: Union[str, Sequence[str], None] = 'a91b80e0e206'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """--sql
        CREATE TABLE IF NOT EXISTS trending_news(
            id BIGSERIAL PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source VARCHAR(50) DEFAULT 'cnn',
            published_at TIMESTAMP,
            is_done BOOLEAN DEFAULT FALSE,
            scraped_at TIMESTAMP DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_unread_news ON trending_news(id) WHERE is_done = FALSE;

        """
    )


def downgrade() -> None:
    op.execute(
        """--sql
        DROP TABLE IF EXISTS trending_news;
        """
    )
