const zmq = require('zeromq')
const uuid = require('uuid/v4')

const n = parseInt(process.argv[2], 10);

const requester = zmq.socket('dealer')
const handlers = {}
requester.on('message', (id, msg) => {
  handlers[id](msg.toString())
  delete handlers[id]
})
const send = msg => new Promise(done => {
  const id = uuid()
  handlers[id] = done
  requester.send([id, msg])
})
const transport = 'tcp://localhost:3000' // or 'ipc://bench.ipc'
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