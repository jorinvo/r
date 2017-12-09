const zmq = require('zeromq')

const n = parseInt(process.argv[2], 10);

const requester = zmq.socket('dealer')
const handlers = {}
requester.on('message', (id, msg) => {
  handlers[id](msg.toString())
  delete handlers[id]
})
const send = msg => new Promise(done => {
  const id = Math.random().toString()
  handlers[id] = done
  requester.send([id, msg])
})
const transport = 'ipc://bench.ipc' // or 'tcp://localhost:3000'
requester.connect(transport)

const run = async () => {
  console.time('bench')

  await Promise.all([...Array(n)].map(() =>
    send(JSON.stringify({ data: "test" }))
  ))

  console.timeEnd('bench')

  requester.close()
  process.exit(0)
}

run()