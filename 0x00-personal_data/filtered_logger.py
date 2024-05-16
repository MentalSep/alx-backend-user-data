#!/usr/bin/env python3
"""Module filttered_logger.py"""
import re


def filter_datum(fields, redaction, message, separator):
    """Filtering data from log message"""
    pattern = rf"(?:{separator})({'|'.join(fields)})=(.*?)(?={separator}|$)"
    return re.sub(pattern, rf"\1={redaction}", message)
