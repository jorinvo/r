import argparse
import sys

default_abc = 'abcdefghijklmnopqrstuvwxyz '

def main():
    # Parse ars
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'abc',
        type=str,
        help=''
    )
    args = parser.parse_args()
    abc = args.abc

    # Validate alphabet
    if sorted(abc) != default_abc:
        print('abc has wrong length, illegal characters or duplicates', file=sys.stderr)
        exit(1)

    substitutions = dict(zip(default_abc, abc))
    substitutions['\n'] = ''

    for line in sys.stdin:
        print(''.join(substitutions[c] for c in line))


if __name__ == "__main__":
    main()