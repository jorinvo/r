import requests
import re

url = 'https://gist.githubusercontent.com/jorinvo/6f68380dd07e5db3cf5fd48b2465bb04/raw/c02b1e0b45ecb2e54b36e4410d0631a66d474323/fd0d929f-966f-4d1a-89cd-feee5a1c5347.json'
visited = set()


def get_money(url):
    try:
        transaction = requests.get(url).json()
    except Exception:
        print('failed to get url')
        return 0
    if transaction['id'] in visited:
        return 0
    match = re.search('\$[0-9,.]+', transaction['content'])
    if not match:
        return 0
    dollar = float(match.group(0).strip('$.,').replace(',', '.'))
    visited.add(transaction['id'])
    return dollar + sum(get_money(link) for link in transaction['links'])


total = get_money(url)
print('transactions: {}, total: ${:.2f}'.format(len(visited), total))