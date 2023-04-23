# Offline Support with jonatasgrosman/wav2vec2-large-xlsr-53-english

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datasets import load_dataset
import torch
import soundfile as sf
import librosa


""" speech recognition model """
MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
r_processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
r_model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)


def recognize(filepath="output.wav"):
  # speech recognition
  speech_array, sampling_rate = librosa.load(filepath, sr=16_000)
  print(speech_array)
  print(sampling_rate)

  inputs = r_processor([speech_array], sampling_rate=16_000, return_tensors="pt", padding=True)

  with torch.no_grad():
      logits = r_model(inputs.input_values, attention_mask=inputs.attention_mask).logits

  predicted_ids = torch.argmax(logits, dim=-1)
  predicted_sentences = r_processor.batch_decode(predicted_ids)
  
  return predicted_sentences[0]

if __name__ == "__main__":
  print(recognize())