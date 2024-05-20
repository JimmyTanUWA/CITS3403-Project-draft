"""Initial migration

Revision ID: a66283095433
Revises: d8495aff7ac9
Create Date: 2024-05-20 12:55:16.406987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a66283095433'
down_revision = 'd8495aff7ac9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('replies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.String(length=1000), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('dislikes', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_column('dislikes')
        batch_op.drop_column('likes')

    op.drop_table('replies')
    # ### end Alembic commands ###
