#!/usr/bin/env python3
"""Module filttered_logger.py"""
import re
from typing import List, Union
import logging
import os
import mysql.connector

PII_FIELDS = ("email", "ssn", "password", "phone", "name")


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
        """Format log record"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filtering data from log message"""
    pattern = rf'({"|".join(fields)})=([^{separator}]*)'
    return re.sub(pattern,
                  lambda match: f"{match.group(1)}={redaction}",
                  message)


def get_logger() -> logging.Logger:
    """Get logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    )


def main():
    """Main function"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        formatted_row = "; ".join([f"{field}={value}" for field, value
                                   in zip(cursor.column_names, row)]) + ";"
        logger.info(formatted_row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
