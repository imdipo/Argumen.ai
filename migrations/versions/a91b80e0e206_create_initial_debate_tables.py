"""create_initial_debate_tables

Revision ID: a91b80e0e206
Revises:
Create Date: 2026-09-13 17:04:32.653870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a91b80e0e206'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """--sql
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    roblox_user_id BIGINT UNIQUE NOT NULL,
    roblox_username VARCHAR(50) NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS debate_topics (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    model_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled / done
    created_at TIMESTAMP DEFAULT NOW(),

    created_by BIGINT NOT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS debate_messages (
    id BIGSERIAL PRIMARY KEY,
    topic_id BIGINT NOT NULL REFERENCES debate_topics(id) ON DELETE CASCADE,
    round_number INT NOT NULL,

    bot_a VARCHAR(50) NOT NULL,
    bot_b VARCHAR(50) NOT NULL,

    argument_text TEXT NOT NULL,
    tokens_used INT,
    response_latency_ms INT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS users_vote (
    id BIGSERIAL PRIMARY KEY,
    topic_id BIGINT UNIQUE NOT NULL REFERENCES debate_topics(id) ON DELETE CASCADE,

    voter VARCHAR(100) NOT NULL,
    voted_for VARCHAR(20) NOT NULL, -- apakah pro/kontra
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_vote_per_topic UNIQUE (topic_id, voter)
    );

CREATE INDEX IF NOT EXISTS idx_votes_target ON users_vote (topic_id, voted_for)
        """
    )


def downgrade() -> None:
    op.execute("""--sql
        DROP TABLE IF EXISTS users_vote CASCADE;
        DROP TABLE IF EXISTS debate_messages CASCADE;
        DROP TABLE IF EXISTS debate_topics CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        """)
