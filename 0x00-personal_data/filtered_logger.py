#!/usr/bin/env python3
""" Personal data """
import re
from typing import List
import logging


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
            if any(field in text[i] for field in fields)\
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
        record.msg = filtered_message.replace(';', '; ')
        return super().format(record)
