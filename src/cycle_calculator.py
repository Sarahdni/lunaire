import datetime
from icalendar import Calendar, Event
import csv
import io
import json
import os
import importlib.util

def load_phase_descriptions(file_path='docs/phase_descriptions.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_mantras():
    spec = importlib.util.spec_from_file_location("mantras_list", "docs/mantras_list.py")
    mantras_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mantras_module)
    return mantras_module

def get_mantra(phase, date, mantras):
    month = date.strftime('%B')
    day = date.day
    
    if day <= 10:
        period = "Beginning"
    elif day <= 20:
        period = "Middle"
    else:
        period = "End"
    
    try:
        return mantras.__dict__[phase][month][period]
    except KeyError:
        return "Mantra not available for this period."

def calculate_cycle(start_date, cycle_length, period_length, num_months=12):
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    elif not isinstance(start_date, datetime.datetime):
        raise ValueError("start_date must be a string in format 'dd/mm/yyyy' or a datetime object")
    
    all_phases = []
    current_date = start_date
    for _ in range(num_months):
        cycle_end = current_date + datetime.timedelta(days=cycle_length)
        phases = [
            ("Menstrual", current_date, current_date + datetime.timedelta(days=period_length)),
            ("Follicular", current_date + datetime.timedelta(days=period_length), current_date + datetime.timedelta(days=cycle_length // 2 - 2)),
            ("Ovulatory", current_date + datetime.timedelta(days=cycle_length // 2 - 2), current_date + datetime.timedelta(days=cycle_length // 2 + 2)),
            ("Luteal", current_date + datetime.timedelta(days=cycle_length // 2 + 2), cycle_end)
        ]
        all_phases.extend(phases)
        current_date = cycle_end
    return all_phases

def create_ical(phases, user_info, phase_descriptions, mantras):
    cal = Calendar()
    for phase_name, start, end in phases:
        event = Event()
        phase_info = phase_descriptions[phase_name]
        mantra = get_mantra(phase_name, start, mantras)
        
        event.add('summary', phase_info['title'])
        event.add('dtstart', start.date())
        event.add('dtend', end.date())
        
        description = f"Mantra: {mantra}\n\n"
        description += f"Phase: {phase_info['description']['phase_info']['text']}\n"
        description += "Sports recommendations:\n"
        for sport in phase_info['description']['sports_recommendations']:
            if isinstance(sport, dict):
                description += f"- {sport['text']}\n"
            else:
                description += f"- {sport}\n"
        description += "\nNutrition recommendations:\n"
        for food in phase_info['description']['nutrition']['recommended_foods']:
            if isinstance(food, dict):
                description += f"- {food['text']}\n"
            else:
                description += f"- {food}\n"
        
        event.add('description', description)
        cal.add_component(event)
    return cal.to_ical()

def create_google_calendar(phases, user_info, phase_descriptions, mantras):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Subject", "Start Date", "End Date", "All Day Event", "Description"])
    for phase_name, start, end in phases:
        phase_info = phase_descriptions[phase_name]
        mantra = get_mantra(phase_name, start, mantras)
        
        description = f"Mantra: {mantra}\n\n"
        description += f"Phase: {phase_info['description']['phase_info']['text']}\n"
        description += "Sports recommendations:\n"
        for sport in phase_info['description']['sports_recommendations']:
            if isinstance(sport, dict):
                description += f"- {sport['text']}\n"
            else:
                description += f"- {sport}\n"
        description += "\nNutrition recommendations:\n"
        for food in phase_info['description']['nutrition']['recommended_foods']:
            if isinstance(food, dict):
                description += f"- {food['text']}\n"
            else:
                description += f"- {food}\n"
        
        writer.writerow([
            phase_info['title'],
            start.strftime("%m/%d/%Y"),
            end.strftime("%m/%d/%Y"),
            "True",
            description
        ])
    return output.getvalue().encode('utf-8')

def create_outlook_calendar(phases, user_info, phase_descriptions, mantras):
    return create_google_calendar(phases, user_info, phase_descriptions, mantras)

# Example usage
if __name__ == "__main__":
    user_info = {
        "Nom": "Jane Doe",
        "start_date": "01/05/2023",
        "cycle_length": 28,
        "period_length": 5
    }
    
    phase_descriptions = load_phase_descriptions()
    mantras = load_mantras()
    
    phases = calculate_cycle(user_info['start_date'], user_info['cycle_length'], user_info['period_length'])
    
    ical_data = create_ical(phases, user_info, phase_descriptions, mantras)
    with open('menstrual_cycle.ics', 'wb') as f:
        f.write(ical_data)
    
    google_cal_data = create_google_calendar(phases, user_info, phase_descriptions, mantras)
    with open('menstrual_cycle_google.csv', 'wb') as f:
        f.write(google_cal_data)
    
    outlook_cal_data = create_outlook_calendar(phases, user_info, phase_descriptions, mantras)
    with open('menstrual_cycle_outlook.csv', 'wb') as f:
        f.write(outlook_cal_data)