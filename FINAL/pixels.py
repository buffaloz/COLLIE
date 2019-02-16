import time
import apa102
import threading

try:
	import queue as Queue
except ImportError:
	import Queue as Queue

class Pixels:
	PIXELS_N = 3

	def __init__(self):
		self.basis = [0] * 3 * self.PIXELS_N
		self.basis[0] = 2
		self.basis[3] = 1
		self.basis[4] = 1
		self.basis[7] = 2

		self.colors = [0] * 3 * self.PIXELS_N
		self.dev = apa102.APA102(num_led=self.PIXELS_N)

		self.next = threading.Event()
		self.queue = Queue.Queue()
		self.thread = threading.Thread(target=self._run)
		self.thread.daemon = True
		self.thread.start()

	def ext(self,x):
		self.next.set()
		if x == 1:
			self.queue.put(self._blue)
		elif x == 2 :
			self.queue.put(self._green)
		elif x == 3 :
			self.queue.put(self._purple)			
		else :
			self.queue.put(self._off)

	def _run(self):
		while True:
			func = self.queue.get()
			func()

	def _blue(self) :
		colors=[0,0,15,0,0,15,0,0,15]
		self.write(colors)

	def _green(self) :
		colors=[0,15,0,0,15,0,0,15,0]
		self.write(colors)

	def _purple(self) :
		colors=[5,0,10,5,0,10,5,0,10]
		self.write(colors)

	def _off(self) :
		colors=[0,0,0,0,0,0,0,0,0]
		self.write(colors)

	def write(self, colors):
		for i in range(self.PIXELS_N):
			self.dev.set_pixel(i, int(colors[3*i]), int(colors[3*i + 1]), int(colors[3*i + 2]))
		self.dev.show()

pixels = Pixels()

def State(arg):
	pixels = Pixels()
	pixels.ext(arg)
	time.sleep(0.1)

if __name__ == '__main__':
	pixels.ext(4)
	time.sleep(0.1)
