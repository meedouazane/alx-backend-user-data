#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add and save user to database """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **keyword):
        """ returns the first row found in the users table """
        user = self._session.query(User).filter_by(**keyword).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id, **keyword):
        """ update user by their user_id """
        user = self.find_user_by(id=user_id)
        for key, value in keyword.items():
            if not hasattr(user, key):
                raise ValueError
            user.key = value
        self._session.commit()
        return None
