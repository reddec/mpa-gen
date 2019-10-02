#!/usr/bin/env python3
import argparse
import os
from .gen import generate


def main():
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    parser = argparse.ArgumentParser(description='multi-page site generator')
    parser.add_argument('--dir', help='Root directory', default=os.getcwd())
    parser.add_argument('--method', help='HTTP method: GET or POST', default='GET')
    parser.add_argument('section', help='Section name (ex: user/messages)')
    parser.add_argument('name', help='Resource name (ex: dialog)')

    args = parser.parse_args()
    generate(args.name, args.section, location=args.dir, method=args.method, templates_dir=templates_dir)


if __name__ == '__main__':
    main()
