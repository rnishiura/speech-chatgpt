# Following pip packages need to be installed:
# !pip install git+https://github.com/huggingface/transformers sentencepiece datasets

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datasets import load_dataset
import torch
import soundfile as sf
import librosa
import random
import time

speaker_id = 7306
# speaker_id = 7930

# speaker_id = random.randint(0, 7931)
print("Speaker: ", speaker_id)

""" speech generation model """
s_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
s_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[speaker_id]["xvector"]).unsqueeze(0)


def generate(text, filepath='output.wav'):
  # speech generation
  inputs = s_processor(text=text, return_tensors="pt")
  speech = s_model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

  sf.write(filepath, speech.numpy(), samplerate=16000)
  # print("Speech audio saved.")

# 56 61

def audition():
  global speaker_embeddings
  from player import play
  for i in range(36, 7931):
    print(i)
    speaker_id = i
    speaker_embeddings = torch.tensor(embeddings_dataset[speaker_id]["xvector"]).unsqueeze(0)
    generate("Hello! Have a nice day!")
    play()
    # time.sleep(0.5)

if __name__ == "__main__":
  text = input()
  generate(text)

