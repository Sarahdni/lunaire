from .ical_generator import ICalGenerator

class CalendarFactory:
    @staticmethod
    def get_generator(calendar_type):
        if calendar_type.lower() in ["ical", "apple", "google", "outlook"]:
            return ICalGenerator()
        else:
            raise ValueError(f"Unsupported calendar type: {calendar_type}. Using iCal format for all types.")