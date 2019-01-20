#!/usr/bin/env python3
"""Service class"""
from abc import ABCMeta, abstractmethod

class Service:
    __meta__metaclass__ = ABCMeta

    @abstractmethod
    def get_list(self): pass

    