import datetime
import time

now = datetime.datetime.now()
print(now.timetuple())
# tm_year=2017, tm_mon=8, tm_mday=9, tm_hour=12, tm_min=3, tm_sec=35, tm_wday=2, tm_yday=221, tm_isdst=-1
tup = (2017, 8, 9, 11, 50, 9, 0, 0, -1,)
timestamp = time.mktime(tup)
print(timestamp)

print(time.ctime(1502178644))
