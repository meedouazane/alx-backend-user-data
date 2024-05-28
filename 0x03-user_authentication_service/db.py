#!/usr/bin/env python3
"""DB module
"""
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base


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
        """
        Add and save user to database
        :param email: email of user
        :param hashed_password: password of user
        :return: User object
        """
        user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        return user

    def find_user_by(self, **keyword: Dict[str, str]) -> User:
        """
        Get the first row found in the users table
        :param keyword: Arbitrary keyword arguments
        :return: The first row found in the users table
        """
        session = self._session
        try:
            user = self.session(User).filter_by(**keyword).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **keyword: Dict[str, str]) -> None:
        """
        Update user by their user_id
        :param user_id: id of user
        :param keyword: Arbitrary keyword arguments
        :return: None
        """
        session = self._session
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError
        for key, value in keyword.items():
            if not hasattr(user, key):
                raise ValueError
            user.key = value
        session.commit()
        return None
