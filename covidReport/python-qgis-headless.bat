@echo off
::
:: ---------------------------------------------------------------------------------------------
:: python-qgis-headless.bat
::
:: Description
::
::     Batch file to run QGIS python scripts
:: 
:: Usage
::		"c:\Program Files\QGIS 3.10\bin\python-qgis-headless.bat" [-H] someGisScript.py
::  
:: Copyright
::
::	Copyright (c) 2020 Kurt Schulte & Michigan Home Guard.  This software is freely available for
::						non profit conservative organizations and individuals to use in support
::						of American freedom and the constitution. All other rights are reserved,
::						and any other use prohibited.
::  
:: Date        Version     Author          Description
:: 2020.04.04  01.02       SquintMHG       Handle folders with spaces in name
:: 2020.03.26  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

::
::  Whether to run headless or with GUI
::
set HEADLESS=Y
set p1=%1
set p1Stripped=%p1:"=%
if "%p1Stripped%"=="-H" (set HEADLESS="" & shift)
if "%p1Stripped%"=="-h" (set HEADLESS="" & shift)

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
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;C:\Users\booger\AppData\Local\Programs\Python\Python38-32\Lib\site-packages

::
::  Python Installation (the one that came with QGIS)
::
set PYTHONBIN=%OSGEO4W_ROOT%\apps\Python37
set PYTHONEXE=%PYTHONBIN%\python

::echo PYTHONPATH=%PYTHONPATH%
::echo PYTHONHOME=%PYTHONHOME%
::echo PATH=%PATH%

::
::  Run script
::
@echo off 
if "%HEADLESS%" == "Y" (
	:: headless python script
	%PYTHONEXE% %*
) else (
	:: QGIS
	start "QGIS" /B "%OSGEO4W_ROOT%\bin\qgis-ltr-bin.exe" %*
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
