#Manages the knowledge base used to think.
import sys, glob
import time
import aiml

kernel = aiml.Kernel()
for file in glob.glob('ai/*.aiml'):
	kernel.learn(file)

kernel.respond("LOAD AIML B")

while True:
	print("\n" * 100)
	input = input("S> ")
	response = kernel.respond(input)
	print("\n" * 100)
	print(input)
	time.sleep(15)