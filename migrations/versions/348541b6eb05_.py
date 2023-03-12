"""empty message

Revision ID: 348541b6eb05
Revises: 7d57d1648936
Create Date: 2023-03-12 20:33:01.463696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '348541b6eb05'
down_revision = '7d57d1648936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
