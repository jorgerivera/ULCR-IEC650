#!/usr/bin/env python

from Pubnub import Pubnub 
import simplejson as json
import traceback

class BasePubNub(object):
	
	secret_key	= "sec-c-YjFhY2U3MWUtMDIzZS00MzUxLTkyMjgtMmI5ZDMwNGI4YzNj"
	pub_key		= "pub-c-07bede4d-e0d6-4f19-bb9b-fb8414505f36"
	sub_key		= "sub-c-d9e6107e-d34c-11e4-adb1-02ee2ddab7fe"
	channel		= "base"
	
	str_force	= '"query"'
	str_on		= '"set_on"'
	str_off		= '"set_off"'
	str_auto	= '"set_auto"'
	
	def __init__(self, subscribe=True, logcb=None, valuecb=None, swap=False):
		self.channel_down = '%s_down' % self.channel
		self.channel_up = '%s_up' % self.channel
		if swap:
			self.channel_down, self.channel_up = self.channel_up, self.channel_down
		self.pubnub = Pubnub(publish_key=self.pub_key,
							subscribe_key=self.sub_key,
							secret_key=self.secret_key)
		if subscribe:
			self.pubnub.subscribe(channels=self.channel_up,
							callback=self._callback,
							error=self._error_cb)
		self.logcb=logcb
		self.valuecb=valuecb
		
	def logcb(self, text):
		pass
		
	def force(self):
		self.pubnub.publish(self.channel_down, self.str_force)
		
	def set_on(self):
		self.pubnub.publish(self.channel_down, self.str_on)
		
	def set_off(self):
		self.pubnub.publish(self.channel_down, self.str_off)
		
	def set_auto(self):
		self.pubnub.publish(self.channel_down, self.str_auto)
		
	def send_value(self, value):
		info = {'name':self.channel,'value':value}
		self.pubnub.publish(self.channel_down, json.dumps(info))
		
	def _callback(self, message, channel):
		if self.logcb:
			self.logcb("ch [%s] msg [%s]" % (channel, message))
		else:
			print "got called back"
			print "ch [%s]" % channel
			print "msg [%s]" % message
		try:
			if type(message)==str:
				try:
					message = json.loads(message)
				except:
					print "was not a good json"
			#m = json.loads(message)
			if 'value' in message and self.valuecb:
				self.valuecb(self.channel,str(message['value']))
		except ValueError, e:
			print "json failed"			
		except Exception, e:
			print "nope, that didnt work"
			print traceback.format_exc()

	def _error_cb(self, message):
		print "got called back by error"
		print "msg [%s]" % message
		
	def close(self):
		self.pubnub.unsubscribe(channel=self.channel_up)
		
class Belisario(BasePubNub):
	
	channel 	= "belisario"
	
class Marin(BasePubNub):
	
	channel		= "marin"
	
class Molina(BasePubNub):
	
	channel		= "molina"
	
class Valverde(BasePubNub):
	
	channel		= "valverde"
	
class Vazquez(BasePubNub):
	
	channel		= "vazquez"


students = [ 'belisario' , 'marin', 'molina', 'valverde', 'vazquez' ]
st_controls = { 'belisario'	: Belisario,
				'marin'		: Marin,
				'molina'	: Molina,
				'valverde'	: Valverde,
				'vazquez'	: Vazquez }

class LabDigitales(object):

	st = {}
	loglock = None
	def __init__(self):
		for s in students:
			self.st[s] = st_controls[s](logcb=self.logcb,valuecb=self.valuecb)
		if getattr(self,'Bind'):
			import wx
			self.Bind(wx.EVT_CLOSE, self.OnClose)
	
	def button_press(self, event):  # wxGlade: Console.<event_handler>
		butt_name = event.GetEventObject().GetName()
		name = event.GetEventObject().GetParent().GetName()
		print 'pressed %s for st %s' % (butt_name, name)
		if name in self.st:
			m = getattr(self.st[name],butt_name)
			m()
			self.logcb('sent: [%s|%s]' % (name, butt_name))

	def logcb(self, text):
		print "trying to append text to the log_window"
		if self.log_window:
			self.log_window.AppendText("%s\n" % text)
			self.log_window.SendTextUpdatedEvent()
		else:
			print "error adding [%s] to log_window" % text
	
	def valuecb(self, name, val):
		print "val [%s] [%s]" % (name,val)
		valWidget = getattr(self, '%s_value' % name)
		valWidget.ChangeValue(val)
		

	def OnClose(self, event):
		for s in students:
			self.st[s].close()
		event.Skip()

