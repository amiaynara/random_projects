import re
import os


# Constants
subject_normalization = {
    # Politics/Polity related
    'POL': 'Polity',
    'Pol': 'Polity',
    'Polity': 'Polity',
    'GOV.': 'Governance',
    'Gov.': 'Governance',
    'Governance': 'Governance',
    
    # Economics related
    'ECO': 'Economics',
    'Eco': 'Economics',
    'Economics': 'Economics',
    'Economics(': 'Economics',
    'Economics_AK': 'Economics',
    'Economics_PG': 'Economics',
    
    # Environment related
    'ENV': 'Environment',
    'Env': 'Environment',
    'Environment': 'Environment',
    
    # Ethics related
    'ETHICS': 'Ethics',
    'Ethics': 'Ethics',
    'Ethics_JG': 'Ethics',
    
    # Geography related
    'GEOG': 'Geography',
    'Geog': 'Geography',
    'Geography': 'Geography',
    
    # History related
    'HIST': 'History',
    'Hist': 'History',
    'Ancient': 'History',
    'Modern': 'History',
    'World': 'History',
    
    # International relations
    'I.R.': 'International_Relations',
    'International': 'International_Relations',
    
    # Science and Technology
    'S&T': 'Science_&_Technology',
    'S.I.': 'Science_&_Technology',
    'Science': 'Science_&_Technology',
    'Physics': 'Science_&_Technology',
    
    # Miscellaneous
    'D.M.': 'Disaster_Management',
    'Disaster': 'Disaster_Management',
    'P.I.': 'Public_Administration',
    'I.S.': 'Internal_Security',
    'Security': 'Internal_Security',
    'Society': 'Society',
    'Art': 'Art_&_Culture',
    'Biology': 'Science_&_Technology',
    'How': 'How_to_Prepare',
    'Introduction': 'Introduction',
    'Language': 'Language',
    'Map': 'Map',
    'Post': 'Post-Independence',
    'Recorded': 'Recorded_Session',
    'Answer': 'Answer_Writing'
}

def normalize_subject(subject):
    return subject_normalization.get(subject, subject)  # Returns original if not found

def get_subject_name(string):
    match = re.search(r'\d+\.\s+([^\s-]+)', string)
    if match:
        return match.group(1)

def get_subjects(data):
    # Extract subjects using regular expression
    subjects = set()
    for line in data.split('\n'):
        # Match the first word after the number and dot, before space or hyphen
        subject = get_subject_name(line)
        if subject:
            subjects.add(subject)
    return subjects

if __name__ == '__main__':
    print("Unique subjects:")
    with open('file_names.tsv', 'r') as f:
        data = f.read()
    subjects = get_subjects(data)
    normalized_subjects = [normalize_subject(subject) for subject in subjects]
    for subject in sorted(subjects):
        # Create normalize_subject directory if it doesn't exist
        normalize_dir = os.path.join('telegram_media', normalize_subject(subject))
        if not os.path.exists(normalize_dir):
            os.makedirs(normalize_dir)

