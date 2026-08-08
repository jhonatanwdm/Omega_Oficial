"""baseline schema note

Revision ID: 0001_baseline
Revises:
Create Date: 2026-03-08
"""

from typing import Sequence, Union

revision: str = "0001_baseline"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Schema atual é criado por SQLModel no startup do hub.
    # Próximas revisões devem alterar tabelas aqui.
    pass


def downgrade() -> None:
    pass
