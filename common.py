#!/usr/bin/env python
"""common ESXi operation"""
__author__ = 'sanpingz (sanping.zhang@alcatel-lucent.com'

import re
import os
import time
import sys
from os.path import join

DS=r'/vmfs/volumes/datastore1'
ATE_LAB = join(DS, 'ATE_LAB')
LABs = ['vn001', 'vn002', 'vn003']
VMs = ['diskfull_a01', 'diskfull_b01', 'diskfull_c01']
VMDK = 'diskfull.vmdk'
VMX = 'diskfull.vmx'

def print_cmd(func):
	def _deco(args):
		resp = func(args)
		if resp:
			resp = resp.strip()
			print '%s => %s' % (args, resp)
		else:
			print args
		return resp
	return _deco
	
@print_cmd
def run(args):
	return os.popen(args).read()

def doit(args):
        return os.popen(args).read()

def getstate(id):
	cmd = r'vim-cmd vmsvc/power.getstate %s|sed -n -e 2p' % id
	resp = doit(cmd)
	return resp.strip() if resp else 'unknown'
	
class VM(object):
	def __init__(self, name):
		self.name = name
		self.id = 0
		self.state = ''
	def getvmid(self):
		cmd = r"vim-cmd vmsvc/getallvms|grep %s|awk '{print $1}'" % self.name
		resp = run(cmd)
		if resp and resp.split()[0]:
			id = resp.split()[0]
			if str(id).isdigit():
				self.id = id
		return self.id
	def getvmstate(self):
		id = self.id or self.getvmid()
		cmd = r'vim-cmd vmsvc/power.getstate %s|sed -n -e 2p' % id
		resp = run(cmd) if id else id
		self.state = resp and resp.strip()
		return self.state
	def poweroff(self, timeout=15, fq=3):
		state = self.getvmstate()
		cmd = 'vim-cmd vmsvc/power.off %s' % self.id
		if state and not re.match(r'Powered off', state):
			count = (timeout+fq-1)/fq
			while count:
				run(cmd)
				time.sleep(timeout/fq)
				count -= 1
				state = self.getvmstate()
				if state and not re.match(r'Powered off failed', state):
					break	
	def poweron(self):
		state = self.getvmstate()
		cmd = 'vim-cmd vmsvc/power.on %s' % self.id
		if state and not re.match('Powered on', state):
			run(cmd)
	def reboot(self):
		cmd = 'vim-cmd vmsvc/power.reboot %s' % self.id
		run(cmd)
	def shutdown(self):
		cmd = 'vim-cmd vmsvc/power.shutdown %s' % self.id
		run(cmd)
		
if __name__ == '__main__':
	raise Exception('Not an executable module')
