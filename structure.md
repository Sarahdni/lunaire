project_root/
│
├── main.py
├── config.py
├── __init__.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── quiz_config.json
│   └── language_manager.py
│
├── email/
│   ├── __init__.py
│   ├── email_receiver.py
│   └── email_sender.py
│
├── calendars/
│   ├── __init__.py
│   ├── cycle_calculator.py     """gère le calcul des phases du cycle menstruel."""
│   ├── recommendations.py      """s'occupe de la génération de recommandations formatées."""
│   ├── ical_generator.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── user_manager.py
│   ├── cycle_manager.py
│   └── calendar_manager.py
│
├── locales/
│   ├── en/
│   │   ├── mantras.json
│   │   └── phase_descriptions.json
│   ├── fr/
│   │   ├── mantras.json
│   │   └── phase_descriptions.json
│   ├── es/
│   │   ├── mantras.json
│   │   └── phase_descriptions.json
│   ├── de/
│   │   ├── mantras.json
│   │   └── phase_descriptions.json
│   ├── nl/
│   │   ├── mantras.json
│   │   └── phase_descriptions.json
│   └── it/
│       ├── mantras.json
│       └── phase_descriptions.json
│
└── docs/
    