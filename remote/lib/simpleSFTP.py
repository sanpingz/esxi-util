#!/usr/bin/env python
import paramiko 

paramiko.util.log_to_file('/local/logs/paramiko.log')

def transport(hostname, port=22, username='root', password='newsys'):
	t = paramiko.Transport((hostname, port))
	t.connect(username=username, password=password)
	return t

def SFTPConnect(t):
	return paramiko.SFTPClient.from_transport(t)

class SFTPCNN(object):
	def __init__(self, hostname, port=22, username='root', password='newsys'):
		t = paramiko.Transport((hostname, port))
		t.connect(username=username, password=password)
		#self = paramiko.SFTPClient.from_transport(t)
		self.sftp = paramiko.SFTPClient.from_transport(t)
		self.transport = t
	def getSFTP(self):
		return self.sftp
	def close(self):
		#self.sftp.close()
		self.transport.close()

if __name__ == '__main__':
	t = transport('vn002')
	try:
		sftp = SFTPConnect(t)
		print sftp.listdir()
		t.close() 
	except Exception, e:
		try:
			t.close()
		except: pass
		sys.exit(1)
