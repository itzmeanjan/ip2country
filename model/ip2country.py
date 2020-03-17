#!/usr/bin/python3

from __future__ import annotations
from typing import List
from model.iprange import IPRange
from math import nan, isnan
from ipaddress import IPv4Address


class IP2Country:
    '''
        Given a path to CSV file, holding IPv4 to country mapping
        it'll read that file, parse its content and build one object model
        so that querying one IPv4 address gets easier

        For storing records we'll use a dictionary of IPRange -> 'countrycode:countryname',
        it facilitates constant time lookup, but we'll require to search for which range our
        IP address belongs to, which can be searched for, using binary search in O(log n) time.
    '''

    def __init__(self):
        self.holder = {}

    def _attach(self, record: List[str]):
        '''
            Private method implementation, used for putting a key:value record into this object
        '''
        self.holder[IPRange(*[int(i.strip("\""), base=10) for i in record[:2]])
                    ] = ":".join([i.strip("\"") for i in record[2:]])

    @staticmethod
    def read(file: str) -> IP2Country:
        '''
            Use this method for get an instance of this class,
            it'll parse given CSV file & build object for faster look up ops
        '''
        ip2Country = IP2Country()
        with open(file, 'r') as fd:
            for record in fd.readlines():
                ip2Country._attach(record.strip("\n").split(","))
        return ip2Country

    def _bsearch(self, low: int, high: int, key: int, keys: List[IPRange]) -> int:
        '''
            Given a list of IPRange objects, which are assumed to be sorted ascendically
            we can find where a certain ip address ( integer version ) belongs to i.e. its index in 0(log n) time
            where n = number of ranges present in `keys` list
        '''
        if low > high:
            return nan
        elif low == high:
            if key in keys[low]:
                return low
            else:
                return nan
        else:
            mid = (low + high) // 2
            if key < keys[mid]:
                return self._bsearch(low, mid, key, keys)
            elif key in keys[mid]:
                return mid
            else:
                return self._bsearch(mid, high, key, keys)

    def _search(self, key: int) -> IPRange:
        '''
            Given an IPv4 address in its integer form
            we'll search which IPRange it belongs to

            In case of bad IP or record not found, returns None
        '''
        keys = list(self.holder.keys())
        idx = self._bsearch(0, len(keys)-1, key, keys)
        if isnan(idx):
            return None
        else:
            return keys[idx]

    def __getitem__(self, key: str) -> str:
        '''
            And this one supports period seperated IPv4 address based lookup
            for which we'll actually convert IPv4 address into its integer representation
        '''
        iprng = self._search(int(IPv4Address(key)))
        if iprng:
            return self.holder[iprng]
        else:
            return None


if __name__ == '__main__':
    print("This module isn't supposed to be used this way")
