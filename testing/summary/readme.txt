Iteration 1:
	- Contains first draft of graphs
	- All images are of weak scaling experiments on Stampede
Iteration 2:
	- Intended analyze scaling behaviour of different parameters (steps, strong, weak)
	- Didn't find pronounced pattern in the data

Iteration 3:
	- Weak Scaling and Strong Scaling experiments for SA and Pipeline
	- Pipeline was actually done using the Bag of Tasks class instead, as Vivek is fixing the profiler for Pipeline
	- Encountered error in SA profiling: profiler does not record the "StagingOutput" or "Done" phases when doing strong scaling. Currently investigating
	- Encountered error with even simple Repex scripts where the script fails on "time.sleep(3)"

Scripts are in the "scripts" folder.
The "Borrowed" folder includes files from others that I used to help me with my experiments
