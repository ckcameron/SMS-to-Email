# SMS-to-Email
This Python 3 application parses and processes the backup output of the Android application "SMS Backup and Restore" by Carbonite. 

Run the application as you would a bash script:

./smsparse.py

...and then just follow the prompts.

Once the script is complete you will find a .mbox file with the name of your choosing in the current ddirectory and a directory called "sms" with .eml copies of each SMS found in the backup.

The script is a work in progress so ping me on github https://www.github.com/ckcameron/SMS-to-Email to report bugs and new features will be added,/improvements will be made  when I have the time. I establish no release timelines and I am not repsonsible for you giving yourself 50 million duplicate messsages if you import the output multiply.

##Dependencies

The script depends on the following modules being installed and available to Python:

xml.dom.minidom os io codecs mailbox email.utils datetime string sys time unicodedata

## Legal

This software is in no way supported by, and I am in no way affiliated with authors of the SMS Backup and Restore application. This script is to be used at your own risk. The software is provided with no warranty, whatsoever, including merchantability and is to be considered development software for evaluation and testing purposes only.

##Contact

Contact the sole author, CK Cameron, at chase@ckcameron.net . 


Paypal: chase@ckcameron.net 


LinkedIn: https://linkedin.com/in/interrobang
Keybase: https://www.keybase.io/ckcameron

