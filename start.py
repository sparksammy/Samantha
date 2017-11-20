#Written by Alex I. Ramirez @alexram1313
#arcompware.com
import re
import wave
import pyaudio
import _thread
import time
import sys, glob
import aiml
import os

kernel = aiml.Kernel()
for file in glob.glob('ai/*.aiml'):
	kernel.learn(file)

kernel.respond("LOAD AIML B")

class TextToSpeech:
    
    CHUNK = 1024

    def __init__(self, words_pron_dict:str = 'cmudict-0.7b.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict:str):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ',2)
                    self._l[key] = re.findall(r"[A-Z]+",val)

    def get_pronunciation(self, str_input):
        list_pron = []
        for word in re.findall(r"[\w']+",str_input.upper()):
            if word in self._l:
                list_pron += self._l[word]
        print(list_pron)
        delay=0
        for pron in list_pron:
            _thread.start_new_thread( TextToSpeech._play_audio, (pron,delay,))
            delay += 0.145
    
    def _play_audio(sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("sounds/"+sound+".wav", 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            
            data = wf.readframes(TextToSpeech.CHUNK)
            
            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)
        
            stream.stop_stream()
            stream.close()

            p.terminate()
            return
        except:
            pass
    
 
 

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        question = input("S> ")
        if "open paint" in question: 
            output = "Opening paint..."
            os.system('mspaint')
            print(output)
            response = tts.get_pronunciation(output)
        elif "open notepad" in question: 
            output = "Opening notepad..."
            os.system('notepad')
            print(output)
            response = tts.get_pronunciation(output)
        elif "open command prompt" in question: 
            output = "Opening command prompt..."
            os.system('cmd')
            print(output)
            response = tts.get_pronunciation(output)
        elif "open firefox" in question: 
            output = "Opening Fire fox..."
            os.system('firefox.exe')
            print(output)
            response = tts.get_pronunciation(output)
        elif "who are you" in question: 
            output = "I am a girlfriend of Sparksammy's Spark Sammy, and my name is Samantha. However, we can be greats friends!"
            print(output)
            response = tts.get_pronunciation(output)
        elif "be your girlfriend" in question: 
            output = "Sorry, but I am already taken"
            print(output)
            response = tts.get_pronunciation(output)
        else:
            output = kernel.respond(question)
            print(output)
            response = tts.get_pronunciation(output)
        continue
		
        print(output)
        response = tts.get_pronunciation(output)
        time.sleep(4.2)
        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X
