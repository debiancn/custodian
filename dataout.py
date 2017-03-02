#!/usr/bin/python3

import data_collector

if __name__ == "__main__":
    r = data_collector.parse_debrepo()
    for i in r:
        print(r[i].components)
