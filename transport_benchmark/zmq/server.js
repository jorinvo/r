const zmq = require('zeromq')

let x = 0

const socket = zmq.socket('router')

const transport = 'tcp://*:3000' // or 'ipc://bench.ipc'
socket.bindSync(transport)

socket.on('message', (...args) => {
  x++
  socket.send([args[0], args[1], JSON.stringify({ data: x })])
})
