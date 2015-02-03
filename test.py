from countminsketch import CountMinSketch
import math

def sketch_em(keycounts):
	sketch = CountMinSketch(1000, 10) # table size=1000, hash functions=10
	# print out the big buckets and 20 random small buckets 
	# for x in range(bigbuckets):
	# 	print ("{:,}".format(x) + ": " + "{:,}".format(sketch[x]) + " (" + "{:,}".format(orig[x]) + ")")
	# 	print ("{:,}".format(x) + ": " + "{:,}".format(sketch.meanquery(x)) + " (" + "{:,}".format(orig[x]) + ")")
	# for x in sorted([random.randrange(bigbuckets, totalbuckets) for i in range(1,20)]):
	# 	print ("{:,}".format(x) + ": " + "{:,}".format(sketch[x]))
	# 	print ("{:,}".format(x) + ": " + "{:,}".format(sketch.meanquery(x)))
	
	totalbuckets = len(keycounts)
	for p in keycounts.iteritems():
		# import pdb; pdb.set_trace()
		sketch.add(p[0], p[1])

	
	sum_sq_error_cm = sum(((s-o)**2) for o, s in zip(keycounts.values(),map(sketch.query, keycounts.keys())))
	mse = sum_sq_error_cm*1.0 / totalbuckets
	print "	CountMin Error: " + "{:,}".format(math.sqrt(mse))
	sum_sq_error_cmm = sum(((s-o)**2) for o, s in zip(keycounts.values(),map(sketch.meanquery, keycounts.keys())))
	mse = sum_sq_error_cmm*1.0 / totalbuckets
	print "	CountMeanMin Error: " + "{:,}".format(math.sqrt(mse))

if __name__ == "__main__":
	# bigbuckets = 5
	# totalbuckets = 100000

	# keycounts = dict()
	# for i in range(bigbuckets):
	# 	keycounts[i] = pow(10,i)
	# for i in range(bigbuckets, totalbuckets):
	# 	keycounts[i] = 1
	# sketch_em(keycounts)
	import numpy
	from collections import defaultdict

	for exp in (3,2,1,0,-1):
		print "Data sampled from Zipf distributions; reporting sqrt(MSE)"
		print "Zipf alpha = " + str(1+10**(-1*exp))
		d = defaultdict(int)
		for i in numpy.random.zipf(1+10**(-1*exp), 100000):
			d[i] += 1
		sketch_em(d)