import time
import os
ttime = time.localtime(time.time())
#print(ttime)
dat = "date %u-%02u-%02u" % (ttime.tm_year, ttime.tm_mon, ttime.tm_mday+1)
tm = "time %02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
print(dat, tm)
os.system(dat)
os.system(tm)