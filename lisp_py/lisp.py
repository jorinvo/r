from library import library

def tokenize(lisp_str):
    return lisp_str.replace('(', ' ( ').replace(')', ' ) ').split()


def parenthesize(tokens, tree=[]):
    if not tokens:
        return tree.pop()
    token = tokens.pop(0)
    if token == '(':
        return parenthesize(tokens, tree + [parenthesize(tokens)])
    elif token == ')':
        return tree
    else:
        return parenthesize(tokens, tree + [categorize(token)])


def categorize(token):
    try:
        return ('lit', float(token))
    except:
        return ('id', token)



def interpret(val, context=None):
    if not context:
        return interpret(val, library)
    elif type(val) == list:
        l = [interpret(x, context) for x in val]
        if callable(l[0]):
            return l[0](*l[1:])
        else:
            return l
    elif val[0] == 'id':
        try:
            return context[val[1]]
        except KeyError as key:
            raise Exception('Function %s not in context' % (key))
    else:
        # lit
        return val[1]


if __name__ == '__main__':
    test_input = '''
    (
        (+ 1 7)
        (+ (2.5 4))
        (map square (1 2 3))
        1
        (first (
            (first ((square 3)))
            1
            (first (4 5))
        ))
        (if 1 10 20)
        (if (first (0 1)) 10 20)
    )
    '''
    tokens = tokenize(test_input)
    tree = parenthesize(tokens)
    print(interpret(tree))