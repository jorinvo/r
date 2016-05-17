class Library:

    @staticmethod
    def first(x):
        return x[0]

    @staticmethod
    def add(*x):
        if type(x[0]) == list:
            return sum(x[0])
        else:
            return sum(x)

    @staticmethod
    def max(*x):
        if type(x[0]) == list:
            return max(x[0])
        else:
            return max(x)

    @staticmethod
    def square(x):
        return x * x

    @staticmethod
    def map(fn, l):
        return [fn(x) for x in l]

    @staticmethod
    def ifelse(cond, then_val, else_val):
        if cond == 1:
            return then_val
        elif cond == 0:
            return else_val
        else:
            raise Exception('Non-boolean condition: %s' % (cond))


library = {
    'first': Library.first,
    '+': Library.add,
    'max': Library.max,
    'square': Library.square,
    'map': Library.map,
    'if': Library.ifelse
}
