#!/usr/bin/python3
#Copyright (C) 2019 CK Cameron (chase@ckcameron.net)
#
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

#import modules
from xml.dom import minidom
import os
import io
import codecs
import mailbox
from email import utils
from datetime import datetime
import string
import sys
from sys import *
import shutil
import time
import unicodedata

global debug
debug = True

def main():

    try:        
        #Print basic inforamtion about the script
    
        print ("This script will parse an XML file and output a .mbox file in the current directory\r\n and a directory named sms both containing all of the messages found in the XML file.", 2 * "\r\n")
        time.sleep(3)
        print("The script is intended only to parse XML output from the Android application SMS Backup and Restore and will work with no other format.", 2 * "\r\n", "Please note that MMS and advanced message content are not supported yet.", 2 * "\r\n")
        time.sleep(3)
        print("The script makes a few basic assumptions about the backup it is parsing:", 2 * "\r\n")
        time.sleep(3)
        print("1. The mobile carrier and number that the messages are associated with is the same across the entire backup", 2 * "\r\n")
        time.sleep(3)
        print("2. The contact names from your contacts application have been associated with their appriate message and anything without a contact name will be marked as from Unknown", 2 * "\r\n")
        time.sleep(3)
        print("3. The mail client you are using can import the .mbox format, or the .eml files output in the newly created sms directory. Both the directory and mbox file will appear whereever you ran this script", 4 * "\r\n")
        time.sleep(2)

        #gather user input for name, mobile number, carrier, desired filename and backuplocation
    
        name = input("Please enter your name as you would like it to appear in the To and From fields in the emails generated: ")
        time.sleep(1)
        number = input("\r\n\r\nPlease enter your 10-digit mobile number: ")
        time.sleep(1)
        print ("\r\nMobile number recorded as: " + number + (2 * "\r\n"))
        def menu():
            print (30 * "-", "MOBILE CARRIER" , 30 * "-")
            print ("1. Verizon")
            print ("2. T-Mobile")
            print ("3. AT&T")
            print ("4. Sprint")
            print ("5. Other")
        time.sleep(2)
        menu()
        time.sleep(2)
        
        #a menu for selecting the mobile carrier (US Specific)
    
        selection = input("\r\nEnter the number corresponding to your mobile carrier above: ")
        if selection =='1':
            print ("Verizon")
            SMSemailSuffix = "vtext.com"
        elif selection == '2':
            print ("T-Mobile")
            SMSemailSuffix = "tmomail.net"
        elif selection == '3':
            print ("AT&T")
            SMSemailSuffix = "txt.att.net"
        elif selection == '4':
            print ("Sprint")
            SMSemailSuffix = "messaging.sprintpcs.com"
        elif selection == '5':
            SMSemailSuffix = input("Please enter the sms email suffix for your mobile carrier (vtext.com, for example): ")
            print("\r\nThe SMS email suffix has been recoded as : ")
            print(SMSemailSuffix)
            print(2 * "\r\n")
        else:
            print (2 * "\r\n", "Unknown Option Selected!", 2 * "\r\n")
        time.sleep(2)
        infile_name = input("\r\n\r\nPlease give the absolute path of the backup file: ")
        dest_name = (input("\r\n\r\nPlease provide a name for the mailbox you would like to create: ") + ".mbox")
        smspath = "sms"
        script_dir = os.path.dirname(__file__)
        time.sleep(1)
        print (2 * "\r\n", "Input is:  " + infile_name)
        print (2 * "\r\n", "Output is: " + dest_name)
        
        #attempt to create the sms directory
        
        try:  
            os.mkdir(smspath)
        except OSError:  
            print("Creation of the directory %s failed\r" % (smspath))
        else:  
            print("Successfully created the directory %s \r" % (smspath))
            time.sleep(5)
            print((3 * "\r\n") + "Hold on, this could take a while, depending on the number of messages being processed." + (2 * "\r\n"))
    
            #parse the backup file by XML tag atttribute
    
            doc = minidom.parse(infile_name)
            sms = doc.getElementsByTagName("sms") 
            smscounter = 0
            mboxcounter = 0
            #declare/create the mbox
    
            dest_mbox = mailbox.mbox(dest_name, create=True)
            
            for i in sms:
                filename = (i.getAttribute("contact_name") + " " + i.getAttribute("readable_date") + ".eml")
                rel_path = "sms/"
                filepath = os.path.join(script_dir, rel_path, filename)
                with open(filepath, "w+") as file:
                    file.write("Date: ")
                    rawdate = utils.parsedate_to_datetime(i.getAttribute("readable_date"))
                    message_date = utils.format_datetime(rawdate) 
                    file.write(message_date)
                    file.write("\r\n")
                    message_id = utils.make_msgid(idstring=None, domain="sms.smsparse-py.net")
                    file.write("Message-ID: ")
                    file.write(message_id + "\r\n")
                    file.write("From: ")
                    if i.getAttribute("type") == 1:
                            file.write(i.getAttribute("address") + "\r\nTo: " + name + " <" + number  + "@" + SMSemailSuffix + ">\r\n"
)
                    else:
                            file.write(name + " <" + number + "@" + SMSemailSuffix + ">\r\nTo: " + i.getAttribute("address") + "\r\n")
                    file.write("Subject: ")
                    file.write(i.getAttribute("body") + "\r\nX-SMS: true\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n")
                    file.write(i.getAttribute("body"))
                    file.close()
                    
                    #define a function and a try loop for adding the eml files to the mbox fil

                    def addEMLtoMbox(file, dest_mbox):
                                try:
                                    dest_mbox.add(file)
                                except:
                                    dest_mbox.close()
                                    raise

                    #reopen the file and add it to the mbox now that it is complete

                    with open(filepath, "rb") as file:
                        dest_mbox.lock()
                        addEMLtoMbox(file, dest_mbox)
                        file.close()
                        dest_mbox.unlock()
                        smscounter = (smscounter + 1)
                        stdout.write('Number of SMS files Processed: %s \r' % (smscounter))
            print(2 * "\r\n")       
            stdout.flush();
            print("Processing of the SMS backup file is complete. Find the eml files in the sms directory or they are all included in the mbox file just created with the name of your choosing.") 
        return 0

                            
    
                        
    #handle exceptions and cleanup
    except Exception:
        os.remove(os.path.join(script_dir, dest_name))
        os.remove(os.path.join(script_dir, dest_name) + ".lock")
        shutil.rmtree(smspath)
        return 1

if __name__ == '__main__':
    sys.exit(main())
