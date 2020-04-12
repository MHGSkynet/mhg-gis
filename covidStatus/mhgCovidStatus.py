#
# ---------------------------------------------------------------------------------------------
# mhgCovidStatus.py                         .
#                                        ,'/ \`.                      :   <">    I am a virus,
# Description                           |\/___\/|                     :   _T_    please copy me. 
#                                       \'\   /`/                     :   /Y\ 
#    Covid Status Reporting              `.\ /,'                                                   
#    Tool                                   |                                                    
#                                           |                                                      
#                                          |=|                                                    
#                                     /\  ,|=|.  /\                                                
#                                 ,'`.  \/ |=| \/  ,'`.                                           
#                               ,'    `.|\ `-' /|,'    `.                                        
#                             ,'   .-._ \ `---' / _,-.   `.                                        
#                                ,'    `-`-._,-'-'    `.
#                               '                       `
#                             
#                    
# Description
#
#	Get data from spreadsheet and render as chart. 	
#
#	Sample Spreadsheet:
#   	https://docs.google.com/spreadsheets/d/1ckdKCNIB-5-KSUlV2ehW3KPARVlu_CC2npjsAHrml7Q/edit?usp=sharing
#
# Copyright
#
#	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
#						non profit conservative organizations and individuals to use in support
#						of American freedom and the constitution. All other rights are reserved,
#						and any other use prohibited.
#
# Date			Version		Author			Description
# 2020.04.07	02.00		SquintMHG		Rewrite from script to oo app
# 2020.04.04	01.01		SquintMHG		Fix filter date compare problem
# 2020.03.27	01.00		SquintMHG		Initial version
# ---------------------------------------------------------------------------------------------

import os
import sys

import mhgAppSettings
import mhgCovidDataReader
import mhgDetailWriter
import mhgKmlWriter
import mhgSummaryWriter
import mhgException
import mhgUtility

#
# Exit handler
#
def appExit(err=None):

	statusText = ''
	statusCode = AppError.ERR_NONE

	if not err is None:
		print(err.formattedText())
		statusCode = err.errorNumber()
		statusText = " Status={}".format(statusCode)

	print ("####\n#### {} complete.{}\n####".format(AppSettings.PROGNM,statusText))

	sys.exit(statusCode)

"""
##########################################
		MAIN
##########################################
"""
def main():

	# App Start
	print ("####\n#### {} starting.\n####".format(AppSettings.PROGNM))

	# Get Application settings (environment info and command args). Retain a reference to command arg options for convenience
	try:
		_appOptions = AppSettings.glob().options()
	except (CommandArgError, EnvironmentError) as err:
		appExit(err)

	# Get Corona data from spreadsheet
	dataReader = CovidDataReader()
	fetchOk = dataReader.FetchCoronaData():
	if not fetchOk: 
		appExit(UserError('No records retrieved from sheet.',AppError.ERR_FETCHFAIL))
		
	# Generate Output CSVs and KML from State County stats
	try:
		# Write Detail
		if _appOptions.captureDetail(): DetailWriter.WriteStatusRows(dataReader.covidSheet().statusRowsFiltered())
		
		# Write Summary
		if _appOptions.generateSummary(): SummaryWriter.WriteStateCountyStats(dataReader.stateData())

		# Write KML
		KmlWriter.WriteStateCountyStats(dataReader.stateData())

	except EnvironmentError as err:
		appExit(err)

	# Remojinate generated KML into QGIS Project, then barf to PDF and JPG
	try:
		gisWriter = GisWriter()														# Fire up GIS Writer
		gisWriter.GenerateProject()													# Create a GIS project base on generated KML
		if _appOptions.generateProject(): 	gisWriter.SaveProject()					# Save project, if needed.
		if _appOptions.generatePDF(): 		gisWriter.GeneratePdf()					# Write to PDF, if needed.
		if _appOptions.generateImage(): 	gisWriter.GenerateImage()				# Write to JPG image, if needed.
		gisWriter.Cleanup()															# Shut down GIS Writer

	except (RenderError,EnvironmentError) as err:
		appExit(err)

	# App Exit
	appExit()

if __name__ == '__main__':
	main()