def retrieve_notes(tone: str):    
    note = tone[:-6] if tone.endswith(' Major') or tone.endswith(' Minor') else tone[:-7]
    quality = tone[-6:] if tone.endswith(' Major') else tone[-6:] if tone.endswith(' Minor') else ''
    
    return note, quality

def get_scale(tone: str):
    notes_with_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note, quality = retrieve_notes(tone)
    
    if quality not in [' Major', ' Minor']:
        return "Invalid scale type. Please use 'Major' or 'Minor'."
    
    start_index = notes_with_sharps.index(note)
    
    if quality.strip() == 'Major':
        scale_pattern = [0, 2, 4, 5, 7, 9, 11]
    else:  
        scale_pattern = [0, 2, 3, 5, 7, 8, 10]
    
    scale = [notes_with_sharps[(start_index + interval) % 12] for interval in scale_pattern]
    
    return scale