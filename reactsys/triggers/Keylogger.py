from pynput import keyboard
import threading
import time
import logging

class Keylogger():
	def __init__(self, main_queue, main_lock, query_list):
		# For working with the obj from the core.py
		self.main_queue = main_queue
		self.main_lock = main_lock
		self.query_list = query_list
		# For processing the strings
		self.queue = []
		self.lock = threading.Lock()
		# Deal with logging
		logging.basicConfig()
		self.logger = logging.getLogger('keylogger')
		self.logger.setLevel(logging.DEBUG)

	def clear_queue(self):
		self.logger.debug("Clearing the queue!")
		self.lock.acquire()
		self.queue = []
		self.lock.release()

	def is_query_typed(self):
		self.lock.acquire()
		s = "".join(self.queue)
		self.logger.info(s)
		self.lock.release()
		for query in self.query_list:
			if s.find(query) != -1:
				self.clear_queue()
				return True, query
		return False, None

	def add_action(self, query):
		self.main_lock.acquire()
		self.main_queue.append("keylogger_{}".format(query))
		self.main_lock.release()

	def on_release(self, key):
		self.logger.debug("the key was released!")
		is_typed, query = self.is_query_typed()
		if is_typed:
			self.add_action(query)
		self.logger.debug(self.queue)
		if (key == keyboard.Key.esc):
			return False

	def on_press(self, key):
		self.logger.debug("the key was pushed!")
		if hasattr(key, 'char'):
			self.lock.acquire()
			self.queue.append(key.char)
			self.lock.release()
			self.logger.debug("Char added!")

		if (key == keyboard.Key.space):
			self.lock.acquire()
			self.queue.append(" ")
			self.lock.release()
			self.logger.debug("Space added!")

		if (key == keyboard.Key.backspace):
			self.lock.acquire()
			if (len(self.queue) != 0): 
				self.queue.pop()
			self.lock.release()
			self.logger.debug("Backspace processed!")

	def run(self):
		with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
			listener.join()

if __name__ == "__main__":
	logging.basicConfig()
	logger = logging.getLogger('trigger_test')
	logger.setLevel(logging.DEBUG)
	lock = threading.Lock()
	queue = []
	k = Keylogger(queue, lock, ["porno", "violence"])
	threading.Thread(target=k.run, name='keylogger').start()
	while True:
		logger.debug(" ".join(queue))
		time.sleep(1)
