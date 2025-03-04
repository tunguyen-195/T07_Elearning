"""Add class link to assignments

Revision ID: ac1023b63aa6
Revises: 4cd586b4fdaf
Create Date: 2025-03-02 11:07:19.291764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac1023b63aa6'
down_revision = '4cd586b4fdaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('class_link', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.drop_column('class_link')

    # ### end Alembic commands ###
