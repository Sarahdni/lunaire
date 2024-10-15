from datetime import datetime, timedelta

def generate_recommendations(category, recommendations):
    description = f"\n{category}:\n"
    for item in recommendations:
        description += f"• {item['text'] if isinstance(item, dict) else item}\n"
    return description