# Include the Dropbox SDK
import dropbox

# get access token to connect to dropbox app
f = open('/home/pi/dropbox/access_token', 'r')
access_token = f.read()

client = dropbox.client.DropboxClient(access_token)
#print 'linked account: ', client.account_info()

# upload ifconfig.txt to dropbox app
f = open('/home/pi/dropbox/ifconfig.txt')
response = client.put_file('/raspberryIpAddress.txt', f, True)
print "uploaded:", response
