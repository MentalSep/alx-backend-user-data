#!/usr/bin/env python3
"""Module filttered_logger.py"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filtering data from log message"""
    pattern = rf"(?:{separator})({'|'.join(fields)})=(.*?)(?={separator}|$)"
    return re.sub(pattern, rf"\1={redaction}", message)
