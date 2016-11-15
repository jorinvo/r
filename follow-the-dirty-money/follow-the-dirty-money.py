import requests
import re

start = 'https://gist.githubusercontent.com/jorinvo/6f68380dd07e5db3cf5fd48b2465bb04/raw/c02b1e0b45ecb2e54b36e4410d0631a66d474323/fd0d929f-966f-4d1a-89cd-feee5a1c5347.json'
visited = set()
total = 0
urls = [start]

while len(urls) > 0:
    transaction = requests.get(urls.pop()).json()
    if transaction['id'] in visited:
        continue
    visited.add(transaction['id'])
    match = re.search('\$[0-9,.]+', transaction['content'])
    if not match:
        continue
    total += float(match.group(0).strip('$.,').replace(',', '.'))
    urls.extend(transaction['links'])

print('transactions: {}, total: ${:.2f}'.format(len(visited), total))