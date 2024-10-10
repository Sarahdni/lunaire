import datetime
from icalendar import Calendar, Event
import csv
import io
import json

# Charger les descriptions des phases et les mantras
def load_phase_descriptions(file_path='docs/phase_descriptions.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_mantras(file_path='docs/mantras_list.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Obtenir le mantra pour la phase donnée
def get_mantra(phase, date, mantras):
    month = date.strftime('%B')
    day = date.day
    index = 0 if day <= 10 else 1 if day <= 20 else 2
    
    try:
        mantra = mantras[phase][month][index]
        return mantra.split(': ', 1)[1]  # Retourne seulement la partie après ": "
    except (KeyError, IndexError):
        return f"Mantra not available for {phase} phase, {month}, index {index}."

# Calculer le cycle menstruel
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

# Générer la description de chaque phase
def generate_phase_description(phase_name, phase_info, mantra):
    # Initialisation de la description avec le mantra
    description = f"\n{' ' * 35}{phase_info['description']['phase_info']['text']}\n\n"
    description += f"✨ {mantra} ✨\n\n"
    

    # Recommandations sportives
    description += "\n🏋️‍♀️ Sports recommendations:\n"
    for sport in phase_info['description']['sports_recommendations']:
        description += f"• {sport['text'] if isinstance(sport, dict) else sport}\n"

    # Recommandations nutritionnelles
    description += "\n🍽️ Nutrition recommendations:\n"
    for food in phase_info['description']['nutrition']['recommended_foods']:
        description += f"• {food['text'] if isinstance(food, dict) else food}\n"
    
    # Aliments à éviter
    description += "\n🚫🍟 Foods to avoid:\n"
    for food in phase_info['description']['nutrition']['foods_to_avoid']:
        description += f"• {food['text'] if isinstance(food, dict) else food}\n"

    # Vitamines et suppléments
    description += "\n💊 Vitamins & Supplements:\n"
    for vitamin in phase_info['description']['vitamins_supplements']:
        description += f"• {vitamin['text'] if isinstance(vitamin, dict) else vitamin}\n"

    # Seed cycling
    seed_cycling = phase_info['description'].get('seed_cycling', None)
    if seed_cycling:
        description += "\n🌻 Seed Cycling:\n"
        description += f"Include {', '.join(seed_cycling['seeds'])}\n"
        description += f"Benefits: {seed_cycling['benefits']}\n"

    # Astuces de soins personnels
    description += "\n🧘‍♀️ Self-Care Tips:\n"
    for tip in phase_info['description']['self_care_tips']:
        description += f"• {tip['text'] if isinstance(tip, dict) else tip}\n"
    
    return description


# Créer un événement pour un calendrier donné
def create_event(phase_name, start, end, phase_info, mantras, format='ical'):
    mantra = get_mantra(phase_name, start, mantras)
    description = generate_phase_description(phase_name, phase_info, mantra)
    
    if format == 'ical':
        event = Event()
        event.add('summary', phase_info['title'])
        event.add('dtstart', start.date())
        event.add('dtend', end.date())
        event.add('description', description)
        return event
    elif format == 'csv':
        return [
            phase_info['title'],
            start.strftime("%m/%d/%Y"),
            end.strftime("%m/%d/%Y"),
            "True",
            description
        ]

# Créer un calendrier au format iCal
def create_ical(phases, user_info, phase_descriptions, mantras):
    cal = Calendar()
    for phase_name, start, end in phases:
        phase_info = phase_descriptions[phase_name]
        event = create_event(phase_name, start, end, phase_info, mantras, format='ical')
        cal.add_component(event)
    return cal.to_ical()

# Créer un calendrier Google (CSV)
def create_google_calendar(phases, user_info, phase_descriptions, mantras):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Subject", "Start Date", "End Date", "All Day Event", "Description"])
    for phase_name, start, end in phases:
        phase_info = phase_descriptions[phase_name]
        writer.writerow(create_event(phase_name, start, end, phase_info, mantras, format='csv'))
    return output.getvalue().encode('utf-8')

# Créer un calendrier Outlook (CSV similaire à Google)
def create_outlook_calendar(phases, user_info, phase_descriptions, mantras):
    return create_google_calendar(phases, user_info, phase_descriptions, mantras)

# Créer un calendrier Apple (équivalent à iCal)
def create_apple_calendar(phases, user_info, phase_descriptions, mantras):
    return create_ical(phases, user_info, phase_descriptions, mantras)

