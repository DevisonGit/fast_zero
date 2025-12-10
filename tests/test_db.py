from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='aline', password='secret', email='aline@teste.com'
        )
        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'aline')
        )

        assert asdict(user) == {
            'id': 1,
            'username': 'aline',
            'password': 'secret',
            'email': 'aline@teste.com',
            'created_at': time,
            'updated_at': time,
        }
