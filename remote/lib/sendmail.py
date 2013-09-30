#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from auth import ad4

SERVER = "CASArray.ad4.ad.alcatel.com"
FROM = "sanping.zhang@alcatel-lucent.com"
CC = ["sanping.zhang@alcatel-lucent.com"] # must be a list
U,P = ad4

def send(_from, to, subject, content, cc='', smtp=SERVER, username=U, password=P):
	# Prepare actual message
	msg = MIMEMultipart()  
	msg['From'] = _from
	if isinstance(to, list):
		tmp = ''
		for t in to:
			tmp += '%s;' % t
		msg['To'] = tmp
	else:
		msg['To'] = to
		to = [to]
	msg['To'] = to
	if cc:
		if isinstance(cc, list):
			tmp = ''
			for c in cc:
				tmp += '%s;' % c
				msg['Cc'] = tmp
				to += cc
		else:
			msg['Cc'] = cc
			to.append(cc)
	msg['Subject'] = subject
	cnt = MIMEText(content)
	print cnt
	msg.attach(cnt)
	# Send the mail
	server = smtplib.SMTP(smtp)
	server.login(username, password)
	print msg
	server.sendmail(_from, to, msg.as_string())
	server.quit()

if __name__ == '__main__':
	send(FROM, FROM, 'hello', 'hello Calvin')
