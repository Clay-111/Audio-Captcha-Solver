########### EVALUATION ###########


import pandas as pd
from Levenshtein import distance

# Load the CSV files
ocr_df = pd.read_csv("transformed_image_to_text.csv")  # Image file (OCR output)
audio_df = pd.read_csv("transcriptions_transformed.csv")  # Audio file (transcription)

# Remove extensions to match filenames 
ocr_df["file"] = ocr_df["file"].str.replace(r"\.png$", "", regex=True)
audio_df["file"] = audio_df["file"].str.replace(r"\.wav$", "", regex=True)

# Merge both DataFrames on the "file" column
merged_df = pd.merge(ocr_df, audio_df, on="file", how="inner")

# Function to calculate exact match accuracy
def exact_match(row):
    return 1 if row["text_x"] == row["text_y"] else 0

# Function to calculate Levenshtein distance (with error handling)
def levenshtein_distance(row):
    text1 = str(row["text_x"]) if pd.notna(row["text_x"]) else ""
    text2 = str(row["text_y"]) if pd.notna(row["text_y"]) else ""
    return distance(text1, text2)

# Function to calculate Character Error Rate (CER)
def cer(row):
    ref_text = str(row["text_y"])
    if len(ref_text) == 0:
        return 1 if len(row["text_x"]) == 0 else 0  # Handle empty references
    return levenshtein_distance(row) / len(ref_text)

# Apply the metrics
merged_df["exact_match"] = merged_df.apply(exact_match, axis=1)
merged_df["levenshtein_distance"] = merged_df.apply(levenshtein_distance, axis=1)
merged_df["error_rate"] = merged_df.apply(cer, axis=1)

# Organizing the columns
merged_df = merged_df[["file", "text_x", "text_y", "exact_match", "levenshtein_distance", "error_rate"]]

# Rename columns
merged_df.columns = ["file", "transformed_image_to_text", "transcriptions_transformed", "exact_match", "levenshtein_distance", "error_rate"]

# Compute overall metrics
exact_match_accuracy = merged_df["exact_match"].mean() * 100
avg_levenshtein_distance = merged_df["levenshtein_distance"].mean()
avg_error_rate = merged_df["error_rate"].mean()

# Save to CSV
merged_df.to_csv("accuracy_comparison.csv", index=False)


print(f"Accuracy comparison saved to accuracy_comparison.csv")
print(f"Exact Match Accuracy: {exact_match_accuracy:.2f}%")
print(f"Average Levenshtein Distance: {avg_levenshtein_distance:.2f}")
print(f"Average Error Rate (CER): {avg_error_rate:.4f}")
