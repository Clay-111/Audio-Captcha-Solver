############ CONVERT DECODED AUDIO TEXTS ############


import pandas as pd
import re

# Load CSV
df = pd.read_csv("transcriptions.csv")

# Mapping for number words to digits
number_map = {
    "for": "4", "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}

# Function to preprocess and transform transcription text
def transform_transcription(text):
    if not isinstance(text, str):  
        return ""  # Handle NaN values

    # Preserve spaces and Normalize for uniform processing
    text = text.lower()
    
    # Convert 'capital letters 'X'' to 'X' (uppercase)
    text = re.sub(r'\bcapital (\w)', lambda m: m.group(1).upper(), text)

    # Convert 'small letters 'X'' to 'x' (lowercase)
    text = re.sub(r'\bsmall (\w)', lambda m: m.group(1).lower(), text)

    # Replace number words with digits
    for word, digit in number_map.items():
        text = re.sub(fr'\b{word}\b', digit, text)

    # Remove spaces, commas, and periods
    text = re.sub(r"[ ,\.]", "", text)

    return text

# Apply transformation
df["text"] = df["text"].astype(str).apply(transform_transcription)

# Save to CSV
df.to_csv("transcriptions_transformed.csv", index=False)
print("Transformed CSV saved as transcriptions_transformed.csv")
