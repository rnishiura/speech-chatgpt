from transformers import pipeline
import librosa
import torch

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

# load model and processor
model_name = "openai/whisper-small"
pipe = pipeline(
  "automatic-speech-recognition",
  model=model_name,
  chunk_length_s=30,
  device=device,
  max_new_tokens=448,
)

def recognize(filepath="output.wav"):
  speech_array, sampling_rate = librosa.load(filepath, sr=16_000)
  prediction = pipe(speech_array)["text"]
  return prediction
  # we can also return timestamps for the predictions
  # prediction = pipe(speech_array, return_timestamps=True)["chunks"]
  # print(prediction)

if __name__ == "__main__":
  print("recognizing...")
  print(recognize())