from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.exc import StatementError

from fast_zero.models import Todo, User


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
            'todos': [],
        }


@pytest.mark.asyncio
async def test_create_todo(session, user, mock_db_time):
    with mock_db_time(model=Todo) as time:
        todo = Todo(
            title='Test todo',
            description='Test desc',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()

        todo = await session.scalar(select(Todo))

        assert asdict(todo) == {
            'description': 'Test desc',
            'state': 'draft',
            'user_id': 1,
            'title': 'Test todo',
            'id': 1,
            'created_at': time,
            'updated_at': time,
        }


@pytest.mark.asyncio
async def test_create_todo_enum_error(session, user):
    todo = Todo(
        title='test',
        description='description',
        state='invalid',
        user_id=user.id,
    )

    session.add(todo)

    with pytest.raises(StatementError):
        await session.commit()
