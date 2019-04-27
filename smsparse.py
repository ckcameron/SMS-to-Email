#!/usr/bin/python3

from xml.dom import minidom
import os
import io
import codecs
import mailbox
from email import utils
from datetime import datetime
import string
import sys
import time
import unicodedata

global debug
debug = True

def main():
    print ("This script will parse an XML file and output a .mbox file in the current directory\r\n and a directory named sms both containing all of the messages found in the XML file.\r\n\r\n")
    time.sleep(3)
    print("The script is intended only to parse XML output from the Android application SMS Backup and Restore and will work with no other format.\r\n\r\nPlease note that MMS and advanced message content are not supported yet.\r\n\r\n")
    time.sleep(2)
    print("The script makes a few basic assumptions about the backup it is parsing:\r\n\r\n")
    time.sleep(3)
    print("1. The mobile carrier and number that the messages are associated with is the same across the entire backup\r\n\r\n")
    time.sleep(2)
    print("2. The contact names from your contacts application have been associated with their appriate message and anything without a contact name will be marked as from Unknown\r\n\r\n")
    time.sleep(2)
    print("3. The mail client you are using can import the .mbox format, or the .email files output in the newly created sms directory. Both the directory and mbox file will appear whereever you ran this script\r\n\r\n\r\n\r\n")
    time.sleep(2)
    name = input("Please enter your name as you would like it to appear in the To and From fields in the emails generated: ")
    time.sleep(1)
    number = input("Please enter your 10-digit mobile number: ")
    time.sleep(1)
    print ("\r\nMobile number recorded as: " + number +"\r\n\r\n")
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
    selection = input("Enter the number corresponding to your mobile carrier above: ")
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
        print ("\r\nThe SMS email suffix has been recoded as : ")
        print (SMSemailSuffix)
        print ("\r\n\r\n")
    else:
        print ("\r\n\r\nUnknown Option Selected!\r\n\r\n")
    time.sleep(2)
    infile_name = input("Please give the absolute path of the backup file: ")
    dest_name = (input("\r\n\r\nPlease provide a name for the mailbox you would like to create: ") + ".mbox")
    if debug:
        time.sleep(1)
        print ("Input is:  " + infile_name)
        print ("Output is: " + dest_name)
    dest_mbox = mailbox.mbox(dest_name, create=True)
    dest_mbox.lock()
    
    doc = minidom.parse(infile_name)
    sms = doc.getElementsByTagName("sms") 
    smspath = "sms"
    try:  
        os.mkdir(smspath)
    except OSError:  
        print ("Creation of the directory %s failed" % smspath)
    else:  
        print ("Successfully created the directory %s " % smspath)
    for i in sms:

        filename = (i.getAttribute("contact_name") + " " + i.getAttribute("readable_date") + ".eml")
        script_dir = os.path.dirname(__file__)
        rel_path = "sms/"
        filepath = os.path.join(script_dir, rel_path, filename)
        with codecs.open(filepath, "w+") as file:
            file.write("Date: ")
            rawdate =   utils.parsedate_to_datetime(i.getAttribute("readable_date"))
            message_date = utils.format_datetime(rawdate) 
            file.write(message_date)
            file.write("\r\n")
            message_id = utils.make_msgid(idstring=None, domain="sms.ckcameron.net")
            file.write("Message-ID: ")
            file.write(message_id + "\r\n")
            file.write("From: ")
            if i.getAttribute("type") == 1:
                if i.getAttribute("contact_name") == "unknown":
                    file.write("unknown <" + i.getAttribute("address") + "@unknown.email>" + "\r\nTo: " + name + " <" + number  + "@" + SMSemailSuffix + ">\r\n")
                elif i.getAttribute("contact_name") == "null":
                    file.write("unknown <" + i.getAttribute("address") + "@unknown.email>" + "\r\nTo: " + name + " <" + number  + "@" + SMSemailSuffix + ">\r\n")
                else:
                    file.write(i.getAttribute("contact_name") + " <" + i.getAttribute("address") + "@unkown.email> " + "\r\nTo: " + name + " <" + number  + "@" + SMSemailSuffix + ">\r\n"
)
            else:
                if i.getAttribute("contact_name") == "unknown":
                        file.write(name + " <" + number + "@" + SMSemailSuffix + ">\r\nTo: " + i.getAttribute("contact_name") + " <" + i.getAttribute("address") + "@unkown.email>\r\n")
                elif i.getAttribute("contact_name") == "null":
                    file.write(name + " <" + number + "@" + SMSemailSuffix + ">\r\nTo: " + i.getAttribute("address") + "@unknown.email>\r\n")
                else:
                    file.write(name + " <" + number + "@" + SMSemailSuffix + ">\r\nTo: " + i.getAttribute("address") + "@unknown.email>\r\n")
            file.write("Subject: ")
            file.write(i.getAttribute("body") + "\r\nX-SMS: true\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n")
            file.write(i.getAttribute("body"))
            dest_mbox.add(mailbox.mboxMessage(file))
            file.close()
            dest_mbox.flush()
    dest_mbox.unlock()

main()

