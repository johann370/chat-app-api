"""fixed foreign key from servers.id to users.id

Revision ID: 15f2fd224226
Revises: 6796bd6d1d10
Create Date: 2021-11-16 17:38:09.993681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15f2fd224226'
down_revision = '6796bd6d1d10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('servers_owner_id_fkey', 'servers', type_='foreignkey')
    op.create_foreign_key(None, 'servers', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'servers', type_='foreignkey')
    op.create_foreign_key('servers_owner_id_fkey', 'servers', 'servers', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
