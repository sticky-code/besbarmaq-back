"""empty message

Revision ID: 371f44c4a1e4
Revises: 
Create Date: 2024-12-22 05:32:00.721813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '371f44c4a1e4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('hashed_password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('rooms',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'CLOSED', 'IN_PROGRESS', name='roomstatustype'), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['host_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statistics',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('overall_wpm', sa.Integer(), nullable=False),
    sa.Column('overall_accuracy', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('room_statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('wpm', sa.Integer(), nullable=False),
    sa.Column('accuracy', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_rooms_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_rooms_association')
    op.drop_table('room_statistics')
    op.drop_table('statistics')
    op.drop_table('rooms')
    op.drop_table('users')
    # ### end Alembic commands ###
