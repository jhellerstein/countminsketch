from countminsketch import CountMinSketch
import math

def sketch_em(keycounts, numsamples):
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
	cm_rmse = math.sqrt(sum_sq_error_cm*1.0 / totalbuckets)
	# print "	CountMin RMSE: " + "{:,}".format(cm_rmse) + " (" + str(cm_rmse*100.0/numsamples) + "%)"
	sum_sq_error_cmm = sum(((s-o)**2) for o, s in zip(keycounts.values(),map(sketch.meanquery, keycounts.keys())))
	cmm_rmse = math.sqrt(sum_sq_error_cmm*1.0 / totalbuckets)
	# print "	CountMeanMin RMSE: " + "{:,}".format(cmm_rmse) + " (" + str(cmm_rmse*100.0/numsamples) + "%)"
	return (cm_rmse, cmm_rmse)

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

	numsamples = 100000
	iterations = 10
	results = []

	# print str(iterations) + " iterations of " + str(numsamples) + " points sampled from Zipf distributions."

	print "iteration,s,cm_rmse,cmm_rmse,distinct_values"
	for i in range(0,iterations):
		seq_dict = {x: 1 for x in range(0,numsamples)}
		results = sketch_em(seq_dict, numsamples)
		print str(i) + ",uniform," + str(results[0]) + "," + str(results[1]) + "," + str(numsamples)
		for exp in (4,3,2,1,0):
			d = defaultdict(int)
			exp = 1+10**(-1*exp)
			for i in numpy.random.zipf(exp, numsamples):
				d[i] += 1
			# print "Zipf alpha = " + str(1+10**(-1*exp)) + ", " + str(len(d)*100.0/numsamples) + "% distinct values"
			# results.append([exp] + sketch_em(d, numsamples))
			results = sketch_em(d, numsamples)
			print str(i) + "," + str(exp) + "," + str(results[0]) + "," + str(results[1]) + "," + str(len(d))
