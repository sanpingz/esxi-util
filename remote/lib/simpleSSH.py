#!/usr/bin/env python
import paramiko 
import select
import sys
import re
paramiko.util.log_to_file('/local/logs/paramiko.log')

class SSHConnect(paramiko.SSHClient):
	def __init__(self, hostname, port=22, username='root', password='newsys', timeout=8):
		super(SSHConnect, self).__init__()
		#paramiko.SSHClient.__init__(self)
		self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.connect(hostname, port=port, username=username, password=password, timeout=timeout)
		self.chan = self.get_transport().open_session()
	def run(self, cmd):
		return self.exec_command(cmd)
	def nrun(self, cmd):
		channel = self.chan	
		channel.exec_command(cmd)
		status = 0
		while True:
			try:
				if channel.exit_status_ready():
					break
				rl, wl, xl = select.select([channel],[],[],0.0)
				if len(rl) > 0:
					# Must be stdout
					rec = channel.recv(1024)
					sys.stdout.write(rec)
			except KeyboardInterrupt:
				print 'Caught Ctrl-C'
				self.stop(cmd)
				raise KeyboardInterrupt
	def stop(self, cmd):
		print r"kill -9 `ps -ef|grep %s|grep -v grep|awk '{print $2}'`" % cmd
		self.chan.exec_command(r"kill -9 `ps -ef|grep %s|grep -v grep|awk '{print $2}'`" % cmd)
	def close(self):
		super(SSHConnect, self).close()
		self.chan.close()


if __name__ == '__main__':
	cnn = SSHConnect('esxi-server', password='vmnewsys')
	stdin, stdout, stderr = cnn.run(r'/vmfs/volumes/datastore1/usr/bin/vm all') 
	for std in stdout.readlines(): 
	   	print std, 
	cnn.close() 
