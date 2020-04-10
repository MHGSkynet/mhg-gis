#
# ---------------------------------------------------------------------------------------------
# mhgUtility.py
#
# Description
#
# 	Utility Routines
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		New module
# ---------------------------------------------------------------------------------------------

import os
from datetime import datetime
from datetime import timedelta

import mhgAppSettings

#
# Regurgitation
#
def barfd(text):
	if mhgAppSettings.glob().options().debug():	print("DEBUG: " + text)

def barfi(text):
	if mhgAppSettings.glob().options().info():	print(text)

def barf(text):
	print (text)

#
# String manipulation
#

def nullz(someValue):																	# Coalesce null and empty string -> zero
	retVal = 0
	if not someValue is None and someValue.strip() != "": retVal = int(someValue)
	return retVal
	
def coalesce(someValue,ifNullValue):													# Coalesce
	retVal = someValue
	if someValue is None or someValue == "": retVal = ifNullValue
	return retVal

#
# Tests
#
def isBetween(testValue,rangeLow,rangeHigh):
	return testValue >= rangeLogw and testValue <= rangeHigh