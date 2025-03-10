# Audio Captcha Solver

This file contains the main workflow for processing and evaluating audio CAPTCHA data. 
The program includes steps for finding common files between audio and image datasets, extracting text from images, transcribing audio files, and comparing the accuracy of the transcriptions.

## Workflow

1. **Finding Common Files**
   - Identify common files between the audio and image datasets.
   - Save the list of common files to `common_files.csv`.

2. **Extracting Text from Images**
   - Use EasyOCR to extract text from images.
   - Save the extracted text to `image_to_text.csv`.

3. **Transcribing Audio Files**
   - Use the Whisper model to transcribe audio files.
   - Save the transcriptions to `transcriptions.csv`.

4. **Transforming Extracted and Transcribed Texts**
   - Apply transformations to the extracted and transcribed texts.
   - Save the transformed texts to `transcriptions_transformed.csv` and `transformed_image_to_text.csv`.

5. **Comparing Accuracy**
   - Compare the extracted and transcribed texts to calculate accuracy metrics.
   - Save the accuracy comparison results to `accuracy_comparison.csv`.
  
For more details, refer to the [README.pdf](README.pdf) and [Explanation Video.mp4](Explanation%20Video.mp4).

## Dependencies

Ensure you have the following dependencies installed:

```sh
pip install pandas easyocr whisper pydub torchaudio


