@echo off
::
::
:: Usage:
::
::    mhgCovidStatus.py [-h] [--start START] [--end END] [--ndays [NDAYS]] [--nodetail] [--nosummary]
::                         [--noproject] [--nopdf] [--noimage] [--info] [--debug] [--zombies]
::
::     === MHG Covid Status Report ===
::
::     optional arguments:
::       -h, --help       show this help message and exit
::       --start START    Beginning date of range to select data by
::       --end END        End date of range to select data by
::       --ndays [NDAYS]  Number of days from begin date to select data by
::       --nodetail       Disables capture of detail to daily CSV files
::       --nosummary      Disables generation of summary info CSV file
::       --noproject      Disables saving of GIS Project
::       --nopdf          Disables saving of PDF file
::       --noimage        Disables saving of JPG image
::       --info           Whether to barf progress info
::       --debug          Whether to barf debug info
::       --zombies        Whether to enable zombies
::
::     Note:
::             dates may be entered mm/dd, mm/dd/yyyy or yyyy.mm.dd
::             nDays may be positive or negative.
::
::     Examples:
::             mhgCovidStatus.bat                                  # Run for today
::             mhgCovidStatus.bat --start 2020.04.03               # Run for specific date
::             mhgCovidStatus.bat --start 04/03 --end 04/06        # Run for a date range
::             mhgCovidStatus.bat --start 04/03 --ndays 7          # Run for week following start date given
::             mhgCovidStatus.bat --start 04/03/2020 --ndays -7    # Run for week prior to and including start date given
::             mhgCovidStatus.bat --ndays -7                       # Run for the past week# Description
::
:: Copyright
::
::	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
::						non profit conservative organizations and individuals to use in support
::						of American freedom and the constitution. All other rights are reserved,
::						and any other use prohibited.
::  
:: Date        Version     Author          Description
:: 2020.04.06  02.00       SquintMHG       App rewrite, add command line arguments, etc
:: 2020.04.04  01.02       SquintMHG       Fix folders with spaces
:: 2020.03.26  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

@echo off
:: echo mhgCovidFetch running...

call mhgCovidEnv.bat

if "%MHGGIS_ROOT%"=="" (
	echo "mhgCovidFetch.bat.ERROR: MHGGIS_ROOT environment variable not defined. Fix mhgCovidEnv.bat"
	exit 1
)

::
::  Status Report python application location
::
set MHGSTATUS_APP=%MHGGIS_ROOT%\covidStatus\mhgCovidStatus.py

::
::  Whether to run headless or with GUI.  Parse P1 for GUI switch, and leech it off of parameters list if there
::
set HEADLESS=Y
set p1=%1
set p1Stripped=%p1:"=%
if "%p1Stripped%"=="--GUI" (set HEADLESS="" & shift)
if "%p1Stripped%"=="--gui" (set HEADLESS="" & shift)

:: Save Environment
set OLD_PATH=%PATH%
set OLD_PYTHONBIN=%PYTHONBIN%
set OLD_PYTHONEXE=%PYTHONEXE%
set OLD_PYTHONHOME=%PYTHONHOME%
set OLD_PYTHONPATH=%PYTHONPATH%

::  QGIS is pissy and kerplodes when paths have spaces. Convert to short path
for /d %%I in ("%MHGGIS_QGIS_ROOT%") do set MHGGIS_QGIS_ROOT=%%~sI

::
::  QGIS Environment vars
::
@echo off
call %MHGGIS_QGIS_ROOT%\bin\o4w_env.bat
call %MHGGIS_QGIS_ROOT%\bin\qt5_env.bat
call %MHGGIS_QGIS_ROOT%\bin\py3_env.bat
@echo off

::
::  Add QGIS application folders to PATH
::
path %OSGEO4W_ROOT%\apps\qgis-ltr\bin;%PATH%

::
::  QGIS Settings vars
::
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr
set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set GDAL_FILENAME_IS_UTF8=YES

:: Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000

::
::  Let python know about QGIS libraries
::
@echo off

:: set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins;%PYTHONPATH%
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%PYTHONPATH%

set PYTHONPATH=%PYTHONPATH%;C:\Users\booger\AppData\Local\Programs\Python\Python38-32\Lib\site-packages
set PYTHONPATH=%PYTHONPATH:\=/%

::echo PYTHONPATH=%PYTHONPATH%
::echo PYTHONHOME=%PYTHONHOME%
::echo PATH=%PATH%

::
::  Python Installation (the one that came with QGIS)
::
:::: set PYTHONBIN=%OSGEO4W_ROOT%\apps\Python37
:::: set PYTHONEXE=%PYTHONBIN%\python

::
::  Run script
::
::
if "%HEADLESS%" == "Y" (
	::echo HEADLESS RUN...
	python %MHGSTATUS_APP% %*
) else (
	rem QGIS
	start "QGIS" /B "%OSGEO4W_ROOT%\bin\qgis-ltr-bin.exe" "%MHGSTATUS_APP%" %*
	set xx=0
)

:: Restore Environment
set PATH=%OLD_PATH%
set PYTHONBIN=%OLD_PYTHONBIN%
set PYTHONEXE=%OLD_PYTHONEXE%
set PYTHONHOME=%OLD_PYTHONHOME%
set PYTHONPATH=%OLD_PYTHONPATH%
set OLD_PATH=
set OLD_PYTHONBIN=
set OLD_PYTHONEXE=
set OLD_PYTHONHOME=
set OLD_PYTHONPATH=

exit /B 