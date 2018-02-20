#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from scripts.error import LogException

if __name__ == '__main__':
	with LogException():
		from scripts.client import Client
		client = Client()
		client.run()
