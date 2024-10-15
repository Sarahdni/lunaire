from icalendar import Calendar, Event
from datetime import datetime
from utils.logger import logger
from .recommendations import generate_recommendations


class ICalGenerator:
    def generate(self, phases, user_info, phase_descriptions, mantras):
        cal = Calendar()
        for phase_name, start, end in phases:
            event = self.create_event(phase_name, start, end, phase_descriptions[phase_name], mantras[phase_name])
            cal.add_component(event)
        return cal.to_ical()

    def create_event(self, phase_name, start, end, phase_info, mantra):
        logger.info(f"Creating event for phase: {phase_name}")
        logger.info(f"Event period: {start.date()} to {end.date()}")
        
        event = Event()
        
        # Logging the title
        title = phase_info['title']
        logger.info(f"Event title: {title}")
        event.add('summary', title)
        
        event.add('dtstart', start.date())
        event.add('dtend', end.date())
        
        # Logging before generating description
        logger.info(f"Generating description for {phase_name}")
        logger.debug(f"Phase info: {phase_info}")
        logger.debug(f"Mantra: {mantra}")
        
        description = self.generate_description(phase_info, mantra, start)
        logger.info(f"Generated description length: {len(description)} characters")
        logger.debug(f"Description preview: {description[:100]}...")  # Log les 100 premiers caractères
        
        event.add('description', description)
        
        logger.info(f"Event created successfully for {phase_name}")
        return event

    def get_mantra_based_on_date(self, phase_mantra, start_date):
        """
        Selects the appropriate mantra based on the day of the month.
        - Beginning: days 1-10
        - Middle: days 11-20
        - End: days 21+
        """
        day = start_date.day
        if day <= 10:
            return phase_mantra[0]  # Beginning
        elif day <= 20:
            return phase_mantra[1]  # Middle
        else:
            return phase_mantra[2]  # End

    def generate_description(self, phase_info, mantra, start_date):
        current_month = start_date.strftime("%B")
        
        # Select the appropriate mantra based on the start date
        if current_month in mantra:
            full_mantra = self.get_mantra_based_on_date(mantra[current_month], start_date)
            # Remove the prefix (e.g., "Beginning: ") and surround with stars
            month_mantra = f"✨ {full_mantra.split(': ', 1)[-1]} ✨"
        else:
            month_mantra = "✨ No mantra available ✨"

        # Start building the description
        description = f"{phase_info['description']['phase_info']['text']}\n\n"
        description += f"{month_mantra}\n\n"  # Add the mantra without prefix

        # Add sports recommendations
        description += generate_recommendations("🏋️‍♀️ Sports recommendations", phase_info['description']['sports_recommendations'])
        
        # Add nutrition recommendations
        description += generate_recommendations("🍽️ Nutrition recommendations", phase_info['description']['nutrition']['recommended_foods'])
        
        # Add foods to avoid
        description += generate_recommendations("🚫 Foods to avoid", phase_info['description']['nutrition']['foods_to_avoid'])
        
        # Add vitamins and supplements
        description += generate_recommendations("💊 Vitamins & Supplements", phase_info['description']['vitamins_supplements'])
        
        # Add seed cycling recommendations
        description += "\n🌻 Seed Cycling:\n"
        description += f"• Seeds: {', '.join(phase_info['description']['seed_cycling']['seeds'])}\n"
        description += f"• Benefits: {phase_info['description']['seed_cycling']['benefits']}\n"
        
        # Add self-care tips
        description += generate_recommendations("🧘‍♀️ Self-Care Tips", phase_info['description']['self_care_tips'])

        return description
    