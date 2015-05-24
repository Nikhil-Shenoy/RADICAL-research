import os
import sys
import radical.pilot as rp

os.system("scp reverse nrs76@india.futuregrid.org:~/")


def pilot_state_cb (pilot, state) :
    """ this callback is invoked on all pilot state changes """

    print "[Callback]: ComputePilot '%s' state changed to %s at %s." % (pilot.uid, state, datetime.datetime.now())

    if  state == rp.FAILED:
        sys.exit (1)

#------------------------------------------------------------------------------
#
def unit_state_cb (unit, state) :
    """ this callback is invoked on all unit state changes """

    print "[Callback]: ComputeUnit '%s' state changed to %s at %s." % (unit.uid, state, datetime.datetime.now())

    if state in [rp.FAILED] :
        print "stdout: %s" % unit.stdout
        print "stderr: %s" % unit.stderr

os.system('clear')

print "Seeing if I can come up with a Radical Script on my own"
print "NEED TO PRINT ALL OBJECT IDS"

# if database_url parameter is not set, whatever the environment variable
# RADICAL_PILOT_DBURL is set to will be used 
my_session = rp.Session(database_url="mongodb://ec2-54-221-194-147.compute-1.amazonaws.com:24242/")
#my_session = rp.Session()

print " Now we create a Context object"
context = rp.Context('ssh') # We communicate with the machine doing the work via ssh 
context.user_id = "nrs76"
my_session.add_context(context)

print "Let's create a Pilot Manager"

pm = rp.PilotManager(session = my_session)

print " Now we create the description for a Compute Pilot and submit it to the Pilot Manager"

pd = rp.ComputePilotDescription()
pd.resource = 'futuregrid.india'
pd.cores = 1
pd.runtime = 5 # minutes

print " submitting the Pilot Description to the Pilot Manager to create the Pilot"

pilot = pm.submit_pilots(pd)

print "Create the Unit Manager"
um = rp.UnitManager(session = my_session, scheduler=rp.SCHED_DIRECT_SUBMISSION)

# Unit Manager needs Pilots, Compute Units, and a Schedule Type. Schedule Type is specified in the Unit Manager's constructor 

print "Add the pilot to the Unit Manager"
um.add_pilots(pilot)

# Now let's create some CUs!

# empty array for CUs

my_cus = []

Input = "alpha.txt"
print "Adding rest of the CUs"
for i in range(1,10):
	output = "final%s.txt" % i

	print "Output file name: %s" % output

	cud = rp.ComputeUnitDescription()
	cud.executable = "~/reverse"
	cud.cores = 1
	cud.arguments = [Input , output ]
	cud.input_staging = Input
	cud.output_staging = output
	my_cus.append(cud)


print "Submitting All CUs"
my_units = um.submit_units(my_cus)

print "Waiting on all CUs"
um.wait_units()

os.system("mkdir results; mv -t results final*")

print "Closing the session"
my_session.close()









