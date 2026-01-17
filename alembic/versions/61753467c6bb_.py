"""empty message

Revision ID: 61753467c6bb
Revises: 5a866c39c0e7
Create Date: 2026-01-09 19:51:01.040285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61753467c6bb'
down_revision: Union[str, Sequence[str], None] = '5a866c39c0e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
