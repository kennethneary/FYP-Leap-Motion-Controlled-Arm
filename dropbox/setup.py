# Include the Dropbox SDK
import dropbox

# Get your app key and secret from the Dropbox developer website
app_key = 'pnfb2ynygibs8nu'
app_secret = '35bgg6mixv1l2v1'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
# Have the user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()
# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)

# Write access_token to a file
f = open('/home/pi/dropbox/access_token', 'w') 
f.write(access_token)
f.close()
