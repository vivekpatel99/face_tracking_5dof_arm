import time


class Time:
	def __init__(self):
		self.start_time = time.time()
		self.end_time = time.time()

	def startTime(self):
		self.start_time = time.time()

	def endTime(self):
		self.end_time = time.time()

	def totalTime(self):
		print("[Time Elapse]: {}" .format(self.end_time - self.start_time))

	def wait(self, waiting_time = 5):
		time.sleep(waiting_time)

def main():
	t = Time()
	t.startTime()
	t.wait(10)
	t.endTime()
	t.totalTime()

if __name__ == "__main__":
	main()
