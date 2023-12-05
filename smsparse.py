#!bin/python
#Copyright (C) 2019 CK Cameron (chase@ckcameron.net)
#
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

#import modules
from __future__ import print_function
from xml.dom import minidom
import os
import json
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
import py-imessage
import unicodedata
import requests
import pickle
import platform
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly'] 

global debug
debug = True
def main():
        '''This is the Big enchilada which will check to see what OS you are working wihtin, gather the necessary data, and process your input files'''
        #Check for macOS
        macOS = 0
        if "macOS" in platform.platform():
            macOS = 1
        else: 
            pass
        
        #Print basic inforamtion about the script
    
        print ("This script will parse an XML file and output a .mbox file in the current directory\r\n and a directory named sms both containing all of the messages found in the XML file.", 2 * "\r\n")
        time.sleep(3)
        print("The script is intended only to parse XML output from the Android application SMS Backup and Restore and will work with no other format.", 2 * "\r\n", "Please note that MMS and advanced message content are not supported yet.", 2 * "\r\n")
        time.sleep(5)
        
        #gather user input for name, mobile number, carrier, desired filename and backuplocation
    
        myname = input("Please enter your name as you would like it to appear in the To and From fields in the emails generated: ")
        time.sleep(1)
        mobileNumberCounter = 0
        
        
        #declare dictionaries for numbers and carriers
        collectedNumbers = {}
        while True:
            mobileNumberCounter = (mobileNumberCounter + 1)
            mynumber = input("\r\n\r\nPlease enter your 10-digit mobile number: ")
            while len(mynumber) != 10:
                print("\r\n\r\nInvalid input. Your phone number must be exactly 10 digits in length.")
                time.sleep(2)
                mynumber =  input("\r\n\r\nPlease enter your 10-digit mobile number: ")
            time.sleep(1)
            print("\r\nMobile number recorded as: " + mynumber + (2 * "\r\n"))
            shallDefault = input("\r\n\r\nShall this number be used as the default for messages being addressed from you? (Y/N) ")
            if shallDefault == "Y" or shallDefault == "y":
                defaultNumber = mynumber
            else:
                pass
            #dict of the carriers and their sms domain suffixes
            carriers={\
                "ACS Wireless":[@paging.acswireless.com],\
                "Advantage Communications":[@advantagepaging.com],\
                "Airtouch Pagers":[@myairmail.com,\ @alphapage.airtouch.com,\ @airtouch.net,\ @airtouchpaging.com],\
                "Alltel":[@alltelmessage.com],\
                "Alltel PCS":[@message.alltel.com],\
                "Ameritech Paging":[@paging.acswireless.com,\ @pageapi.com],\
                "Ameritech Clearpath":[@clearpath.acswireless.com],\
                "Andhra Pradesh Airtel":[@airtelap.com],\
                "Arch Pagers (PageNet)":[@archwireless.net,\ @epage.arch.com,\ @archwireless.net],\
                "AT&T":[@mms.att.net,\ @txt.att.net],\
                "AT&T Pocketnet PCS":[@dpcs.mobile.att.net],\
                "Beepwear":[@beepwear.net],\
                "BeeLine GSM":[@sms.beemail.ru],\
                "Bell Atlantic":[@message.bam.com],\
                "Bell Canada":[@txt.bellmobility.ca,\ @bellmobility.ca],\
                "Bell Mobility":[@txt.bellmobility.ca],\
                "Bell South (Blackberry)":[@bellsouthtips.com],\
                "Bell South":[@sms.bellsouth.com,\ @wireless.bellsouth.com,\ @blsdcs.net,\ @bellsouth.cl],\
                "Bell South Mobility":[@blsdcs.net],\
                "Blue Sky Frog":[@blueskyfrog.com],\
                "Bluegrass Cellular":[@sms.bluecell.com],\
                "Boost":[@myboostmobile.com],\
                "BPL mobile":[@bplmobile.com],\
                "Cellular One East Coast":[@phone.cellone.net],\
                "Cellular One South West":[@swmsg.com],\
                "Cellular One PCS":[@paging.cellone-sf.com],\
                "Cellular One":[@mobile.celloneusa.com,\ @cellularone.txtmsg.com,\ @cellularone.textmsg.com,\ @cell1.textmsg.com,\ @message.cellone-sf.com,\ @sbcemail.com],\
                "Cellular One West":[@mycellone.com],\
                "Cellular South":[@csouth1.com],\
                "Central Vermont Communications":[@cvcpaging.com],\
                "CenturyTel":[@messaging.centurytel.net],\
                "Chennai RPG Cellular":[@rpgmail.net],\
                "Chennai Skycell / Airtel":[@airtelchennai.com],\
                "Cincinnati Bell":[@mobile.att.net],\
                "Cingular Wireless":[@mycingular.textmsg.com,\ @mobile.mycingular.com,\ @mobile.mycingular.net],\
                "Claro Wireless":[@vtexto],\
                "Clearnet":[@msg.clearnet.com],\
                "Comcast":[@comcastpcs.textmsg.com],\
                "Comviq":[@sms.comviq.se],\
                "Cook Paging":[@cookmail.com],\
                "Corr Wireless Communications":[@corrwireless.net],\
                "Delhi Aritel":[@airtelmail.com],\
                "Delhi Hutch":[@delhi.hutch.co.in],\
                "Digi-Page / Page Kansas":[@page.hit.net],\
                "Dobson Cellular Systems":[@mobile.dobson.net],\
                "Dobson-Alex Wireless / Dobson-Cellular One":[@mobile.cellularone.com],\
                "DT T-Mobile":[@t-mobile-sms.de],\
                "Dutchtone / Orange-NL":[@sms.orange.nl],\
                "Edge Wireless":[@sms.edgewireless.com],\
                "EMT":[@sms.emt.ee],\
                "Escotel":[@escotelmobile.com],\
                "Fido":[@fido.ca],\
                "GCS Paging":[@webpager.us],\
                "Goa BPLMobil":[@bplmobile.com],\
                "Google Project Fi":[@msg.fi.google.com],\
                "Golden Telecom":[@sms.goldentele.com],\
                "GrayLink / Porta-Phone":[@epage.porta-phone.com],\
                "GTE":[@airmessage.net,\ @gte.pagegate.net,\ @messagealert.com],\
                "Gujarat Celforce":[@celforce.com],\
                "Houston Cellular":[@text.houstoncellular.net],\
                "Idea Cellular":[@ideacellular.net],\
                "Inland Cellular Telephone":[@inlandlink.com],\
                "Kerala Escotel":[@escotelmobile.com],\
                "Kolkata Airtel":[@airtelkol.com],\
                "Kyivstar":[@smsmail.lmt.lv],\
                "Lauttamus Communication":[@e-page.net],\
                "LMT":[@smsmail.lmt.lv],\
                "Maharashtra BPL Mobile":[@bplmobile.com],\
                "Maharashtra Idea Cellular":[@ideacellular.net],\
                "Manitoba Telecom Systems":[@text.mtsmobility.com],\
                "MCI Phone":[@mci.com],\
                "MCI":[@pagemci.com],\
                "Meteor":[@mymeteor.ie,\ @sms.mymeteor.ie],\
                "Metrocall":[@page.metrocall.com],\
                "Metrocall 2-way":[@my2way.com],\
                "Metro PCS":[@mymetropcs.com,\ @metropcs.sms.us],\
                "Microcell":[@fido.ca],\
                "Midwest Wireless":[@clearlydigital.com],\
                "MiWorld":[@m1.com.sg],\
                "Mobilecom PA":[@page.mobilcom.net],\
                "Mobilecomm":[@mobilecomm.net],\
                "Mobileone":[@m1.com.sg],\
                "Mobilfone":[@page.mobilfone.com],\
                "Mobility Bermuda":[@ml.bm],\
                "Mobistar Belgium":[@mobistar.be],\
                "Mobitel Tanzania":[@sms.co.tz],\
                "Mobtel Srbija":[@mobtel.co.yu],\
                "Morris Wireless":[@beepone.net],\
                "Motient":[@isp.com],\
                "Movistar":[@correo.movistar.net],\
                "Mumbai BPL Mobile":[@bplmobile.com],\
                "Mumbai Orange":[@orangemail.co.in],\
                "NBTel":[@wirefree.informe.ca],\
                "Netcom":[@sms.netcom.no],\
                "Nextel":[@messaging.nextel.com,\ @page.nextel.com,\ @nextel.com.br],\
                "NPI Wireless":[@npiwireless.com],\
                "Ntelos":[@pcs.ntelos.com],\
                "O2 (M-mail)":[@mmail.co.uk],\
                "Omnipoint":[@omnipoint.com,\ @omnipointpcs.com],\
                "One Connect Austria":[@onemail.at],\
                "OnlineBeep":[@onlinebeep.net],\
                "Optus Mobile":[@optusmobile.com.au],\
                "Orange":[@orange.net],\
                "Orange Mumbai":[@orangemail.co.in],\
                "Orange – NL / Dutchtone":[@sms.orange.nl],\
                "Oskar":[@mujoskar.cz],\
                "P&T Luxembourg":[@sms.luxgsm.lu],\
                "Pacific Bell":[@pacbellpcs.net],\
                "PageMart Advanced /2way":[@airmessage.net],\
                "PageMart Canada":[@pmcl.net],\
                "PageNet Canada":[@pagegate.pagenet.ca],\
                "PageOne NorthWest":[@page1nw.com],\
                "PCS One":[@pcsone.net],\
                "Pioneer / Enid Cellular":[@msg.pioneerenidcellular.com],\
                "PlusGSM":[@text.plusgsm.pl],\
                "Pondicherry BPL Mobile":[@bplmobile.com],\
                "Powertel":[@voicestream.net],\
                "Price Communications":[@mobilecell1se.com],\
                "Primco":[@primeco@textmsg.com],\
                "Primtel":[@sms.primtel.ru],\
                "Public Service Cellular":[@sms.pscel.com],\
                "Qwest":[@qwestmp.com],\
                "RAM Page":[@ram-page.com],\
                "Rogers":[@pcs.rogers.com,\ @sms.rogers.com],\
                "Safaricom":[@safaricomsms.com],\
                "Satelindo GSM":[@satelindogsm.com],\
                "Satellink":.pageme[@satellink.net],\
                "SBC Ameritech Paging":[@paging.acswireless.com],\
                "SCS-900":[@scs-900.ru],\
                "SFR France":[@sfr.fr],\
                "Simple Freedom":[@text.simplefreedom.net],\
                "Smart Telecom":[@mysmart.mymobile.ph],\
                "Southern LINC":[@page.southernlinc.com],\
                "Southwestern Bell":[@email.swbw.com],\
                "Sprint":[@sprintpaging.com],\
                "Sprint PCS":[@messaging.sprintpcs.com],\
                "SunCom":[@tms.suncom.com,\ @suncom1.com],\
                "Sunrise Mobile":[@mysunrise.ch,\ @freesurf.ch],\
                "Surewest Communications":[@mobile.surewest.com],\
                "Swisscom":[@bluewin.ch],\
                "T-Mobile":[@tmomail.net,\ @voicestream.net],\
                "T-Mobile Austria":[@sms.t-mobile.at],\
                "T-Mobile Germany":[@t-d1-sms.de],\
                "T-Mobile UK":[@t-mobile.uk.net],\
                "Tamil Nadu BPL Mobile":[@bplmobile.com],\
                "Tele2 Latvia":[@sms.tele2.lv],\
                "Telefonica Movistar":[@movistar.net],\
                "Telenor":[@mobilpost.no],\
                "Teletouch":[@pageme.teletouch.com],\
                "Telia Denmark":[@gsm1800.telia.dk],\
                "Telus":[@msg.telus.com],\
                "TIM":[@timnet.com],\
                "Triton":[@tms.suncom.com],\
                "TSR Wireless":[@alphame.com,\ @beep.com],\
                "UMC":[@sms.umc.com.ua],\
                "Unicel":[@utext.com],\
                "Uraltel":[@sms.uraltel.ru],\
                "US Cellular":[@email.uscc.net],\
                "US Cellular":[@uscc.textmsg.com],\
                "US West":[@uswestdatamail.com],\
                "Uttar Pradesh Escotel":[@escotelmobile.com],\
                "Verizon Pagers":[@myairmail.com],\
                "Verizon PCS":[@vtext.com,\ @myvzw.com],\
                "Vessotel":[@pager.irkutsk.ru],\
                "Virgin Mobile":[@vmobl.com,\ @vxtras.com],\
                "Vodafone Italy":[@sms.vodafone.it],\
                "Vodafone Japan":[@c.vodafone.ne.jp,\ @h.vodafone.ne.jp,\ @t.vodafone.ne.jp],\
                "Vodafone Spain":[@vodafone.es],\
                "VoiceStream / T-Mobile":[@voicestream.net],\
                "WebLink Wiereless":[@airmessage.net,\ @pagemart.net],\
                "West Central Wireless":[@sms.wcc.net],\
                "Western Wireless":[@cellularonewest.com],\
                "Wyndtell":[@wyndtell.com],\
                }

            #a menu for selecting the mobile carrier (US Specific)

            def menu():
                print(30 * "-", "MOBILE CARRIER" , 30 * "-")
                print("1.  Verizon")
                print("2.  T-Mobile")
                print("3.  AT&T")
                print("4.  Sprint")
                print("5.  Boost Mobile")
                print("6.  Cricket")
                print("6.  Cricket")
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
                collectedNumbers[mynumber] = "Verizon"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "vtext.com"
            elif selection == '2':
                print("T-Mobile")
                collectedNumbers[mynumber] = "T-Mobile"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "tmomail.net"
            elif selection == '3':
                print("AT&T")
                collectedNumbers[mynumber] = "AT&T"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "txt.att.net"
            elif selection == '4':
                print("Sprint")
                collectedNumbers[mynumber] = "Sprint"
                if shallDefault == "Y" or shallDefault == "y":
                     SMSEmailSuffix = "messaging.sprintpcs.com"               
            elif selection == '5':
                print("Boost Mobile")
                collectedNumbers[mynumber] = "Boost Mobile"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "myboostmobile.com"            
            elif selection == '6':
                print("Cricket")
                collectedNumbers[mynumber] = "Cricket"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "sms.mycricket.com" 
            elif selection == '7':
                print("Metro PCS")
                collectedNumbers[mynumber] = "Metro PCS"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "mymetropcs.com" 
            elif selection == '8':
                print("Tracfone")
                collectedNumbers[mynumber] = "Tracfone"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "mmst5.tracfone.com" 
            elif selection == '9':
                print("US Cellular")
                collectedNumbers[mynumber] = "US Cellular"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "email.uscc.net" 
            elif selection == '10':
                print("Virgin Mobile")
                collectedNumbers[mynumber] = "Virgin Mobile"
                if shallDefault == "Y" or shallDefault == "y":
                    SMSEmailSuffix = "vmobl.com" 
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
           
        #continue gathering necessary information
        
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
        print("If necessary, we will now open a browser to autohorize our use of your Google contacts for matching names to numbers, but if you have authenticated using the script before, it likely won't be and this stage will just flash by with no intervention needed from the user...")
        time.sleep(1)
        #call the Google People API to get contact names and phone numbers and store them as a dict.
        
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            
            # If there are no (valid) credentials available, let the user log in.
    
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
        # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('people', 'v1', credentials=creds)
        print("Great! Now please wait just a moment while we parse your contact data...")
        #get their google contact names and numbers

        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,phoneNumbers').execute()
        connections = results.get('connections', [])
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("...")
        
        parsedGoogleContacts = {}    
        for person in connections:
            names = person.get('names', [])
            if names:
                nameFromGoogle = names[0].get('displayName')
            contactNumbers =  person.get('phoneNumbers',[])
            for number in contactNumbers: 
                def extract_values(obj, key):
                    """Pull all values of specified key from nested JSON."""
                    arr = []
                    def extract(obj, arr, key):
                        """Recursively search for values of key in JSON tree."""
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if isinstance(v, (dict, list)):
                                    extract(v, arr, key)
                                elif k == key:
                                    arr.append(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                extract(item, arr, key)
                        return arr
                    results = extract(obj, arr, key)
                    return results
                    canonicalNumber = extract_values('contactNumbers', 'canonicalForm')
                    stringifiedCanonicalNumber = str(canonicalNumber)
                    strippedCanonicalNumber = stringifiedCanonicalNumber.strip('+1')
                    parsedGoogleContacts[nameFromGoogle] = strippedCanonicalNumber
                    print(parsedGoogleContacts[nameFromGoogle])
            

            
        print((3 * "\r\n") + "Great. The script has sucessfully processed your Google Contacts for the needed data.\r\n\r\n\r\nThis script offers the ability to have all of the numbers for your contacts checked against numverify (a commercial phone number validation API) . Thee advantage of this is having the correct carrier information and therefore the correct SMS email addresses for all of your contacts and messages.\r\n\r\nThis is --not-- free.\r\n\r\nAgain:\rn\r\n\r\n this is not free.\r\n\r\n\r\nnumverify allows up to 250 API calls a month for free but beyond that you are going to need to go to numverify.com and sign up for an API key and set-up billing. 5000 calls per month is ten bucks and that is more than adequate for addressing most people's SMS needs. \r\n\r\n")
        numverifyOrNot = input("Would you like to use the numverify service to get the carrier data for each of your contacts? (Y/N) ")
        if numverifyOrNot == "Y" or numverifyOrNot == "y":
            numverifyAPIkey = input("\r\n\r\n\r\nPlease enter your numverify API key: ")
        else:
            pass
        print("\r\n\r\nAwesome.\r\n...Now the real work begins. The script will now parse your sms backupfile, match the necessary data, write the email headers and create the mbox file.")
        time.sleep(2)
        print("\r\n\r\nIt slices...")
        time.sleep(1)
        print("\r\n\r\nIt dices...")
        time.sleep(1)
        print("\r\n\r\nIt circumcises...")
        time.sleep(2)
        print("   ...")
        time.sleep(1)
        print("...igotnothin'.\r\n\r\nAnnnnnnnnnnnnyhow... hold on, this could take a while, depending on the number of messages being processed." + (2 * "\r\n"))
    
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
                
            #format the phone number into something we can work with
                
            rawNumber = i.getAttribute("address")
            if "+" in rawNumber:
                strippedNumber = rawNumber.strip('+1')
            else:
                strippedNumber = rawNumber
            mobileCarrier = "unknown"
            if numverifyOrNot == "Y" or numverifyOrNot == "y": 
                url = 'http://apilayer.net/api/validate?access_key=' + numverifyAPIkey + '&number=1' + strippedNumber
                response = requests.get(url)
                numverifyData = json.loads(response.text)
                if numverifyData['valid'] == "false":
                    mobileCarrier = "unknown"
                else:    
                    try:
                        mobileCarrier = numverifyData['carrier']
                    except:
                        mobileCarrier = "unknown"
            try:            
                gContactName = parsedGoogleContacts['strippedNumber']
            except:
                gContactName = i.getAttribute("contact_name")

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
                
                if i.getAttribute("type") == 1 :
                    file.write(gContactName +" <" + SMSemailAddress + ">" + "\r\nTo: " + myname + " <" + defaultNumber  + "@" + SMSEmailSuffix + ">\r\n")

                else:
                    file.write(myname + " <" + defaultNumber + "@" + SMSEmailSuffix + ">\r\nTo: " + gContactName + " <" + SMSemailAddress + ">\r\n")
                    file.write("Subject: [SMS] ")
                    file.write(i.getAttribute("body") + "\r\nX-SMS: true\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n")
                    file.write(i.getAttribute("body"))
                    file.close()
                    
                    #reopen the file and add it to the mbox now that it is complete

                    with open(filepath, "rb") as file:
                        dest_mbox.lock()
                        dest_mbox.add(file)
                        dest_mbox.flush()
                        dest_mbox.unlock()
                        stdout.write('Number of SMS files Processed: %s \r' % (smscounter))
        stdout.flush();
        print(2 * "\r\n")       
            
        print("************************************\r\n***********************************\r\nProcessing of the SMS backup file is complete. Find the eml files in the sms directory or they are all included in the mbox file just created with the name of your choosing.") 
    
main()
                            
    
                        
