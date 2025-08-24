
import os
import whisper
from pydub import AudioSegment

# Ensure ffmpeg is installed and in PATH

_model_cache = {}

def get_model(name: str = "base"):
    if name not in _model_cache:
        _model_cache[name] = whisper.load_model(name)
    return _model_cache[name]

def ensure_wav(input_path: str) -> str:
    # Whisper can take many formats, but WAV is safest
    if input_path.lower().endswith(".wav"):
        return input_path
    wav_path = input_path + ".wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_file(input_path: str, model_name: str = "base") -> str:
    model = get_model(model_name)
    wav_path = ensure_wav(input_path)
    result = model.transcribe(wav_path)
    return result.get("text", "").strip()
