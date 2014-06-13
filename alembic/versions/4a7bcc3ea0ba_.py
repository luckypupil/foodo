"""empty message

Revision ID: 4a7bcc3ea0ba
Revises: 4150a1162c3e
Create Date: 2014-06-04 15:49:48.909310

"""

# revision identifiers, used by Alembic.
revision = '4a7bcc3ea0ba'
down_revision = '4150a1162c3e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('nameindex', table_name='rest')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('nameindex', 'rest', ['tsv'], unique=False)
    ### end Alembic commands ###
