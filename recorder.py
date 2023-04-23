import time
import speech_recognition
import pyaudio
from threading import Thread
import wave
import sys

""" constants """
continue_flg = True
# CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
SAMPLERATE = 16000
mic_name = "MacBook Proのマイク"

""" to stop recording """
def stop_func():
  global continue_flg
  if input():
    pass
  continue_flg = False

""" write wav file """
def callback(in_data, frame_count, time_info, status):
    global sprec, wf
    wf.writeframes(in_data)
    return (None, pyaudio.paContinue if continue_flg else pyaudio.paComplete)
    
""" record streamer """
def record(filepath='output.wav'):
    global sprec, continue_flg, wf

    audio = pyaudio.PyAudio() 

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(SAMPLERATE)

    # with wave.open('output.wav', 'wb') as wf:
    sprec = speech_recognition.Recognizer()  # インスタンスを生成
    # Audio インスタンス取得

    for x in range(0, audio.get_device_count()): 
        if audio.get_device_info_by_index(x)['name'] == mic_name:
          mic_index = audio.get_device_info_by_index(x)['index']
      
    stream = audio.open( format = pyaudio.paInt16,
                        rate = SAMPLERATE,
                        channels = CHANNELS, 
                        input_device_index = mic_index,
                        input = True, 
                        frames_per_buffer = SAMPLERATE*2, # 2秒周期でコールバック
                        stream_callback=callback)


    # stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
    stream.start_stream()
    # RECORD_SECONDS = 5
    # CHUNK = 1024
    continue_flg = True
    Thread(target=stop_func).start()

    while stream.is_active():
    # while continue_flg:
    # for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        # wf.writeframes(stream.read(CHUNK))
        time.sleep(0.1)
        # pass

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf.close()

if __name__ == "__main__":
  record()