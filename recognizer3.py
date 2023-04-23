from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import librosa

# load model and processor
model_name = "openai/whisper-small"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="transcribe")
# model.config.forced_decoder_ids = None

def recognize(filepath="output.wav"):
  speech_array, sampling_rate = librosa.load(filepath, sr=16_000)

  input_features = processor(speech_array, sampling_rate=sampling_rate, return_tensors="pt").input_features 

  # generate token ids
  predicted_ids = model.generate(input_features, max_new_tokens=448)
  # decode token ids to text
  # transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)

  transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

  return transcription[0]

if __name__ == "__main__":
  print(recognize())