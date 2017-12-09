const axios = require('axios')

const n = parseInt(process.argv[2], 10);
const url = 'http://localhost:3000'

const run = async () => {
  console.time('bench')

  await Promise.all([...Array(n)].map(() =>
    axios.post(url, { data: "test" })
  ))

  console.timeEnd('bench')
}

run()
