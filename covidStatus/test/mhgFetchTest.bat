@echo off
::
:: ---------------------------------------------------------------------------------------------
:: mhgFetchTest.bat
::
:: Description
::
::     Test stuff
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
:: 2020.04.06  01.03       SquintMHG       Add command line arguments
:: 2020.04.04  01.02       SquintMHG       Fix folders with spaces
:: 2020.03.26  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

:: echo mhgCovidFetch running...

if "%MHGGIS_ROOT%"=="" (
	echo "mhgCovidFetch.bat.ERROR: MHGGIS_ROOT environment variable not defined. Run mhgCovidEnv.bat"
	exit 1
)

::
::  Let python know about QGIS libraries
::
set PYTHONPATH=%MHGGIS_ROOT%\covidFetch;%PYTHONPATH%

::  Set app name and title
::
set MHGGIS_APPALIAS=mhgCovidStatus.bat

python "%MHGGIS_ROOT%\covidFetch\mhgFetchTest.py" %*

exit /B %ERRORLEVEL%