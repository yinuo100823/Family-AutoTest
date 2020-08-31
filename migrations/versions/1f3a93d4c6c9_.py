"""empty message

Revision ID: 1f3a93d4c6c9
Revises: 
Create Date: 2020-08-31 09:42:39.530140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f3a93d4c6c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bt_interface', sa.Column('body', sa.Text(), nullable=False, comment='请求体'))
    op.add_column('bt_interface', sa.Column('method', sa.String(length=10), nullable=False, comment='请求方式'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bt_interface', 'method')
    op.drop_column('bt_interface', 'body')
    # ### end Alembic commands ###
