from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, user):
    db_user = session.scalar(select(User).where(User.username == 'Teste'))

    assert db_user.username == 'Teste'
