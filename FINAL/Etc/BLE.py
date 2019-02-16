#!/usr/bin/python

import dbus
import os

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".MediaPlayer1"

def sys_volume(state):
	got = os.popen('amixer -c0 get '"'Headphone'"'').readlines()
	ggot = int(got[6].split(' ')[5])
	os.system('amixer -c0 set '"'Headphone'"' %d'%(ggot+state))

def bluez(ADAPTER_INTERFACE):
	bus = dbus.SystemBus()
	manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"),
		"org.freedesktop.DBus.ObjectManager")
	objects = manager.GetManagedObjects()
	for path, ifaces in objects.iteritems():
		adapter = ifaces.get(ADAPTER_INTERFACE)
		if adapter is None:
			continue
	print path
	player = bus.get_object('org.bluez',path)
	BT_Media_iface = dbus.Interface(player, dbus_interface=ADAPTER_INTERFACE)
	return adapter, BT_Media_iface

if __name__ == '__main__':
	print "This is BT_Controller"
	adapter, BT_Media_iface = bluez(ADAPTER_INTERFACE)

	while 1:
		s = raw_input()
		if s == 'quit': 
			print "Good Luck!"
			break
		if s == 'play': BT_Media_iface.Play()
		if s == 'pause': BT_Media_iface.Pause()
		if s == 'stop': BT_Media_iface.Stop()
		if s == 'next': BT_Media_iface.Next()
		if s == 'pre': BT_Media_iface.Previous()
		if s == 'fast': BT_Media_iface.FastForward()
		if s == 'rewind': BT_Media_iface.Rewind()
		if s == 'up': sys_volume(+5)
		if s == 'down': sys_volume(-5)
		if s == 'show':
			adapter, BT_Media_iface = bluez(ADAPTER_INTERFACE)
			track =  adapter.get('Track')
			print 'Title: ' + track.get('Title') 
			print 'Artist: ' + track.get('Artist')
