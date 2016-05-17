// JS version of code from Jim Weirichs Talk on Lambda Calculus (https://www.youtube.com/watch?v=FITJMJjASUs)

// Y Combinator
// makes the recursion
(function (improver) {
  return (function (gen) { return gen(gen) })(
    function (gen) {
      return improver(function (v) {
        return gen(gen)(v)
      })
    }
  )
})(
// this part is the condition for the factorial
function (partial) {
  return function (n) {
    return n === 0 ? 1 : n * partial(n - 1)
  }
}
// pass any number here to get its factorial
)(5)
