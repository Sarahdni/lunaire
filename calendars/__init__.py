"""
Calendars Package
This package provides functionality for generating iCal format calendars,
calculating menstrual cycle phases, and generating recommendations.
"""

from .cycle_calculator import calculate_cycle
from .ical_generator import ICalGenerator
from .recommendations import generate_recommendations

__all__ = ['calculate_cycle', 'ICalGenerator', 'generate_recommendations']