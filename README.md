#AWS_AUTOMATION

This script uses boto3 module to perform the following operations :-
      -- Create an Instance
      -- Stop an Instance
      -- Start an Instance
      -- Terminate an Instance
      -- List all the Instances
      -- Public ip, Private ip etc of all the running instances
      

USE :-

>> Use -h to see all the options available
   python aws_automate -h
   usage: aws_automate.py [-h] [-list] [-create CREAT] [-stop STO] [-start STAR][-term TER] [-status] [-userdata USERDAT]
   optional arguments:
              -h, --help        show this help message and exit
              -list             Display all VM
              -create CREAT      Create an Instance
              -stop STO          Stop an Instance
              -start STAR        Start an Instance
              -term TER          Terminate an Instance
              -status            Check Status
              -userdata USERDAT  Add the userdata to the Instance
              
>> To list down all the instances
   python aws_automate -list
   
>> Create an instance
   Without userdata :- 
        python aws_automate.py -create < INSTANCE_NAME >
    
   With userdata :-
        python aws_automate.py -create < INSTANCE_NAME > -userdata < “USERDATA” >

>> Stopping an Instance
   python aws_automate.py -stop < INSTANCE NAME > 
   
>> Starting a stoppedInstance
   python aws_automate.py -start< INSTANCE NAME > 

>> Terminating an Instance
   python aws_automate.py -term < INSTANCE NAME >
   
>> Rebootingan Instance
   python aws_automate.py -reboot<INSTANCE NAME >
  
>> Public ip, Private IP etc ) of the running instances
   python aws_automate.py -status
