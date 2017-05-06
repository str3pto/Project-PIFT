#!/usr/bin/python

import sys
import os
import subprocess


ResourcePath = '/usr/share/unblocker'

'''def super():
        user = os.geteuid()
        if user == 0:
                print("Well done, yes you are")
        else:
                print("You need root permissions to execute this program")
                sys.exit(1)'''

def menu():
        a1 = '/dev/sda1'
        b1 = '/dev/sdb1'
        print('''
        0) Unblock/Block sda1 
        1) Unblock/Block sdb1
        2) Exit
        ''')
        print("Currently")
        result1 = statusmenu(a1)
        print "sda1: %s " % result1
        result2 = statusmenu(b1)
        print "sdb1: %s " % result2
        
        choicemenu = raw_input("Please select from the menu above: ")
        return choicemenu

def file_check(filename):#checks if the file inserted exists
    try:
        open(filename, 'r')
        return 1
    except:
        print "This file doesn't seem to exist"
    return 0

def statusmenu(disk):
        resultmenu = subprocess.Popen(['blockdev', '--getro', disk], stdout = subprocess.PIPE).communicate()[0]
        resultmenu = resultmenu[:1]
        if resultmenu == '1':
              resultmenu = "Blocked"
        else:
              resultmenu = "Unblocked"
              
        return resultmenu

def status(disk):
        result = subprocess.Popen(['blockdev', '--getro', disk], stdout = subprocess.PIPE).communicate()[0]
        result = result[:1]
        return result

def unblock(disk):
        unbldisk = subprocess.Popen(['blockdev', '--setrw', disk], stdout = subprocess.PIPE).communicate()[0]
        return

def block(disk):
        blkdisk = subprocess.Popen(['blockdev', '--setro', disk], stdout = subprocess.PIPE).communicate()[0]
        return

def main ():
        a = '/dev/sda1'
        b = '/dev/sdb1'
        choicemenu = menu()
        while choicemenu is not "2":        
                if choicemenu == "0":
                        print("Checking the status of the Disk")
                        diska = status(a)
                        if diska == '1':
                                print("Disk is Readonly")
                                print("Unblocking...")
                                unblock(a)
                                print("Unblocked")
                        else:
                                print("Disk is Readble")
                                print("Blocking...")
                                block(a)
                                print("Blocked")

                        choicemenu = menu()
                elif choicemenu == "1":
                        print("Checking the status of the Disk")
                        diska = status(b)
                        if diska == '1':
                                print("Disk is Readonly")
                                print("Unblocking...")
                                unblock(b)
                                print("Unblocked")
                        else:
                                print("Disk is Readble")
                                print("Blocking...")
                                block(b)
                                print("Blocked")

                        choicemenu = menu()

                #elif choicemenu == "2":
                        '''print("insert the dev block, eg: /dev/sdb2")
                        c1 = raw_input()
                        c2 = file_check(c1)

                        while c2 == 0:
                                print "insert the dev block, eg: /dev/sdb2"
                                c1 = raw_input()
                                c2 = file_check(c1)
                                
                        print("Checking the status of the Disk")
                        diska = status(c2)
                        if diska == '1':
                                print("Disk is Readonly")
                                print("Unblocking...")
                                unblock(a)
                                print("Unblocked")
                        else:
                                print("Disk is Readble")
                                print("Blocking...")
                                block(a)
                                print("Blocked")
                        choicemenu = menu()
                        '''
                else:
                        print "wrong choice"
        print "Bye!"
        raw_input()
                       
                        

if __name__ == "__main__":
        main()
                                

