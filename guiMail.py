#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, BOTH
from Tkinter import *
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from pyx import *
import numpy as np
import matplotlib.pyplot as plt
import os



def overview():
	root = Tk()
	root.geometry('1200x768+300+300')
#	root.pack(fill = BOTH, expand = 1)
#	root.parent.title('AcaEmail')
#	frameInbox = Frame(root)
#	frameInbox.pack(side = LEFT,fill = BOTH)

	frameBackground = Frame(root)
	frameBackground.pack(side = RIGHT,fill = BOTH)
	frameBackground.place(bordermode = INSIDE,height = 1280,width = 768)


	entryRecipient = Entry(frameBackground,bd = 3)
	entryRecipient.pack()
	entryRecipient.place(bordermode = INSIDE, x = 200,y = 10,height = 40,width = 600)

	entryBody = Text(frameBackground,bd=3)
#	entryBody.pack()
	entryBody.place(bordermode = INSIDE, x = 10,y = 100,height = 600,width = 600)

	buttonDelete = Button(frameBackground,text='Delete',fg = 'red',command =lambda:deleteBody(entryBody))
	buttonDelete.pack(side = TOP)
	buttonDelete.place(x = 20,y=20)

	buttonSend = Button(frameBackground,text='Send',fg='red',command = lambda:sendEmail(entryBody,entryRecipient))
	buttonSend.pack(side = TOP)
	buttonSend.place(x=20,y = 40)

	buttonSave = Button(frameBackground,text='Save',fg='red',command = lambda:saveAction(entryBody))
	buttonSave.pack(side = TOP)
	buttonSave.place(x=20,y = 60)


	root.mainloop()

def deleteBody(body):
	body.delete(0,END)

def sendEmail(body,recipient):

	body.get(1.0,END)
	destination  = recipient.get()

	msg = MIMEMultipart('mixed')
	msg['Subject'] = 'Test Email'
	msg['From'] = 'stevenslxie@gmail.com'
	msg['To'] = destination

	msg.preamble = 'This is a multi-part message in MIME format.'

	msg = convertRawEmailToMIME(body,msg)
#msg.attach(msgAll)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.starttls()
	s.login('stevenslxie','2xiexing')
	s.sendmail('stevenslxie@gmail.com', destination, msg.as_string())
	s.quit()

# textSort() sort out the body of the email, identifying those 'plain text' and display as it is. For those Tex, create a .png for each Tex. a Tex starts with a '$' and ends with the same symbol.
def textSort(entryBody):
	body = entryBody.get(1.0,END)
	math = []
	nonMath = []
	seg = []
	mathIndex = []
	lastEnd = -1
	lastStart = 0
	i = 0
	j = 0
	k = 0
	while i < len(body):
#	print i
		if body[i] == '$':
			seg.append(body[lastEnd+1:i])
			k = k+1
			lastStart = i
			for j in range(len(body[i+1:])):
				if body[i+j+1]== '$':
					lastEnd = i+j+1
					seg.append(body[i:lastEnd+1])
					mathIndex.append(k)
					k = k+1
					i = i+j+1
					break
			i = i+1
		else:
			i = i+1
		j = 0
	if lastEnd != len(body)-1:
		seg.append(body[lastEnd+1:])
		k = k+1

#	for s in seg:
#print s
#	print mathIndex
	return seg,mathIndex

# detect which strings are Tex and convert them into images.
def createMathImages(stringSeg,stringIndex):
	i = 0
	for s in stringSeg:
		if i in stringIndex:
			convertTexToImage(s,i)
		i = i+1
	
	
# using PyX to convert Tex to .png Image
def convertTexToImage(mathString,mathIndex):
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	fig = plt.figure()

	print mathString
	ax = fig.add_axes([0,0,1,1])
	ax.text(0.5,0.5,mathString,horizontalalignment='center',verticalalignment='center',fontsize=50)
	ax.set_axis_off()
	s = str(mathIndex)
	path = os.getcwd()+'/'+s

	plt.savefig(path)

def saveAction(body):
	stringSeg,stringIndex = textSort(body)
	createMathImages(stringSeg,stringIndex)

def convertRawEmailToMIME(body,msg):
#msg = MIMEMultipart('Alternative')
	stringSeg,stringIndex = textSort(body)
	createMathImages(stringSeg,stringIndex)

	i = 0
	for s in stringSeg:
		if i in stringIndex:
			message = attachImageToMIME(i)
		else:
			message = attachTextToMIME(s,i)
		msg.attach(message)
		i = i +1
	print msg.get_payload()
	return msg

def attachImageToMIME(i):
#	textMIME = MIMEText('')
	fp = open(str(i)+'.png','rb')
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-Disposition', 'inline', filename=str(i)+'.png')
	fp.close()

	return msgImage

def attachTextToMIME(s,i):
	textMIME = MIMEText(s)
	textMIME.add_header('Content-Disposition', 'inline', filename=str(i)+'.txt')

	return textMIME


	



