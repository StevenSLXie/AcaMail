# Import smtplib for the actual sending function
import smtplib
import imaplib
import email

# Import the email modules we'll need
from email.mime.text import MIMEText


# The sendMail function provides a simple way to send the content of a .txt file as 
# the body of a email. Several to be done: 1) options for typing strings or use a textfile;
# 2) support other email server; 3) error handling.

def sendMail(source,password,destination,title,textfile):
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open(textfile, 'rb')
	# Create a text/plain message
	msg = MIMEText(fp.read())
	fp.close()

	msg['Subject'] = title
	msg['From'] = source
	msg['To'] = destination

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('smtp.gmail.com:587')
	s.starttls()
	s.login(source,password)
	s.sendmail(source, destination, msg.as_string())
	s.quit()

# read the latest raw email data from Gmail Inbox. Several to be done: 1) select the number of latest emails to rea#d; 2) select with key words; 3) error handling;
def readRawMail(username,password):
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(username, password)
	mail.list()
	rawEmail = []
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.
	result, data = mail.search(None, "ALL")
 
	result, data = mail.uid('search', None, "ALL") # search and return uids instead
	latestEmailUid = data[0].split()[-10:-1]
#	print latestEmailUid
	for mailId in latestEmailUid:
		result, data = mail.uid('fetch', mailId, '(RFC822)')
		rawEmail.append(data[0][1])

	return rawEmail

def eachRawMailTidyUp(eachRawEmail):
	emailMessage = email.message_from_string(eachRawEmail)
#	print emailMessage['To']
#	print email.utils.parseaddr(emailMessage['From'])
#	print emailMessage.items() # print all headers
	mainType = emailMessage.get_content_maintype()
	if mainType == 'text':
		print emailMessage.get_payload()
	elif mainType == 'multipart':
		for part in emailMessage.get_payload():
			if part.get_content_maintype() == 'text':
				print part.get_payload()

def tidyUpBatch(rawEmail):
	for mail in rawEmail:
		eachRawMailTidyUp(mail)


def test():
	rawEmail = readRawMail('stevenslxie@gmail.com','2xiexing')
	tidyUpBatch(rawEmail)
#rawMailTidyUp(rawEmail)
