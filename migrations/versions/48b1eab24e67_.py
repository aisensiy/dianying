"""empty message

Revision ID: 48b1eab24e67
Revises: 1cbbb889f387
Create Date: 2014-01-06 23:29:27.338946

"""

# revision identifiers, used by Alembic.
revision = '48b1eab24e67'
down_revision = '1cbbb889f387'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('last_read', sa.Column('owner_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('last_read', 'owner_id')
    ### end Alembic commands ###