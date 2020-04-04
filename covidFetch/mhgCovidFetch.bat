@echo off
::
:: ---------------------------------------------------------------------------------------------
:: mhgCovidFetch.bat
::
:: Description
::
::     Batch file to run mhgCovidDataFetch.py application 
:: 
:: Usage
::     mhgCovidFetch.bat [filter-date]
::
::		filter-date			Date to retrieve data for (yyyy.mm.dd format), default=today.
::
:: Copyright
::
::	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
::						non profit conservative organizations and individuals to use in support
::						of American freedom and the constitution. All other rights are reserved,
::						and any other use prohibited.
::  
:: Date        Version     Author          Description
:: 2020.04.04  01.02       SquintMHG       Fix folders with spaces
:: 2020.03.26  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

:: echo mhgCovidFetch running...

if "%MHGGIS_ROOT%"=="" (
	echo "mhgCovidFetch.bat.ERROR: MHGGIS_ROOT environment variable not defined. Run mhgCovidEnv.bat"
	exit 1
)

if not "%1" == "" (
	set MHGGIS_FILTER_DATE=%1
)

python "%MHGGIS_ROOT%\covidFetch\mhgCovidDataFetch.py"

exit /B %ERRORLEVEL%