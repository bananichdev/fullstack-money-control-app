"""init_database

Revision ID: 31dde883fa54
Revises: 
Create Date: 2024-04-20 16:21:29.728983

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "31dde883fa54"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("admission_date", sa.Date(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="passport",
    )
    op.create_index(
        op.f("ix_accounts_account_id"),
        "account",
        ["id"],
        unique=False,
        schema="passport",
    )
    op.create_table(
        "operations",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column(
            "type", sa.Enum("пополнение", "списание", native_enum=False), nullable=False
        ),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["passport.account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="passport",
    )
    op.create_index(
        op.f("ix_accounts_operations_id"),
        "operations",
        ["id"],
        unique=False,
        schema="passport",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_accounts_operations_id"), table_name="operations", schema="passport"
    )
    op.drop_table("operations", schema="passport")
    op.drop_index(
        op.f("ix_accounts_account_id"), table_name="account", schema="passport"
    )
    op.drop_table("account", schema="passport")
    # ### end Alembic commands ###
