import sys
from collections import deque
from threading import Thread
from time import sleep
from numpy import inf
import pyaudio
import wave

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recorder import record
from recognizer import recognize
from generator import generate
from player import get_stream, play_wave_file

# constants    
STOP_DURATION = 2
REFRESH_RATE = 0.15
user_input_wav_filepath = 'user.wav'
response_wav_filepath   = 'chatgpt.wav'
dummy_wav_filepath     = 'dummy.wav'

def send_chatgpt(text):
  global chatgpt_driver
  text_area = chatgpt_driver.find_element(By.TAG_NAME, "textarea")
  text_area.send_keys(text + " Please keep your response shorter." + Keys.ENTER)

def initialize_chat_stream():
  global chat_stream
  generate("this is a dummy message.", dummy_wav_filepath)
  with wave.open(dummy_wav_filepath, "rb") as wf:
    chat_stream = get_stream(wf)

def destroy_chat_stream():
  global chat_stream
  chat_stream.stop_stream()
  sleep(3)
  chat_stream.close()

def text_reader_run():
  global reader_waitlist, reader_continue, reader_complete, chat_stream
  reader_complete = False
  while reader_continue or len(reader_waitlist):
    if len(reader_waitlist):
      generate(reader_waitlist.popleft(), response_wav_filepath)
      play_wave_file(chat_stream, response_wav_filepath)
    sleep(REFRESH_RATE)
  reader_complete = True


def main():
  global chatgpt_driver, reader_continue, reader_complete, reader_waitlist

  print()
  print("**************************")
  print("** English Conversation **")
  print("**************************")
  print()

  print("- Now Loading...")
  chatgpt_driver = uc.Chrome()
  chatgpt_driver.get("https://chat.openai.com")

  initialize_chat_stream()

  print("- Please sign in to ChatGPT. ")  
  sleep(5)

  input("- Enter when the ChatGPT page is ready. [Enter]:")
  sleep(1)

  input_visible    = True
  response_visible = False

  i = input("* Do you want to display what you speak? [Y/n]:")
  input_visible = (i in ["Y", "y", "yes", ""])

  i = input("* Do you want to display the responses from ChatGPT? [Y/n]:")
  response_visible = (i in ["Y", "y", "yes", ""])

  # sleep(1)

  print()
  print("*******************")
  print("*** INSTRUCTION ***")
  print("*******************")
  print("- Speak anyway you want, OR you can start with this phrase:")
  print('"I recently started learning English. Please give me an easy question for practice."')
  print()

  sleep(2)

  exit_flg = False
  while True:
    """ Record and Recognize Audio """
    while True:
      if input("- Start recording [Enter]:") == 'exit': 
        exit_flg = True
        break

      sleep(0.2)

      print("🎤 Recording...")
      sleep(0.4)

      print("- Stop recording [Enter]:", end="")
      record(user_input_wav_filepath)
      try:
          text = recognize(user_input_wav_filepath)
          if len(text) <= 1: raise Error()
      except:
          print()
          print("- Sorry, but not recognized. Please retry.")
          continue
      break
    
    if exit_flg: break

    if input_visible: 
      print()
      print("User:", text)


    """ Send Text """
    send_chatgpt(text)
    sleep(0.5)

    """ Receive Text and send to Reader """
    if response_visible: 
      print()
      print("ChatGPT: ", end="", flush=True)

    # start text reader thread
    reader_waitlist = deque()
    reader_continue = True
    Thread(target=text_reader_run).start()

    # snapshot for checking if start to receive the latest response 
    snapshot = chatgpt_driver.find_elements(By.CLASS_NAME, "group")[-1].text
    while True: 
      sleep(REFRESH_RATE)
      latest = chatgpt_driver.find_elements(By.CLASS_NAME, "group")[-1].text
      if snapshot != latest: break

    # make the first part of the response
    text = latest 
    if response_visible: print(text, end="", flush=True)

    # receive the remainder part
    cnt = 0
    read_text = ""
    while True:
      sleep(REFRESH_RATE)
      latest = chatgpt_driver.find_elements(By.CLASS_NAME, "group")[-1].text

      # stop receiving if no more response
      if text == latest: 
        cnt += 1
      else:
        cnt = 0
      if cnt > STOP_DURATION / REFRESH_RATE:
        reader_continue = False
        break

      # flush unflushed text
      if response_visible: 
        print(latest[len(text):], end="", flush=True)

      # check if there is completed unread text to send to reader
      unread_text = latest[len(read_text):]
      
      i = inf
      for stopper in [".", "!", "?"]:
        j = unread_text.find(stopper)
        if j != -1: 
          i = min(i, j)

      if i < inf:
        t = unread_text[:i+1]
        reader_waitlist.append(t)
        read_text += t

      # update text to the latest
      text = latest

    while not reader_complete:
      sleep(REFRESH_RATE)

    if response_visible: print()
    print()

  destroy_chat_stream()
  chatgpt_driver.close()


if __name__ == "__main__":
  main()