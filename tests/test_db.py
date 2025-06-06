from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='teste', password='teste', email='teste@test.com'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'teste'))

    assert asdict(user) == {
        'id': 1,
        'username': 'teste',
        'password': 'teste',
        'email': 'teste@test.com',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user, mock_db_time):
    with mock_db_time(model=Todo) as time:
        todo = Todo(
            title='Test Todo',
            description='Test description',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()

    todo = await session.scalar(select(Todo))

    assert asdict(todo) == {
        'description': 'Test description',
        'id': 1,
        'state': 'draft',
        'title': 'Test Todo',
        'created_at': time,
        'updated_at': time,
        'user_id': 1,
    }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
