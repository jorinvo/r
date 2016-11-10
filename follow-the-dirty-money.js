var got = require('got')

var start = 'https://gist.githubusercontent.com/jorinvo/6f68380dd07e5db3cf5fd48b2465bb04/raw/c02b1e0b45ecb2e54b36e4410d0631a66d474323/fd0d929f-966f-4d1a-89cd-feee5a1c5347.json'
var visited = new Set()

var getTotal = (url) => got(url, { json: true }).then((res) => {
  var transaction = res.body
  if (visited.has(transaction.id)) return 0
  visited.add(transaction.id)
  var match = transaction.content.match(/\$[0-9,.]+/)
  if (!match) return 0
  var dollar = parseFloat(match[0].replace(/(^\$)|([.,]$)/, '').replace(',', '.'), 10)
  return Promise.all(transaction['links'].map((link) => getTotal(link)))
    .then((results) => results.reduce((a, b) => a + b, dollar))
})

getTotal(start).then((total) => {
  var pretty = Math.round(total * 100) / 100
  console.log(`transactions: ${visited.size}, total: $${pretty}`)
})

