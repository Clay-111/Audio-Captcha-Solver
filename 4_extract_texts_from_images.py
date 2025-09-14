############ IMAGE EXTRACTION ############


import easyocr
import os
import csv
import pandas as pd
import cv2

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Get Image dataset path
image_folder = "./0. Datasets/audioCaptcha/captchas/images"

# Load common files (without extensions)
common_files = pd.read_csv("common_files.csv")["Filename"].astype(str).tolist()
common_files_set = {f + ".png" for f in common_files} 

# Get list of common image files
image_files = sorted([f for f in os.listdir(image_folder) if f in common_files_set])

# Output CSV file
csv_file = "image_to_text.csv"

# Function for Preprocessing
def preprocess_image(image_path):
    img = cv2.imread(image_path)  # Load image in color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    
    # Resize image 
    img = cv2.resize(img, (250, 100))
    return img

# Process images and save results
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["file", "text"]) 

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        
        # Preprocess image
        processed_img = preprocess_image(image_path)

        # Run OCR on the processed image
        result = reader.readtext(processed_img)

        # Join extracted text
        extracted_text = " ".join([detection[1] for detection in result])
        
        # Save to CSV
        writer.writerow([image_file, extracted_text])

print(f"Extraction complete. Results saved in {csv_file}")

