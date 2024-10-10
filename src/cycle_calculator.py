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

def load_mantras(file_path='docs/mantras_list.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_mantra(phase, date, mantras):
    month = date.strftime('%B')
    day = date.day
    
    if day <= 10:
        index = 0  # Beginning
    elif day <= 20:
        index = 1  # Middle
    else:
        index = 2  # End
    
    try:
        mantra = mantras[phase][month][index]
        return mantra.split(': ', 1)[1]  # Retourne seulement la partie après ": "
    except (KeyError, IndexError):
        return f"Mantra not available for {phase} phase, {month}, index {index}."

def calculate_cycle(start_date, cycle_length, period_length, num_months=12):
    if isinstance(start_date, str):
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            try:
                start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD' or 'DD/MM/YYYY'")
    
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

def create_apple_calendar(phases, user_info, phase_descriptions, mantras):
    # Pour Apple Calendar, nous pouvons utiliser le même format que iCal
    return create_ical(phases, user_info, phase_descriptions, mantras)

