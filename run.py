#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from scripts.error import LogException

if __name__ == '__main__':
	with LogException():
		from scripts.application import Application
		application = Application()
		application.run()
