############ FIND COMMON FILES ############

import os
import csv

# Get folder paths
audio_folder = "./0. Datasets/audioCaptcha/captchas/audio"
image_folder = "./0. Datasets/audioCaptcha/captchas/images"

# Get filenames without extensions
audio_files = {os.path.splitext(f)[0] for f in os.listdir(audio_folder) if f.endswith(".wav")}
image_files = {os.path.splitext(f)[0] for f in os.listdir(image_folder) if f.endswith(".png")}

# Find common files
common_files = sorted(audio_files.intersection(image_files))

# Save to CSV
csv_filename = "common_files.csv"
with open(csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename"]) 
    for file in common_files:
        writer.writerow([file])

print(f"Saved {len(common_files)} common filenames to {csv_filename}")

import pandas as pd

# Replace this with the actual file path
df = pd.read_csv("./common_files.csv")

# Print the entire DataFrame
print(df.head())

