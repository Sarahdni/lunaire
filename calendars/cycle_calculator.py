
def generate_recommendations(category, recommendations):
    description = f"\n{category}:\n"
    for item in recommendations:
        description += f"• {item['text'] if isinstance(item, dict) else item}\n"
    return description

from datetime import datetime, timedelta

def calculate_cycle(start_date, cycle_length, period_length, num_months=12):
    if isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'")
    
    all_phases = []
    current_date = start_date
    for _ in range(num_months):
        cycle_end = current_date + timedelta(days=cycle_length)
        phases = [
            ("Menstrual", current_date, current_date + timedelta(days=period_length)),
            ("Follicular", current_date + timedelta(days=period_length), current_date + timedelta(days=cycle_length // 2 - 2)),
            ("Ovulatory", current_date + timedelta(days=cycle_length // 2 - 2), current_date + timedelta(days=cycle_length // 2 + 2)),
            ("Luteal", current_date + timedelta(days=cycle_length // 2 + 2), cycle_end)
        ]
        all_phases.extend(phases)
        current_date = cycle_end
    return all_phases
