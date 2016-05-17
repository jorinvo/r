function alphabetSoup (str) {
  return str.split(' ').map(function (word) {
    var parts = word.substr(1, word.length - 2).split('')
      .sort(function () { return Math.random() })
      .join('')
    return word[0] + parts + word[word.length - 1]
  }).join(' ')
}

alphabetSoup('Hello World!') // "Hlleo Wdlro!"

function rollercaster (str) {
  return str.split('').map(function (char, i) {
    return i % 2 ? char.toLowerCase() : char.toUpperCase()
  }).join('')
}

rollercaster('Hello World!') // "HeLlO WoRlD!"
