import http.client
from dotenv import load_dotenv
import os

#pulling API key from .env file
load_dotenv()

#assigning API key to local variable
API_KEY = os.environ['API_KEY']

conn = http.client.HTTPSConnection("api.themoviedb.org")

#passing API key 
headers = {'Authorization': f"Bearer {API_KEY}"}

#pulling no other choice as an example for now
conn.request("GET", "/3/search/movie?query=No%20Other%20Choice", headers=headers)

res = conn.getresponse()
data = res.read()

#print response
print(data.decode("utf-8"))