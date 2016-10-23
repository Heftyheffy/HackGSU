import speech_recognition as sr
import pyttsx
import win32com.client
import threading
from Dexter import runDexter

engine = pyttsx.init()

dir(sr)

r = sr.Recognizer()
print("D.E.X.T.E.R")
running = True

a = threading.Thread(target = runDexter)
a.start()

while running:

	try:
		with sr.Microphone() as source: r.adjust_for_ambient_noise(source)

		print("Say something: ")
		with sr.Microphone() as source: audio = r.listen(source)
		speech = r.recognize_google(audio)
	
		if "exit" in speech:
			print("I am exiting...")
			running = False
		if "where" in speech:
			shirtFile = open('shirt.txt', 'r')
			cupFile = open('cup.txt', 'r')
			cup = cupFile.read()
			shirt = shirtFile.read()
			shirt = int(shirt)
			if "shirt" in speech:
				if(shirt <= 300):
					print('You are wearing your shirt')
					#engine.say('You are not wearing it')
				else:
					print('Your shirt is under the desk.')
					#engine.say('You are wearing it.')
					#engine.runAndWait()
			elif "laptop" in speech:
				print("your laptop is on the desk")
	except sr.UnknownValueError:
		print("Could not understand audio")
