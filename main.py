#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Coder: indryanto
    Source By @rsmnarts
"""

from assets import *
from modules import *

def selectOption():
    print(MenuList)
    try:
        return int(input('Select Online Shop Name: '))
    except ValueError:
        write('Invalid input.', 'exit')
    except KeyboardInterrupt:
        write('\nExit by user interrupt.', 'exit')
    except Exception as e:
        write('Error ' + str(e), 'exit')


def main():
    print(Header)
    index = selectOption()
    try:
        if index == 1:
            shopeeScraper()
        elif index == 99:
            write('Exit by user', 'exit')
        else:
            write('Invalid input.', 'exit')
    except KeyboardInterrupt:
        write('Exit by user interrupt.', 'exit')
    except Exception as e:
        write('Error ' + str(e), 'exit')    

if __name__ == "__main__":
    main()
