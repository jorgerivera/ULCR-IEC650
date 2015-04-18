#!/usr/bin/env python

import pubnub_controls
import time

lab = pubnub_controls.LabDigitales()

while True:
	try:
		for mname in ['set_on', 'set_off', 'set_auto', 'force']:
			for stn, stobj in lab.st.iteritems():
				m = getattr(stobj, mname)
				m()
				print "calling method [%s] of student [%s]" % (mname, stn)
			time.sleep(60)
	except KeyboardInterrupt, e:
		lab.OnClose(None)
		break
