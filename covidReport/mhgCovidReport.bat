@echo off
::
:: ---------------------------------------------------------------------------------------------
:: mhgCovidReport.bat
::
:: Description
::
::     Batch file to run mhgCovidStatus.py QGIS python
:: 
:: Usage
::     mhgCovidStatus.bat [date]
::  
::
:: Copyright
::
::	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
::						non profit conservative organizations and individuals to use in support
::						of American freedom and the constitution. All other rights are reserved,
::						and any other use prohibited.
::
:: Date        Version     Author          Description
:: 2020.04.04  01.02       SquintMHG       Fix to handle folders with space in name
:: 2020.03.26  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

:: echo mhgCovidReport running...

if "%MHGGIS_ROOT%"=="" (
	echo "ERROR MHGGIS_ROOT environment variable not defined. Run mhgCovidEnv.bat"
	exit 1
)

set MHGGIS_REPORT_FOLDER=%MHGGIS_ROOT%\covidReport

"%MHGGIS_REPORT_FOLDER%\python-qgis-headless.bat" "%MHGGIS_REPORT_FOLDER%\mhgCovidReport.py" %*