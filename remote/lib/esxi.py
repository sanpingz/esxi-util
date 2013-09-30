#!/usr/bin/env python
"""The API of operating remote ESXi server
Usage: esxi <cmd> <args>
Available commands:
	create_image <labname>				# e.g. cz001, cz002, cz003
	vm all						# show all VMs
	vm state <labname>				# show state of VMs
	vm <poweron|poweroff|reboot> <vmid>		# operate VM, vmid can be got by running 'vm state [labname]' or 'vm all'
"""

__author__ = 'sanpingz (sanping.zhang@alcatel-lucent.com'

from simpleSSH import SSHConnect
import sys

CMD_PATH = r'/vmfs/volumes/datastore1/usr/bin'

def run(cmd, argv, path=CMD_PATH):
	cnn = SSHConnect('esxi-server', password='vmnewsys')
	args = (reduce(lambda x,y: '%s %s ' % (x,y), argv)).strip()
	cmd = r'%s/%s %s' % (path, cmd, args)
	#print 'run \'%s\'' % cmd
	#sys.exit()
	try:
		stdin, stdout, stderr = cnn.run(cmd)
		stat = stdout.channel.recv_exit_status()
		if stat:
			print stderr.read()
			sys.exit()
		#for std in stdout.readlines():
		#	print std,
		while True:
			line = stdout.readline()
			if not line:
				break
			print line.strip()
	except Exception, e:
		cnn.close()
		print e
def nrun(cmd, argv, path=CMD_PATH):
	ssh = SSHConnect('esxi-server', password='vmnewsys')
	args = (reduce(lambda x,y: '%s %s ' % (x,y), argv)).strip()
	cmd = r'%s/%s %s' % (path, cmd, args)
	try:
		ssh.nrun(cmd)
		ssh.close()
	except Exception, e:
		ssh.close()
		print e
 
if __name__ == '__main__':
	pass
