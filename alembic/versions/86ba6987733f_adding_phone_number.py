"""adding phone number

Revision ID: 86ba6987733f
Revises: 
Create Date: 2024-09-12 00:57:08.653574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86ba6987733f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the column as nullable first
    op.add_column('posts', sa.Column('test', sa.String(), nullable=True))
    
    # Update existing rows with a default value
    op.execute("UPDATE posts SET test = 'default_value' WHERE test IS NULL")
    
    # Alter the column to make it non-nullable
    op.alter_column('posts', 'test', nullable=False)

def downgrade():
    op.drop_column('posts', 'test')
