#
# ---------------------------------------------------------------------------------------------
# mhgFetchException.py
#
# Description
#
# 	Application exception handlers
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.06	01.03		SquintMHG		New Module
# ---------------------------------------------------------------------------------------------

import sys

MODULE_NAME				= "mhgFetchException.py"

#
# EXCEPTIONS
#

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class EnvironmentError(Error):
    """Exception raised for errors in the environment configuration.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
		
