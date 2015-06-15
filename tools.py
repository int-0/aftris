#!/usr/bin/env python

# Implementation taken from PEP 0318
def singleton(unique_class):
    instances = {}
    def getinstance():
        if unique_class not in instances:
            instances[unique_class] = unique_class()
        return instances[unique_class]
    return getinstance
