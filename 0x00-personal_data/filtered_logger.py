#!/usr/bin/env python3
"""Module filttered_logger.py"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filtering data from log message"""
    pattern = '|'.join(f'({field}=[^;]*)' for field in fields)
    redact = {'pattern': lambda match: re.sub(r'=.+', f'={redaction}',
                                              match.group())}
    return re.sub(pattern, redact['pattern'], message)
