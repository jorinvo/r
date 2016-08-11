#!/usr/bin/env node


// Login and logout on irccloud.com
//
// Prove of concept to stay connected with free account
// if run with a scheduled job

var Nightmare = require('nightmare')

var email = process.env.EMAIL
var pass = process.env.PASS

if (!email || !pass) {
  console.error('Set env vars EMAIL and PASS')
  process.exit(1)
}

Nightmare({ show: process.env.SHOW })
  .goto('https://irccloud.com')
  .type('#landingLogin .form [name=email]', email)
  .type('#landingLogin .form [name=password]', pass)
  .click('#landingLogin .form [type=submit]')
  .wait('#buffersContainer .memberList')
  .click('.accountMenu__button')
  .click('.accountMenu__signout-button')
  .wait('#landingLogin')
  .end()
  .catch(function (error) {
    console.error('Login failed:', error)
  })
