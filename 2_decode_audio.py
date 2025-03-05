########### AUDIO DECODE ###########


import whisper
import os
import pandas as pd
from pydub import AudioSegment, silence
import torchaudio

# Load Whisper model
model = whisper.load_model("medium").to("cuda")

# Get Audio dataset path
audio_folder = "./0. Datasets/audioCaptcha/captchas/audio"  
output_file = "transcriptions.csv"

# Load common file names (without .wav extension)
common_files = pd.read_csv("common_files.csv")["Filename"].astype(str).tolist()

# Add .wav extension
common_files_set = {f + ".wav" for f in common_files}  

# List only common audio files
audio_files = sorted([f for f in os.listdir(audio_folder) if f in common_files_set])

# Store results
results = []

# Function to preprocess audio
def preprocess_audio(audio_path):
    # Load audio
    audio = AudioSegment.from_file(audio_path)
    
    # Normalization
    target_dBFS = -20  
    gain = target_dBFS - audio.dBFS
    audio = audio.apply_gain(gain if gain < 5 else 0)  
    
    # Minor Trimming silence
    non_silent_ranges = silence.detect_nonsilent(audio, min_silence_len=200, silence_thresh=-30)
    if non_silent_ranges:
        start_trim = max(0, non_silent_ranges[0][0] - 100)  # Give 100ms buffer
        end_trim = min(len(audio), non_silent_ranges[-1][1] + 100)
        audio = audio[start_trim:end_trim]
    
    # Ensure correct format for Whisper
    audio = audio.set_frame_rate(16000).set_channels(1)

    # Save temp file
    temp_path = "temp.wav"
    audio.export(temp_path, format="wav")
    return temp_path


# Process only the common audio files
for audio_file in audio_files:
    audio_path = os.path.join(audio_folder, audio_file)

    # Preprocess audio
    processed_audio_path = preprocess_audio(audio_path)

    # Transcribe with Whisper
    result = model.transcribe(processed_audio_path)
    predicted_text = result["text"].strip().lower()

    # Store result
    results.append({"file": audio_file, "text": predicted_text})

# Save to CSV
df = pd.DataFrame(results)
df.to_csv(output_file, index=False)

print(f"Transcriptions saved to {output_file}")

