"""
Calendars Package

This package provides functionality for generating different types of calendars.
It includes a factory for creating calendar generators and specific generators
for iCal, Google Calendar, Outlook, and Apple Calendar formats.
"""

from .calendar_factory import CalendarFactory
from .cycle_calculator import calculate_cycle

__all__ = ['CalendarFactory', 'calculate_cycle']