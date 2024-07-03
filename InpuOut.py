import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC_ph").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
# wav = tts.tts(text="Hello world!", speaker_wav='./input.wav', language="en")
# Text to speech to a file
tts.tts_to_file(text="Greetings, Hirthik Balaji!, It's a pleasure to meet you in this lively space.🌿 So, what's your story today? Are you ready to take on the world? 🤔", file_path="output.wav")
