"""
Mail Services Package

This package handles email operations for the cycle sync application.
It includes functionality for receiving emails, parsing their content,
and sending emails to users.
"""

from .email_receiver import (
    connect_to_email,
    get_unprocessed_emails,
    parse_email_content,
    extract_info
)

from .email_sender import send_email_to_user

__all__ = [
    'connect_to_email',
    'get_unprocessed_emails',
    'parse_email_content',
    'extract_info',
    'send_email_to_user'
]