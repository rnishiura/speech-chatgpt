# Speech ChatGPT
*Easy-to-use app for quality low-latency conversations in English speech with ChatGPT.*

## Requirements
```
git clone https://github.com/rnishiura/speech-chatgpt.git
cd speech-chatgpt
pip install -r requirements.txt
```

Your computer also has to have Google Chrome installed due to the app using its automated testing function to manage ChatGPT.

## How to run
```
python main.py
```

## Usage
Follow the instructions provided in the program.

## Models

### Speech Recognition Model
* [jonatasgrosman/wav2vec2-large-xlsr-53-english](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english)
* [openai/whisper-small](https://huggingface.co/openai/whisper-small)

### Speech Generation Model
* [microsoft/speecht5_tts](https://huggingface.co/microsoft/speecht5_tts)

