#!/usr/bin/python3

from .serve import serve


def main():
    try:
        serve()
    except KeyboardInterrupt:
        print("\nTerminated")
    finally:
        exit(0)


if __name__ == '__main__':
    main()
