#!/usr/bin/python3

import sys, fileinput, re, os, socket, psutil, subprocess
import netifaces as ni


def get_ip_address(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']  # determing ip address assigned to the particular interface
    print(ip)


def printhost():
    print(socket.gethostbyaddr(socket.gethostname())[0])  # determining host name by using its ip address

def userlist():
    users = {}
    with open('/etc/passwd') as f:  # opening /etc/passwd file
        for line in f:
            if not line.startswith('#') and line.strip(): 
                user_info =line.split(":")  # splitting every line of the file at ":" character
                users[user_info[0]] = user_info[2] 
    for username, user_id in sorted(users.items()): 
        print(f"   - {username}")
    
            

def list_files(start):
    for start, dirs, files in os.walk(start):  
        for d in dirs: 
            print(os.path.join(start, d))  # printing directories from the starting point entered by the user
        
def processlist():
    processes = []
    for proc in psutil.process_iter(['pid']):
    	p = psutil.Process(pid=proc.pid)
    	processes.append(p.as_dict(attrs=['pid', 'name', 'username', 'memory_percent']))  # selecting attributes of the processes
    print("--------------------Top 10 by Memory Usage---------------------------------")
    mem = sorted(processes, key=lambda i: i['memory_percent'], reverse=True)  # sorting processes according to their memory usage
    count = 0
    while (count < 10):  # printig top 10 memory occupying processes
    	count = count + 1
    	print(mem[count])
           
def sudosearch():
    with open('/var/log/auth.log') as f:  # opening auth.log file
        for line in f:
            if 'sudo' in line:  # printing lines with "sudo" in them
                print(line)
                

def main():
    argument = sys.argv[1]
    if(argument == "--help"):
    	print("Welcome to the Admino system information script")
    	print("Please follow the following instructions to use it")
    	print("- admino -H --> provides hostname information.")
    	print("- admino -i <interface> --> provides the IP address of provided <interface> ")
    	print("- admino -u --> provides the list of users of the system")
    	print("- admino -t <user> --> provides the directory list tree for a system <user>")
    	print("- admino -p --> provides the top 10 processes which are using more %memory")
    	print("- admino -s --> provides the list of SUDO invoked commands from auth.log")
    elif(argument == "-i"):
    	get_ip_address(sys.argv[2])
    elif(argument == "-u"):
    	userlist()
    elif(argument == "-t"):
    	list_files(sys.argv[2])
    elif(argument == "-p"):
    	processlist()
    elif(argument == "-s"):
    	sudosearch()
    elif(argument == "-H"):
    	printhost()
    	
    		
if __name__ == '__main__':
    main()  # calling the main function

