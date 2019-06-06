#TTS Engine Written by Alex I. Ramirez @alexram1313
#Pretty much the rest made by Sparksammy (Samuel Lord)
import re
import wave
import pyaudio
import _thread
import time
import sys, glob
import aiml
import os
import wikipedia
import speech_recognition as sr
from roku import Roku
from lifxlan import LifxLAN

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
        # obtain audio from the microphone
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Samantha - Ready.")
                tts.get_pronunciation("I am ready for a request.")
                recogntionAudio = r.listen(source)
                question = r.recognize_google(recogntionAudio)
                print(question)
        except sr.UnknownValueError:
            print("Samantha - could not understand audio.")
            tts.get_pronunciation("Sorry, I couldn't understand you.")
            question = "wellpoowecantunderstandaudiosoyeahthatsaproblem."
        except sr.RequestError as e:
            print("Samantha - could not connect to audio recognition servers.")
            tts.get_pronunciation("Sorry, I couldn't connect to the audio recogntion service.")
            question = "wellpoowecantunderstandaudiosoyeahthatsaproblem."
        if "open gimp" in question: 
            output = "Opening gimp..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('gimp')
        elif "open mousepad" in question: 
            output = "Opening mousepad..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('mousepad')
        elif "open notepad" in question: 
            output = "Opening notepad..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('notepad')
        elif "open paint" in question: 
            output = "Opening paint..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('paint')
        elif "open command prompt" in question: 
            output = "Opening command prompt..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('cmd')
        elif "open terminal" in question: 
            output = "Opening terminal..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('xterm')
        elif "open firefox" in question: 
            output = "Opening Fire fox..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('firefox')
        elif "open chrome" in question: 
            output = "Opening chrome..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('C:\Program Files (x86)\Google\Application\chrome.exe')
        elif "open photoshop" in question: 
            output = "Opening Photo Shop..."
            print(output)
            response = tts.get_pronunciation(output)
            os.system('"C:\Program Files\Adobe\Adobe Photoshop CC 2018\Photoshop.exe"')
        elif "who are you" in question: 
            output = "I am a girlfriend of Spark Sammy, and my name is Samantha. However, we can be great friends!"
            print(output)
            response = tts.get_pronunciation(output)
        elif "be your girlfriend" in question: 
            output = "Sorry, but I am already taken"
            print(output)
            response = tts.get_pronunciation(output)
        elif "Wikipedia" in question: 
            try:
                print("Wikipedia - Ready.")
                tts.get_pronunciation("Wikipedia is ready for a request.")
                recogntionAudio = r.listen(source)
                output = wikipedia.summary(recogntionAudio);
                print(output)
                response = tts.get_pronunciation(output)
            except sr.UnknownValueError:
                print("Wikipedia - could not understand audio.")
                tts.get_pronunciation("Sorry, I couldn't understand you.")
            except sr.RequestError as e:
                 print("Wikipedia - could not connect to audio recognition servers.")
                 tts.get_pronunciation("Sorry, I couldn't connect to the audio recogntion service.")
        elif "connect" in question and "Roku" in question: 
            try:
                Roku.discover(timeout=10)
                print("Roku connect - Ready.")
                tts.get_pronunciation("Please use the keyboard to type the IP")
                rokuIP = input("ROKU IP:")
                roku = Roku(rokuIP)
            except:
                print("ERROR. Are you sure that device exists?")
        elif "Roku" in question and "home" in question:
            try:
                print("Doing roku function.")
                tts.get_pronunciation("OK. Going to roku home screen.")
                roku.home()
            except:
                print("ERROR. I don't think you are connected...")
                tts.get_pronunciation("Whoops! Are you sure you are connected?")
        elif "Roku" in question and "Hulu" in question:
            try:
                print("Doing roku function.")
                tts.get_pronunciation("OK. Going to Hulu.")
                app = roku['Hulu']
                app.launch()
            except:
                print("ERROR. I don't think you are connected...")
                tts.get_pronunciation("Whoops! Are you sure you are connected?")
        elif "Roku" in question and "Netflix" in question:
            try:
                print("Doing roku function.")
                tts.get_pronunciation("OK. Going to Netflix.")
                app = roku['Netflix']
                app.launch()
            except:
                print("ERROR. I don't think you are connected...")
                tts.get_pronunciation("Whoops! Are you sure you are connected?")
        elif "Roku" in question and "Youtube" in question:
            try:
                print("Doing roku function.")
                tts.get_pronunciation("OK. Going to YouTube.")
                app = roku['YouTube']
                app.launch()
            except:
                print("ERROR. I don't think you are connected...")
                tts.get_pronunciation("Whoops! Are you sure you are connected?")
        elif "Roku" in question and "IPTV" in question:
            try:
                print("Doing roku function.")
                tts.get_pronunciation("OK. Launching Free View Player.")
                app = roku['FreeView Player']
                app.launch()
            except:
                print("ERROR. I don't think you are connected...")
                tts.get_pronunciation("Whoops! Are you sure you are connected?")
        elif "lifx" in question and "connect" in question:
            try:
                lanLights = LifxLAN()
                print("LIFX CONNECT READY.")
                tts.get_pronunciation("Please say the name of the device.")
                recogntionAudio = r.listen(source)
                lifxLight = lanLights.get_device_by_name(recogntionAudio)
            except:
                print("ERROR. Are you sure that device exists?")
        elif "lifx" in question and "on" in question:
            try:
                print("LIFX on.")
                lifxLight.set_power(true)
            except:
                print("ERROR. Are you sure you are connected?")
        elif "lifx" in question and "off" in question:
            try:
                print("LIFX off.")
                lifxLight.set_power(off)
            except:
                print("ERROR. Are you sure you are connected?")
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

	
