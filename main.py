#!/usr/bin/python3

from serve import serve


def main():
    serve()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nTerminated")
    finally:
        exit(0)
