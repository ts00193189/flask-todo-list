"""Add model

Revision ID: beeee9fb56c4
Revises: 
Create Date: 2022-05-02 15:14:32.196143

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'beeee9fb56c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=30), nullable=False),
                    sa.Column('password_hash', sa.String(
                        length=128), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('todos',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('task_name', sa.String(
                        length=255), nullable=False),
                    sa.Column('task_content', sa.Text(), nullable=False),
                    sa.Column('task_datetime', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    op.drop_table('users')
    # ### end Alembic commands ###
