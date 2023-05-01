# Speech ChatGPT

_An easy-to-use secure app for quality low-latency conversations in English speech with ChatGPT._

## Requirements

```
git clone https://github.com/rnishiura/speech-chatgpt.git
cd speech-chatgpt
pip install -r requirements.txt
```

- Your computer also has to have [Google Chrome](https://www.google.com/chrome/) installed as its automated testing is used to manage ChatGPT service.
- This app auto detects CUDA for faster speech recognition and generation. Please follow https://pytorch.org to install `torch` and `torchaudio` with CUDA support. Note that `pip install -r requirements.txt` may install PyTorch without CUDA.

## How to run

```
python app.py
```

## Usage

Run `app.py` and further instruction is provided. You don't need to give any credentials to this app. Just login to the ChatGPT service.

## Models

### Speech Recognition Model

- [openai/whisper-small](https://huggingface.co/openai/whisper-small)

### Speech Generation Model

- [microsoft/speecht5_tts](https://huggingface.co/microsoft/speecht5_tts)
