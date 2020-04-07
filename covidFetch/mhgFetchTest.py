#
# ---------------------------------------------------------------------------------------------
# mhgFetchTest.py
#
# Description
#
# 	Test Stuff
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.05	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys
from datetime import datetime

from mhgFetchCommandArgs import mhgFetchCommandArgs
from mhgFetchEnvironment import getPackageRoot

PACKAGE_NAME			= "mhgCovidStatus.bat"
PROGRAM_NAME			= "mhgFetchCommandArgs.py"

"""
##########################################
		INITIALIZATION
##########################################
"""

# System date
currTimestamp			= datetime.now() 												# current date and time (timestamp)
currDateYmd				= currTimestamp.strftime("%Y.%m.%d")							# current date YYYY.MM.DD (text)
currDateTS				= datetime.strptime(currDateYmd,"%Y.%m.%d")						# current date (timestamp)

print("####command arguments...")
print(sys.argv)

print("####Parsed args...")
myArgs = mhgFetchCommandArgs()
success = myArgs.getArguments()
print("Success={}".format(success))	
print("StartDate={}".format(myArgs.startDate()))
print("StartEndDate={}".format(myArgs.endDate()))
print("NDays={}".format(myArgs.nDays()))
print("CaptureDetail={}".format(myArgs.captureDetail()))
print("Debug={}".format(myArgs.debug()))

print("### Package Root Test ####")
myRoot = getPackageRoot()
print(myRoot)

	

