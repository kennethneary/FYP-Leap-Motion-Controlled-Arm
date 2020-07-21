#! /bin/bash
# Starting IP script...
y=$(hostname -I | sed 's/ *$//g')
echo -n "Current IP address of Pi: " > /home/pi/dropbox/ifconfig.txt
echo "$y " >> /home/pi/dropbox/ifconfig.txt
echo "To access the Webpage go to $y:3000 " >> /home/pi/dropbox/ifconfig.txt
echo "To share this App with another Dropbox account go to: https://www.dropbox.com/1/oauth2/authorize?response_type=code&client_id=pnfb2ynygibs8nu " >> /home/pi/dropbox/ifconfig.txt
# Genertaed file ifconfig.txt
# IP address saved in ifconfig.txt
