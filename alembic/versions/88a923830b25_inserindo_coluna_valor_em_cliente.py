"""inserindo coluna valor em cliente

Revision ID: 88a923830b25
Revises: 12fc7a8bc63b
Create Date: 2023-09-22 13:02:42.236270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88a923830b25'
down_revision: Union[str, None] = '12fc7a8bc63b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
