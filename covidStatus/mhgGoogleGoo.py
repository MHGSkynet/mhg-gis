#
# ---------------------------------------------------------------------------------------------
# mhgGoogleGoo.py
#
# Description
#
# 	Stuff related to working with Google APIs
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	01.03		SquintMHG		New modu;s
# ---------------------------------------------------------------------------------------------

# Python includes
from __future__ import print_function
import os
import os.path
from pathlib import Path

# Google includes
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# MHGLIB Includes
import mhgAppSettings
import mhgUtility

#
#  GoogleGoo    Google Service Connection Class
#
class GoogleGoo:

	# Connection Constants (private)
	_SCOPES 						= ['https://www.googleapis.com/auth/spreadsheets.readonly']		# If modifying scope(s), delete the file token.pickle.

	# Spreadsheet data (private)
	_service						= None														# Google sheet service object

	# Constructor
	def __init__(self):
		pass

	#
	# Methods
	#
	def Login():

		# Goo Security
		gooPickleSpec		  	= mhgAppSettings.glob().googlePickleSpec()						# Google API pickle file
		gooCredentialsSpec		= mhgAppSettings.glob().googleCredentials()						# Google API credentials file

		# Security File Specs

		# Get pickle (session token) figured out.
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		creds = None
		if os.path.exists(gooPickleSpec):
			with open(gooPickleSpec, 'rb') as token:
				creds = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(gooCredentialsSpec, SCOPES)
				creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open(gooPickleSpec, 'wb') as token:
				pickle.dump(creds, token)

		# Connect to Google Sheets service
		self._service = build('sheets', 'v4', credentials=creds)
		return self._service

	#
	# Getters
	#
	def Service(self):
		return self._service
