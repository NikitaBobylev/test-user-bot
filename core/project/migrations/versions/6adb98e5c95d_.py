"""empty message

Revision ID: 6adb98e5c95d
Revises: 
Create Date: 2024-05-19 15:22:29.646158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6adb98e5c95d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('telegram_id', sa.String(), nullable=False),
                    sa.Column('status', sa.Enum('alive', 'dead', 'finished', name='status').with_variant(
                        postgresql.ENUM(
                            "alive",
                            "dead",
                            "finished",
                            name="status",
                            create_type=False,
                        ),
                        "postgresql",
                    ),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=False),
                    sa.Column('status_updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=False),
                    sa.Column('to_send_message', sa.DateTime(), nullable=False),
                    sa.Column('stage', sa.Enum('first', 'second', 'last', name='stage'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('telegram_id')
                    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('telegram_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('status', postgresql.ENUM('alive', 'dead', 'finish', name='status'), autoincrement=False,
                              nullable=False),
                    sa.Column('status_updated_at', postgresql.TIMESTAMP(),
                              server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False,
                              nullable=False),
                    sa.PrimaryKeyConstraint('id', name='users_pkey'),
                    sa.UniqueConstraint('telegram_id', name='users_telegram_id_key')
                    )
    op.drop_table('telegram_users')
    # ### end Alembic commands ###
