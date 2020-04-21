#
# ---------------------------------------------------------------------------------------------
# mhgUtility.py
#
# Description
#
#   Utility Routines. Various grease to get the job done. 
#
#                                  |\_______________ (_____\\______________
#          o~=<   o~=<     HH======#H###############H#######################
#                                  ' ~""""""""""""""`##(_))#H\"""""Y########
#                                                  ))    \#H\       `"Y###
#                                                  "      }#H)
# Copyright
#
#   Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#                       non profit conservative organizations and individuals to use in support
#                       of American freedom and the constitution. All other rights are reserved,
#                       and any other use prohibited.
#
# Date          Version     Author          Description
# 2020.04.20    02.00       SquintMHG       New module
# ---------------------------------------------------------------------------------------------

# Python includes
import os
from datetime import datetime
from datetime import timedelta

# MHGLIB includes
from mhgAppSettings		import AppSettings

#
# Regurgitation
#
def barfi(text):
	if AppSettings.glob().options().infoEnabled():	print("INFO: " + text)

def barfd(text):
	if AppSettings.glob().options().debugEnabled():	print("DEBUG: " + text)

def barft(text):
	if AppSettings.glob().options().traceEnabled():	print("TRACE: " + text)

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
def isBetween(testValue,rangeLow,rangeHigh):											# Test betweenness 
	return testValue >= rangeLow and testValue <= rangeHigh