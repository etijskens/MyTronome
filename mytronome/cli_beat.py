# -*- coding: utf-8 -*-
"""Command line interface beat (no sub-commands)."""

import sys, argparse
sys.path.insert(0, '.')
from PyQt5 import QtWidgets

from mytronome import MyTronome

def main():
    parser = argparse.ArgumentParser(description='MyTronome, a simple metronome with a swing option.')
    parser.add_argument('-s','--start',action='store_true'
                       ,help='start automatically with default settings')
    args = parser.parse_args(sys.argv[1:])
#     print(args)

    app = QtWidgets.QApplication(sys.argv)
    ex = MyTronome(args.start)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
