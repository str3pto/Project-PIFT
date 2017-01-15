#!/usr/bin/python

import sys
import os

def splash ():
        print('''
         .----------------.  .----------------.  .----------------.  .----------------.  
        | .--------------. || .--------------. || .--------------. || .--------------. |        
        | |   ______     | || |     _____    | || |  _________   | || |  _________   | |
        | |  |_   __ \   | || |    |_   _|   | || | |_   ___  |  | || | |  _   _  |  | |
        | |    | |__) |  | || |      | |     | || |   | |_  \_|  | || | |_/ | | \_|  | |
        | |    |  ___/   | || |      | |     | || |   |  _|      | || |     | |      | |
        | |   _| |_      | || |     _| |_    | || |  _| |_       | || |    _| |_     | |
        | |  |_____|     | || |    |_____|   | || | |_____|      | || |   |_____|    | |
        | |              | || |              | || |              | || |              | |
        | '--------------' || '--------------' || '--------------' || '--------------' |
         '----------------'  '----------------'  '----------------'  '----------------' 
        ''')
        print("Welcome to the installation PIFT")

def main ():
        splash()
        print('''
        1) Add Tools
        2) Add Screen Application
        ''')
                        
        choicemenu = raw_input("Please select from the menu above: ")
        while choicemenu != 1 or choicemenu != 2:
                choicemenu = raw_input("Please select from the menu: ")
                        
        if choicemenu == 1:
                print("The program will now install the repositories")
                print("First lets elevate")
                cmd0 = os.system("sudo -i")
                cmd1 = os.system("gpg --keyserver hkp://keys.gnupg.net --recv-key 7D8D0BF6")
                cmd2 = os.system("echo '# Kali linux repositories \ndeb http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list")
                cmd3 = os.system("echo deb-src http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list")
                print("Ready for update")
                raw_input()
                cmd4 = os.system("apt-get update -m")
                os.system("apt-get install dc3dd")
                        

if __name__ == "__main__":
        main()
                                
