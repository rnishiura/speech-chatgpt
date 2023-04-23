import pyaudio  
import wave  
import time

#define stream chunk   
chunk = 1024  

def get_stream(wave_file):
  p = pyaudio.PyAudio() 
  #open stream  
  stream = p.open(format = p.get_format_from_width(wave_file.getsampwidth()),  
                  channels = wave_file.getnchannels(),  
                  rate = wave_file.getframerate(),  
                  output = True)  
  return stream

def play_wave_file(stream, filepath='output.wav'):
  #open a wav format music  
  with wave.open(filepath, "rb") as wf:
    #read data  
    data = wf.readframes(chunk)  
    #play stream  
    while data:  
        stream.write(data)  
        data = wf.readframes(chunk)  


def play(filepath='output.wav'):
  with wave.open(filepath, "rb") as wf:
    stream = get_stream(wf)
  play_wave_file(stream, filepath)
  stream.stop_stream()
  stream.close()

if __name__ == "__main__":
  play()