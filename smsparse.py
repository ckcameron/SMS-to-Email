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
#import atom.data
#import gdata.data
#import gdata.contacts.client
##import gdata.contacts.data
#import phonenumbers
#from phonenumbers import carrier
#import mobile_codes
#import trunofficial
#import requests

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
        print("1. The contact names from your contacts application have been associated with their appriate message and anything without a contact name will be marked as from Unknown for the time being until I can get API approoval from Google to check your Google contacts for the number", 2 * "\r\n")
        time.sleep(3)
        print("2. The mail client you are using can import the .mbox format, or the .eml files output in the newly created sms directory. Both the directory and mbox file will appear whereever you ran this script", 4 * "\r\n")
        time.sleep(2)

        #gather user input for name, mobile number, carrier, desired filename and backuplocation
    
        name = input("Please enter your name as you would like it to appear in the To and From fields in the emails generated: ")
        time.sleep(1)
        mobileNumberCounter = 0
        
        #declare dictionaries for numbers and carriers
        collectedNumbers = {}
        while True:
            mobileNumberCounter = (mobileNumberCounter + 1)
            number = input("\r\n\r\nPlease enter your 10-digit mobile number: ")
            while len(number) != 10:
                print("\r\n\r\nInvalid input. Your phone number must be exactly 10 digits in length.")
                time.sleep(2)
                number =  input("\r\n\r\nPlease enter your 10-digit mobile number: ")
            time.sleep(1)
            print("\r\nMobile number recorded as: " + number + (2 * "\r\n"))
        
            #This feature awaits API approval from Google
            #gacount = input("Please enter the Google account you wish to retrieve your contacts from: ")
        
            #a menu for selecting the mobile carrier (US Specific)

            def menu():
                print(30 * "-", "MOBILE CARRIER" , 30 * "-")
                print("1.  Verizon")
                print("2.  T-Mobile")
                print("3.  AT&T")
                print("4.  Sprint")
                print("5.  Boost Mobile")
                print("6.  Cricket")
                print("7.  Metro PCS")
                print("8.  Tracfone")
                print("9.  US Cellular")
                print("10. Virgin Mobile")
                print("11. Other")
            time.sleep(2)
            menu()
            time.sleep(1)
        
            # declare the approprite SMS email suffix based on carrier
        
            selection = input("\r\n****\r\n****\r\n\r\nEnter the number corresponding to your mobile carrier above: ")
            if selection =='1':
                print("Verizon")
                collectedNumbers[number] = "Verizon"
            elif selection == '2':
                print("T-Mobile")
                collectedNumbers[number] = "T-Mobile"
            elif selection == '3':
                print("AT&T")
                collectedNumbers[number] = "AT&T"
            elif selection == '4':
                print("Sprint")
                collectedNumbers[number] = "Sprint"
            elif selection == '5':
                print("Boost Mobile")
                collectedNumbers[number] = "Boost Mobile"
            elif selection == '6':
                print("Cricket")
                collectedNumbers[number] = "Cricket"
            elif selection == '7':
                print("Metro PCS")
                collectedNumbers[number] = "Metro PCS"
            elif selection == '8':
                print("Tracfone")
                collectedNumbers[number] = "Tracfone"
            elif selection == '9':
                print("US Cellular")
                collectedNumbers[number] = "US Cellular"
            elif selection == '10':
                print("Virgin Mobile")
                collectedNumbers[number] = "Virgin Mobile"
            elif selection == '11':
                otherCarrier = input("\r\n\r\nPlease enter a name for the Carrier: ")
                print("Carrier recorded as : ")
                print(otherCarrier)
                SMSemailSuffix = input("\r\nPlease enter the sms email suffix for your mobile carrier (vtext.com, for example): ")
                print("\r\n\r\nThe SMS email suffix has been recoded as : ")
                print(SMSemailSuffix)
                collectedNumbers[number] = otherCarrier
                customSMSemailSuffixes = {}
                cutomSMSEmailSuffixes[number] = SMSemailSuffix 
                print(2 * "\r\n")
            else:
                print (2 * "\r\n", "Unknown Option Selected!", 2 * "\r\n")
            print("\r\n\r\nYou have entered %s numbers.\r" % mobileNumberCounter)
            print("\r\n\r\nThe Numbers and carriers are: \r\n\r\n\r\n")
            print(collectedNumbers)
            anotherNumber = input("\r\n\r\nDo you have another mobile number to enter? (Y/N) ")
            if anotherNumber in ["Y","y","N","n"]:
                if anotherNumber in ["Y","y"]:
                    pass
                else: 
                    break
            else: 
                break


        time.sleep(2)
        infile_name = input("\r\n\r\nPlease give the absolute path of the backup file (.xml file): ")
        dest_name = (input("\r\n\r\nPlease provide a name for the mailbox you would like to create (the .mbox at the end of the filename will be added for you): ") + ".mbox")
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
            
        #initialize the counters

        smscounter = 0
        mboxcounter = 0
            
        #declare/create the mbox
    
        dest_mbox = mailbox.mbox(dest_name, create=True)
            
        # loop through the messages and process them
            
        for i in sms:
                
            #file related OS variables
                
            filename = (i.getAttribute("contact_name") + " " + i.getAttribute("readable_date") + ".eml")
            rel_path = "sms/"
            filepath = os.path.join(script_dir, rel_path, filename)
                
            #For now we will rely on the contact anme in the backup file, but in the future 
            #we will run the numbers against Google Contacts to retrieve the updated information
                
            if i.getAttribute("contact_name") in ["(Unknown)","unknown","Unknown"]:
                    googleContactName = "Unknown"
            else:
                googleContactName = i.getAttribute("contact_name")
                
            #format the phone number into something we can work with
                
            rawNumber = i.getAttribute("address")
            if "+" in rawNumber:
                strippedNumber = rawNumber.strip('+1')
            else:
                strippedNumber = rawNumber
                
                #Lookup the mobile carrier for that number and declare the correct SMS email address based the returned carrier
                #For now I cannot find a free way to do this, so I putting the feature on hold.

            mobileCarrier = "unknown"

            if "Verizon" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@vtext.com")
            elif "T-Mobile" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@tmomail.net")
            elif "AT&T" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@txt.att.net")
            elif "Sprint" in mobileCarrier:            
                    SMSemailAddress = (strippedNumber + "@messaging.sprintpcs.com")
            elif "Boost" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@myboostmobile.com")
            elif "cket" in mobileCarrier:
                    SMSemailAddress = (formatteedNumber + "@sms.mycricket.com")
            elif "Metro" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@mymetropcs.com")
            elif "Trac" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@mmst5.tracfone.com")
            elif "US" in mobileCarrier:
                    SMSemailAddress = (strippedNumber +"@email.uscc.net")
            elif "Virgin" in mobileCarrier:
                    SMSemailAddress = (strippedNumber + "@vmobl.com")
            elif mobileCarrier == "unknown":
                    SMSemailAddress = (strippedNumber + "@unknown-carrier.net")
            else:
                    SMSemailAddress = (strippedNumber + "@unknown-carrier.net")
               
            #write out the email data now that things are parsed, looked-up, formatted and ready
               
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
                    
                if strippedNumber in collectedNumbers:
                    if collectedNumbers[strippedNumber] == "Verizon":
                        SMSemailSuffix = "@vtext.com"
                    elif collectedNumbers[strippedNumber] == "T-Mobile":
                        SMSemailSuffix = "tmomail.net"
                    elif collectedNumbers[strippedNumber] == "AT&T":
                        SMSemailSuffix = "txt.att.net"
                    elif collectedNumbers[strippedNumber] == "Sprint":            
                        SMSemailSuffix = "messaging.sprintpcs.com"
                    elif collectedNumbers[strippedNumber] == "Boost Mobile":
                        SMSemailSuffix = "myboostmobile.com"
                    elif collectedNumbers[strippedNumber] == "Cricket":
                        SMSemailSuffix = "sms.mycricket.com"
                    elif collectedNumbers[strippedNumber] == "Metro PCS":
                        SMSemailSuffix = "mymetropcs.com"
                    elif collectedNumbers[strippedNumber] == "Tracfone":
                        SMSemailSuffix = "mmst5.tracfone.com"
                    elif collectedNumbers[strippedNumber] == "US Cellular":
                        SMSemailSuffix = "email.uscc.net"
                    elif collectedNumbers[strippedNumber] == "Virgin Mobile":
                        SMSemailSuffix = "vmobl.com"
                    elif collectedNumbers[strippedNumber] == "Other":
                        pass
                    else:
                        SMSemailSuffix = "unknown-carrier.net" 
                    file.write(googleContactName +" <" + SMSemailAddress + ">" + "\r\nTo: " + name + " <" + strippedNumber  + "@" + SMSemailSuffix + ">\r\n")

                else:
                    file.write(name + " <" + strippedNumber + "@" + SMSemailSuffix + ">\r\nTo: " + googleContactName + " <" + SMSemailAddress + ">\r\n")
                file.write("Subject: [SMS] ")
                file.write(i.getAttribute("body") + "\r\nX-SMS: true\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n")
                file.write(i.getAttribute("body"))
                file.close()
                    
                    #define a function and a try loop for adding the eml files to the mbox file

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
        print("************************************\r\n***********************************\r\nProcessing of the SMS backup file is complete. Find the eml files in the sms directory or they are all included in the mbox file just created with the name of your choosing.") 
        return 0

                            
    
                        
    #handle exceptions and cleanup
    except Exception:
        lockfile = os.path.join(script_dir, dest_name + ".lock*")
        mboxfile = os.path.join(script_dir, dest_name)
        if os.path.exists(lockfile) and os.path.exists(mboxfile):
            os.remove(lockfile)
            os.remove(mboxfile)
            shutil.rmtree(smspath)
            return 1
        elif os.path.exists(mboxfile):
            os.remove(mboxfile)
            shutil.rmtree(smspath)
            return 1
        else:
            shutil.rmtree(smspath)
            return 1

if __name__ == '__main__':
    sys.exit(main())
