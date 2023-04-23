import time
import pyaudio
from threading import Thread
import wave
import sys

""" constants """
continue_flg = True
# CHUNK = 1024
FORMAT = pyaudio.paInt16
# CHANNELS = 1 if sys.platform == 'darwin' else 2
SAMPLERATE = 16000
# mic_name = "MacBook Proのマイク"

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
    global sprec, continue_flg, wf, CHANNELS

    audio = pyaudio.PyAudio() 
    input_device_index = audio.get_default_input_device_info()['index']
    channels = audio.get_device_info_by_index(input_device_index)['maxInputChannels']

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(SAMPLERATE)

    stream = audio.open( format = FORMAT,
                        rate = SAMPLERATE,
                        channels = channels, 
                        input_device_index = input_device_index,
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
        time.sleep(0.05)
        # pass

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf.close()

if __name__ == "__main__":
  record()