#!/usr/bin/python3

from __future__ import annotations


class IPRange:
    '''
        Holds start and end values of an IPv4 address range,
        which is allocated to a certain country

        Faciliates follwing queries

            - `x in IPRange`, where x is a +ve integer
            - `x < IPRange`
            - `x > IPRange`

        These queries will be helpful while seaching 
        for IPRange where a certain IP adrress belongs to, 
        in `ip2country` module
    '''

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __contains__(self, v: int):
        return v >= self.start and v <= self.end

    def __lt__(self, v: int):
        return v > self.end

    def __gt__(self, v: int):
        return v < self.start


if __name__ == '__main__':
    print("This module isn't supposed to be used this way")
