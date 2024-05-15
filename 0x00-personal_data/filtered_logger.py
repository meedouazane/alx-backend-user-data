#!/usr/bin/env python3
""" Personal data """
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    :param fields: a list of strings representing all fields to obfuscate
    :param redaction: a string that will be obfuscated with
    :param message: a string representing the log line
    :param separator: a string representing by which character is separating
    all fields in the log line (message)
    :return: returns the log message obfuscated
    """
    text = message.split(separator)
    for i in range(len(text)):
        text[i] = re.sub(r'=(.*)', '=' + redaction, text[i]) \
            if any(field in text[i] for field in fields) \
            else text[i]
    return separator.join(text)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum """
        filtered_message = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)
        record.msg = filtered_message
        return super().format(record)


PII_FIELDS = ('name', 'phone', 'ssn', 'password', 'email')


def get_logger() -> logging.Logger:
    """ Create logger  """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connect to secure database """
    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return connection


def main():
    """ """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field = [i[0] for i in cursor.description]
    logger = get_logger()
    info = ''
    for row in cursor:
        for rw, fld in zip(row, field):
            info += f'{fld}={(rw)}; '
        logger.info(info)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
