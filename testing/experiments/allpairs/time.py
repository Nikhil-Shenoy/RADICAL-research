import datetime
import math


start = datetime.datetime.now()

print "The current time is: %s" % start


j = 0
for i in range(0,1000000):
	j += 1




end = datetime.datetime.now()

diff = end - start
print diff.seconds
print diff.microseconds 
print diff.total_seconds()

result = float(diff.total_seconds())
print "The difference is: %f seconds"  % result
