from datetime import time

# Medication configuration based on your mother's prescription
MEDICATIONS = {
    'cervitam': {
        'name': 'Cervitam',
        'times': [time(9, 0), time(21, 0)],  # 9 AM and 9 PM
        'instructions': 'Twice per day - morning and night'
    },
    'tebonina_forte': {
        'name': 'Tebonina Forte',
        'times': [time(9, 0), time(21, 0)],  # 9 AM and 9 PM
        'instructions': 'Twice per day - morning and night'
    },
    'symbicort': {
        'name': 'Symbicort Inhaler',
        'times': [time(8, 0), time(20, 0)],  # 8 AM and 8 PM
        'instructions': 'Inhaler - twice per day, morning and night'
    },
    'fast_freeze_gel': {
        'name': 'Fast Freeze Gel',
        'times': [time(12, 0)],  # 12 PM (noon)
        'instructions': 'Apply as needed (same as before)'
    },
    'movxir': {
        'name': 'Movxir',
        'times': [time(13, 0)],  # 1 PM
        'instructions': 'Same as before'
    },
    'potassium_drink': {
        'name': 'Potassium Drink',
        'times': [time(10, 0)],  # 10 AM
        'instructions': 'Same as before'
    },
    'milga_advance': {
        'name': 'Milga Advance',
        'times': [time(9, 0)],  # 9 AM
        'instructions': 'For diabetes support'
    },
    'januvia': {
        'name': 'Januvia',
        'times': [time(14, 0)],  # 2 PM (after lunch)
        'instructions': 'After lunch - diabetes medication'
    },
    'lipostat': {
        'name': 'Lipostat',
        'times': [time(22, 0)],  # 10 PM
        'instructions': 'Once per night before bed'
    },
    'controloc': {
        'name': 'Controloc',
        'times': [time(8, 0)],  # 8 AM
        'instructions': 'Once per morning before breakfast'
    },
    'dermovate_cream': {
        'name': 'Dermovate Cream',
        'times': [time(11, 0), time(23, 0)],  # 11 AM and 11 PM
        'instructions': 'Apply twice daily for 10 days only'
    },
    'sandocal_vitamin_d': {
        'name': 'Sandocal Vitamin D',
        'times': [time(8, 30)],  # 8:30 AM
        'instructions': 'Once per morning with breakfast'
    },
    'magnesium': {
        'name': 'Magnesium',
        'times': [time(9, 30)],  # 9:30 AM
        'instructions': 'Once per morning'
    }
}

# Time-based grouping for better organization
MORNING_MEDS = ['controloc', 'sandocal_vitamin_d', 'symbicort', 'cervitam', 'milga_advance', 'tebonina_forte', 'magnesium', 'potassium_drink']
AFTERNOON_MEDS = ['dermovate_cream', 'fast_freeze_gel', 'movxir', 'januvia']
EVENING_MEDS = ['symbicort', 'cervitam', 'tebonina_forte', 'lipostat', 'dermovate_cream']

# Medication categories
CATEGORIES = {
    'diabetes': ['milga_advance', 'januvia'],
    'respiratory': ['symbicort'],
    'topical': ['fast_freeze_gel', 'dermovate_cream'],
    'supplements': ['sandocal_vitamin_d', 'magnesium', 'potassium_drink'],
    'circulation': ['tebonina_forte'],
    'neurological': ['cervitam'],
    'gastrointestinal': ['controloc'],
    'cholesterol': ['lipostat'],
    'other': ['movxir']
}