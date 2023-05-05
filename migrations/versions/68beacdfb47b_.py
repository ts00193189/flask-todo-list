"""Modify model

Revision ID: 68beacdfb47b
Revises: beeee9fb56c4
Create Date: 2022-05-07 01:36:42.377083

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '68beacdfb47b'
down_revision = 'beeee9fb56c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('task_date', sa.Date(), nullable=False))
    op.add_column('todos', sa.Column('task_time', sa.Time(), nullable=False))
    op.drop_column('todos', 'task_datetime')
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.add_column('todos', sa.Column(
        'task_datetime', sa.DATETIME(), nullable=False))
    op.drop_column('todos', 'task_time')
    op.drop_column('todos', 'task_date')
    # ### end Alembic commands ###
