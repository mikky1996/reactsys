from reactsys.Core import Core
from reactsys.Core import triggered_by
from reactsys.callback.Email import Email
from reactsys.triggers.Keylogger import Keylogger

class MyClass(Core):

	'''
	Each trigger is a function with 2 parameters queue and lock which
	should take the responsibility to update the queue with a message
	For example by design this trigger will add message "keylogger_violence" to the queue

	Each trigger should start with the word "trigger"
	'''
	def trigger_keylogger_violence(self, queue, lock):
		k = Keylogger(queue, lock, ["violence"])
		k.run()

	'''
	Each callback is just a funciton (currently with no parameters, but parameters can be added via enclosures for example)
	which will be called if certain message will occur in the message queue

	Each callback should start with the word "callback"
	'''
	@triggered_by("keylogger_violence")
	def callback_keylogger_violence():
		e = Email()
		e.run("testingmypythonscript@gmail.com", message = "Violence was typed in on your laptop!")

if __name__ == "__main__":
	myinstance = MyClass()
	myinstance.run()