import re
import os
from typing import Set, Dict, Optional, List

# Enhanced subject normalization
SUBJECT_NORMALIZATION: Dict[str, str] = {
    # Standard subjects
    'Additional': 'Additional_Science',
    'Ancient': 'History',
    'Ancient_and_Medieval_History': 'History',
    'Answer': 'Answer_Writing',
    'Art': 'Art_&_Culture',
    'Biology': 'Science_&_Technology',
    'Disaster': 'Disaster_Management',
    'Economics': 'Economics',
    'Environment': 'Environment',
    'Essay': 'Essay',
    'Ethics': 'Ethics',
    'Geography': 'Geography',
    'Governance': 'Governance',
    'How': 'How_to_Read_Newspaper',
    'International': 'International_Relations',
    'Interview': 'Interview',
    'Introduction': 'Introduction',
    'Medieval': 'History',
    'Modern': 'Modern_History',
    'New': 'New',
    'Polity': 'Polity',
    'Post': 'Post-Independence',
    'Recorded': 'Recorded_Session',
    'Recorded_Ancient_and_Medieval_History': 'History',
    'Science': 'Science_&_Technology',
    'Security': 'Internal_Security',
    'Social': 'Social_Issues',
    'Society': 'Society',
    'Topper': 'Toppers_Talk',
    'Toppers': 'Toppers_Talk',
    'World': 'World_History',
    
    # Special cases and variants
    'Topper\'s_Talk': 'Toppers_Talk',
    'Topper\'s': 'Toppers_Talk',
    'Ancient_and_Medieval': 'History',
    'Medieval_History': 'History',
    'Modern_History': 'Modern_History',
    'World_History': 'World_History',
    'Internal_Security': 'Internal_Security',
    'Social_Justice': 'Social_Issues',
    'Science_Technology': 'Science_&_Technology',
    'S&T': 'Science_&_Technology'
}

def normalize_subject(subject: str) -> str:
    """Normalize subject name with intelligent fallback."""
    # First try exact match
    if subject in SUBJECT_NORMALIZATION:
        return SUBJECT_NORMALIZATION[subject]
    
    # Then try partial matches
    for key, value in SUBJECT_NORMALIZATION.items():
        if subject.startswith(key):
            return value
    
    # Finally, clean up any remaining special cases
    if 'Ancient_and_Medieval_History' in subject:
        return 'History'
    if 'Topper' in subject:
        return 'Toppers_Talk'
    
    return subject

def extract_subject_from_filename(filename: str) -> Optional[str]:
    """
    Extract the subject name from filename with multiple pattern support.
    Handles these formats:
    1. 001. Subject Name Class 01...
    2. 001_Subject_Name_Class_01...
    3. Subject_Name_With_Class...
    4. Topper's_Talk...
    5. 001) Subject Name Class 01...
    """
    # Pattern 1: Number followed by dot and space
    match = re.search(r'^\d+\.\s+([A-Za-z]+)', filename)
    if match:
        return match.group(1)
    
    # Pattern 5: Number followed by parenthesis and space
    match = re.search(r'^\d+\)\s+([A-Za-z]+)', filename)
    if match:
        return match.group(1)
    
    # Pattern 2: Number followed by underscore
    match = re.search(r'^\d+_([A-Za-z_]+)_Class', filename)
    if match:
        return match.group(1)
    
    # Pattern 3: Starts with subject name
    match = re.search(r'^([A-Za-z_]+)_Class', filename)
    if match:
        return match.group(1)
    
    # Pattern 4: Topper's Talk
    if filename.startswith("Topper"):
        return "Topper's_Talk"
    
    return None

def get_unique_subjects(file_content: str) -> List[str]:
    """Extract and normalize all unique subjects from filenames."""
    subjects = set()
    for line in file_content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        subject = extract_subject_from_filename(line)
        if subject:
            subjects.add(subject)
    
    return sorted(subjects)

def create_subject_directories(subjects: List[str], base_dir: str = 'telegram_media') -> None:
    """Create directories for normalized subjects."""
    for subject in subjects:
        normalized = normalize_subject(subject)
        subject_dir = os.path.join(base_dir, normalized)
        os.makedirs(subject_dir, exist_ok=True)
        print(f"Created directory: {subject_dir}")

def main():
    """Main processing function."""
    input_file = 'file_names.tsv'
    
    try:
        with open(input_file, 'r') as f:
            file_content = f.read()
        
        subjects = get_unique_subjects(file_content)
        
        print("\nExtracted and normalized subjects:")
        for subject in subjects:
            print(f"- {subject} → {normalize_subject(subject)}")
        
        create_subject_directories(subjects)
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()