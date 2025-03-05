########### CONVERT EXTRACTED IMAGE TEXTS ###########


import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('image_to_text.csv')

# Function to clean the text column
def clean_text(text):
    text = str(text)  # Convert to string
    return re.sub(r'[^a-zA-Z0-9]', '', text)  # Remove non-alphanumeric characters

# Apply the cleaning function to the 'text' column
df['text'] = df['text'].apply(clean_text)

# Save to a new CSV
df.to_csv('transformed_image_to_text.csv', index=False)
