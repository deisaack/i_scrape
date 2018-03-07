import requests
from bs4 import BeautifulSoup
from lxml import html

session_requests = requests.session()

login_url = "https://bitbucket.org/account/signin/?next=/"
result = session_requests.get(login_url)

tree = result.text
soup = BeautifulSoup(tree, 'html.parser')
form = soup.find('form', {"class": "aui aid-form errors-below-inputs"})

csrf = form.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

payload = {
	"username": "deisaack@gmail.com",
	"password": "Jacktone1",
	"csrfmiddlewaretoken": csrf
}

result = session_requests.post(
	login_url,
	data = payload,
	headers = dict(referer=login_url)
)

page_soup=BeautifulSoup(result.text, 'html.parser')

