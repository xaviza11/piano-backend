def is_valid_tone(tone: str) -> bool:
    valid_tones = [
        "C Major", "C# Major", "D Major", "D# Major", "E Major", "F Major", "F# Major", "G Major", "G# Major", "A Major", "A# Major", "B Major",
        "C Minor", "C# Minor", "D Minor", "D# Minor", "E Minor", "Fm", "F# Minor", "G Minor", "G# Minor", "A Minor", "A# Minor", "B Minor"
    ]
    return tone in valid_tones
