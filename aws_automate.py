#!/usr/bin/env python

"""

With the help of this script, you can do the following operation

-- Create an Instance
-- Stop an Instance
-- Start an Instance
-- Terminate an Instance
-- List all the Instances
-- Check the status of all the instances

"""


# Modules
import argparse
import boto3
import sys
from collections import defaultdict

# Using the EC2 resources
ec2 = boto3.resource('ec2')
ids=[]

## This functions displays the list of the all the instances ##
def list_instances():
        for instance in ec2.instances.all():
                try:
                        for tag in instance.tags:
                                if tag['Key'] == 'Name':
                                        print (instance.id,tag['Value'])
                except (RuntimeError, TypeError, NameError):
                        pass

## This function creates an instance on AWS  ##
def create_instance(name,userda):
        instance = ec2.create_instances(
                        ImageId='ami-xxxxx',
                        MaxCount=1,
                        MinCount=1,
                        InstanceType='t2.micro',
                        TagSpecifications=[
                        {
                                'ResourceType': 'instance',
                                'Tags':[
                                                {
                                                        'Key': 'Name',
                                                        'Value': name
                                                },
                                        ]
                                },
                        ],
                        UserData=userda,
                        NetworkInterfaces=[{    'AssociatePublicIpAddress': True|False,
                                                'DeleteOnTermination': True|False,
                                                'Groups':['sg-xxxxxxxx',],
                                                'DeviceIndex': 0,
                                                'SubnetId': 'subnet-xxxxxxxx'
                                                 }]
                        )
	print "Instance created on the platform"

# Function takes Name as an input and provides instance id as an output
def fetch_instance_id(name):
	for instance in ec2.instances.all():
		try:
			for tag in instance.tags:
				if tag['Key'] == 'Name':
					if tag['Value'] == name:
						return instance.id
		except (RuntimeError, TypeError, NameError):
			pass

# Function used to stop an instance
def stop_instance(name):
	ids.append(fetch_instance_id(name))
        ec2.instances.filter(InstanceIds=ids).stop()
	print "Instance " + name + " is stopped"

# Function used to start an instance
def start_instance(name):
	ids.append(fetch_instance_id(name))
	ec2.instances.filter(InstanceIds=ids).start()
	print "Instance " + name + " is started"

# Function used to terminate an instance
def terminate_instance(name):
        ids.append(fetch_instance_id(name))
        ec2.instances.filter(InstanceIds=ids).terminate()
	print "Instance " + name + " is terminated"

def reboot_instance(name):
	ids.append(fetch_instance_id(name))
	ec2.instances.filter(InstanceIds=ids).reboot()
	print "Instance " + name + " is rebooted"

# Function to fetch information about running instances
def check_status():
	running_instances = ec2.instances.filter(Filters=[{
		'Name': 'instance-state-name',
		'Values': ['running']}])

	ec2info = defaultdict()
	for instance in running_instances:
    		for tag in instance.tags:
        		if 'Name' in tag['Key']:
            			name = tag['Value']
    	# Add instance info to a dictionary
    		ec2info[instance.id] = {
        	'Name': name,
        	'Type': instance.instance_type,
        	'State': instance.state['Name'],
        	'Private IP': instance.private_ip_address,
        	'Public IP': instance.public_ip_address,
        	'Launch Time': instance.launch_time
        }

	attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
	for instance_id, instance in ec2info.items():
    		for key in attributes:
        		print("{0}: {1}".format(key, instance[key]))
    		print("------")



# Funstion used to handle the arguments
def build_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-list',     action='store_true',   
								help='Display all VM')
	parser.add_argument('-create',   action='store',  dest='creat',  
								help='Create an Instance',    type=str,   default="")
	parser.add_argument('-stop',     action='store',  dest='sto',    
								help='Stop an Instance',      type=str,   default="")
	parser.add_argument('-start',    action='store',  dest='star',
								help='Start an Instance',     type=str,   default="")
	parser.add_argument('-term',     action='store',  dest='ter',
								help='Terminate an Instance', type=str,   default="")
	parser.add_argument('-status',   action='store_true',
								help='Check Status')
	parser.add_argument('-userdata', action='store',  dest='userdat',
								help='Add the userdata to the Instance', type=str, default="")
	parser.add_argument('-reboot',   action='store',  dest='reboo',
								help='Reboot Instance',	      type=str,	  default="")
	return parser
	
def main():
	parser = build_parser()
	res = parser.parse_args()
	try:
		assert ( len(sys.argv)>=2 ), "use -h for usage information" 
		if (res.list):
			list_instances()
		elif (res.creat):
			create_instance(res.creat,res.userdat)
		elif (res.sto):
			stop_instance(res.sto)
		elif (res.star):
			start_instance(res.star)
		elif (res.ter):
			terminate_instance(res.ter)
		elif (res.status):
			check_status()
		elif (res.reboo):
			reboot_instance(res.reboo)
	except AssertionError as msg:
		print msg

if __name__ == '__main__':
       	main()
