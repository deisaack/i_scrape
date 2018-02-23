import requests
import json
import getpass

BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
USERNAME = 'pkemey'
PASSWD = getpass.getpass('Please enter your IG password')
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

session = requests.Session()
session.headers = {'user-agent': USER_AGENT}
session.headers.update({'Referer': BASE_URL})

req = session.get(BASE_URL)
session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
login_data = {'username': USERNAME, 'password': PASSWD}
login = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
cookies = login.cookies
login_text= json.loads(login.text)

print(login_text)





















