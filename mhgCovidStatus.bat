@echo off
::
:: ---------------------------------------------------------------------------------------------
:: mhgCovidStatus.bat
::
:: Description
::
::     Batch file to run Covid data fetch and report
:: 
:: Usage
::     mhgCovidStatus.bat [filter-date]
::
::		filter-date			Date to retrieve data for (yyyy.mm.dd format), default=today.
::  
::
:: Date        Version     Author          Description
:: 2020.04.04  01.02       SquintMHG       Fix handling folders with embedded spaces
:: 2020.03.29  01.00       SquintMHG       Initial version
:: ---------------------------------------------------------------------------------------------

:: echo mhgCovidStatus running...

call mhgCovidEnv.bat
call "%MHGGIS_ROOT%\covidFetch\mhgCovidFetch.bat" %*

if %ERRORLEVEL% == 0 (
	call "%MHGGIS_ROOT%\covidReport\mhgCovidReport.bat"
)

