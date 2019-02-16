import os
import alsaaudio
import wave

def rec(path) :
	RECORD_SECONDS = 2.0
	cmd = ""
	numL,numR,numE,numG,numS,numN = 0,0,0,0,0,0
	code=[]

	while True :
		
		print ("|1 : Left|2 : Right|3 : Emergency|4 : Go |5 : Stop|6 : Noise|7 : End|")
		print ("|cnt : %d |cnt : %d  |cnt : %d      |cnt : %d|cnt: %d  |cnt : %d  |"%(numL,numR,numE,numG,numS,numN))
		try :
			start = int(input("Cmd : "))
		except SyntaxError :
			start = 9
			print "Try again!!\n"

		if start == 1 :
			start=''
			cmd = "Left"
			numL+=1
			WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numL)

		elif start == 2 :
			start=''
			cmd = "Right"
			numR+=1
			WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numR)

		elif start == 3 :
			start=''
			cmd = "Emergency"
			numE+=1
			WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numE)

		elif start == 4 :
			start=''
			cmd = "Go"
			numG+=1
			WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numG)

		elif start == 5 :
			start=''
			cmd = "Stop"
			numS+=1
			WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numS)

		elif start == 6 :
			start=''
			cmd = "Noise"
			numN+=1
			WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numN)

		elif start == 7 :
			break

		else : 
			print "Try again!!\n"
			cmd = ""

		if not cmd == "" :

			# start Recording
			print ("recording...")
			frames = []
			inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
			inp.setchannels(1)
			inp.setrate(26000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
			inp.setperiodsize(1024)
	
			for i in range(0, int(8000 / 1024 * RECORD_SECONDS)):
				l, data = inp.read()
				frames.append(data)
			print ("finished recording")
			print("")
	
			# stop Recording
			waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
			waveFile.setnchannels(1)
			waveFile.setsampwidth(2)
			waveFile.setframerate(26000)
			waveFile.writeframes(b''.join(frames))
			waveFile.close()
	
			code.append(WAVE_OUTPUT_FILENAME)
		
	return code,numS
