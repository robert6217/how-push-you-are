"""empty message

Revision ID: 316362fb1822
Revises: 
Create Date: 2018-12-25 10:21:53.571826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '316362fb1822'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserAccounts',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('UserName', sa.String(length=10), nullable=True),
    sa.Column('UserPic', sa.Text(), nullable=True),
    sa.Column('FBuserID', sa.String(length=30), nullable=True),
    sa.Column('FBAccessToken', sa.String(length=256), nullable=True),
    sa.Column('CreateDate', sa.DateTime(), nullable=True),
    sa.Column('ModifiedDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserAccounts')
    # ### end Alembic commands ###
