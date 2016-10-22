import speech_recognition as sr
#from os import system

dir(sr)

#print("Say something yo")
r = sr.Recognizer()
#OS will give Strings meaning!!	
print("D.E.X.T.E.R")

with sr.Microphone() as source: r.adjust_for_ambient_noise(source)
print("Set minimum threshold to {}".format(r.energy_threshold))

#with sr.Microphone() as source:
#	audio = r.listen(source)
	#r = sr.Recognizer()
print("Say something yo")
with sr.Microphone() as source: audio = r.listen(source)
print("I have retrieved it! Now scanning...")
try: 
	speech = r.recognize_google(audio)
	print("You said: " + speech)

	if speech:
		print("This works!!")
	else:
		print("The speech does not work")
	#print("Your speech is %s" % speech
except	sr.UnknownValueError:
	print("Could not understand audio")
