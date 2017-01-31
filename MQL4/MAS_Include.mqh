#ifndef MAS_INCLUDE
    #define MAS_INCLUDE
#else
//+------------------------------------------------------------------+
//|                                                  MAS_Include.mqh |
//|                                 Copyright 2016, Terentew Aleksey |
//|                        https://www.mql5.com/ru/users/terentjew23 |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Terentew Aleksey"
#property link      "https://www.mql5.com/ru/users/terentjew23"
#property strict

//+------------------------------------------------------------------+
struct Forecast {
    int         Version;
    string      Copyright;
    string      SymbolF;
    int         PeriodF;
    int         DigitsF;
    datetime    StartTimeseries;
    datetime    EndTimeseries;
    int         DepthForecast;
};

//+------------------------------------------------------------------+
// Get the index of time
int GetIndexFromTime(datetime time, timeframe = _Period)
{
    int index = 0;
    while( iTime( _Symbol, timeframe, index ) >= time )
        index++;
    return index;
}

//+------------------------------------------------------------------+
// Get the index of the first bar of the month (2)
int GetIndexFirstBarMonth(int timeframe)
{
    int firstBar = 0;
    if( timeframe >= 10080 ) { // W1 & MN ( [count bar] )
        firstBar = 0; // 1 year
    } else if( timeframe >= 240 ) { // H4 & D1
        firstBar = 0; // 2 month
    } else if( timeframe < 240 ) {
        firstBar = 0; // 1 week ?
    }
    while( TimeMonth( iTime(_Symbol, timeframe, firstBar) ) == Month() ||
            TimeMonth( iTime(_Symbol, timeframe, firstBar) ) == 12 )
        firstBar++;
    return firstBar;
}

//+------------------------------------------------------------------+
//| Functions                                                        |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
void SetConfigs()
{
    onePeriod = false;
    periods[0] = 60;
    periods[1] = 240;
    periods[2] = 1440;
    // FileOpen ( FILE_SHARE_READ )
}

//+------------------------------------------------------------------+
bool NewBar()
{
    return false;
}

//+------------------------------------------------------------------+
bool NewForecast()
{
    return false;
}

//+------------------------------------------------------------------+
void SaveHistoryFiles(string[] fileList)
{
    
}

//+------------------------------------------------------------------+
void ReadForecastFile(string file)
{
    
}

//+------------------------------------------------------------------+
void WriteConfigFile(string configFile)
{
    
}

//+------------------------------------------------------------------+
void ReadConfigFile(string configFile)
{
    
}

//+------------------------------------------------------------------+
void OpenNewWindow(string outputSymbol)
{
    
}

//+------------------------------------------------------------------+
void UiUpdate()
{
    
}

//+------------------------------------------------------------------+
void CloseThisWindow()
{
    
}

//+------------------------------------------------------------------+
void SeparateMasSymbol(const string masSymbol, string &symbol, int &period)
{
    int[] periods = {PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1,
                        PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1};
    int idx = 0;
    while( StringFind( masSymbol, IntegerToString(periods[idx]), 0 ) < 0 ) {
        idx++;
        if( idx > 8 ) {
            idx = -1;
            break;
        }
    }
    if( idx >= 0 ) {
        symbol = masSymbol;
        StringReplace( symbol, IntegerToString(periods[idx]), "" );
        period = periods[idx];
    } else {
        symbol = "";
        period = -1;
    }
}

//+------------------------------------------------------------------+
void WriteHistoryFile()
{
    if( onePeriod )
        WriteMain( _Period );
    else
        for(int i = 0; i < 3; i++)
            WriteMain( periods[i] );
}

//+------------------------------------------------------------------+
void WriteMain(int timeframe)
{
    // Path to save file
    saveFileName = StringConcatenate( mainSavePath, _Symbol, timeframe, ".csv" );
    // Find first bar in current month
    int limit = GetIndexFirstBarMonth( timeframe );
    // Create and Open file (FILE_WRITE | FILE_READ - add. FILE_WRITE - rewrite.)
    int csvFile = FileOpen( saveFileName, FILE_WRITE | FILE_CSV, csvChar );
    // Name column headers
    FileWrite( csvFile, 401, Copyright, _Symbol, timeframe, _Digits, iTime(_Symbol, timeframe, limit - 1), Time[0] );
    for( int i = limit - 1; i >= 0; i-- ) {
        // Go to end of file
        FileSeek( csvFile, 0, SEEK_END );
        FileWrite( csvFile, iTime(_Symbol, timeframe, i), 
                            DoubleToStr( iOpen(_Symbol, timeframe, i), _Digits ), 
                            DoubleToStr( iHigh(_Symbol, timeframe, i), _Digits ), 
                            DoubleToStr( iLow(_Symbol, timeframe, i), _Digits ), 
                            DoubleToStr( iClose(_Symbol, timeframe, i), _Digits ), 
                            iVolume(_Symbol, timeframe, i) );
    }
    FileClose( csvFile );
}

//+------------------------------------------------------------------+
void ReadForecastFile()
{
    // Path to read file
    readFileName = StringConcatenate( mainReadPath, _Symbol, _Period, ".csv" );
    // Open file new data prediction (FILE_SHARE_READ - file may be rewrited.)
    int forecastFile = FileOpen( readFileName, FILE_READ | FILE_SHARE_READ | FILE_CSV, csvChar );
    if( forecastFile != INVALID_HANDLE ) {
        if( ReadHeader(forecastFile) ) {
            while( !FileIsEnding(forecastFile) ) {
                ReadForecast( forecastFile );
            }
        }
        else Print("Wrong type of header file! Reading is stopped.");
        FileClose(forecastFile);
    }
    else Print("File not open! - ", readFileName, "; ", GetLastError());
}

//+------------------------------------------------------------------+
// 
bool ReadHeader(int handle)
{
    bool ready = true;
    versionForecast =   StringToInteger( FileReadString(handle) );
    copyrightForecast = FileReadString(handle);
    symbolForecast =    FileReadString(handle);
    periodForecast =    StringToInteger( FileReadString(handle) );
    digitsForecast =    StringToInteger( FileReadString(handle) );
    startTimeseries =   StringToTime( FileReadString(handle) );
    endTimeseries =     StringToTime( FileReadString(handle) );
    depthForecast =     StringToInteger( FileReadString(handle) );
    /*
    Print( versionForecast, ";",
            copyrightForecast, ";",
            symbolForecast, ";",
            periodForecast, ";",
            digitsForecast, ";",
            startTimeseries, ";",
            endTimeseries, ";",
            depthForecast );*/
    if( symbolForecast != _Symbol ) ready = false;
    
    return ready;
}

//+------------------------------------------------------------------+
// 
void ReadForecast(int handle)
{
    datetime time;
    double buffer[11];
    // Read the High array
    ArraySetAsSeries( fHigh_Buffer, true );
    time = StringToTime( FileReadString(handle) );
    for( int i = 0; i < depthForecast; i++ )
        buffer[i] = StringToDouble( FileReadString(handle) );
    fHigh_Buffer[GetIndexFromTime(time)] = buffer[0];
    ArraySetAsSeries( fHigh_Buffer, false );
    // Read the Low array
    ArraySetAsSeries( fLow_Buffer, true );
    FileReadString(handle);     // time
    for( int i = 0; i < depthForecast; i++ )
        buffer[i] = StringToDouble( FileReadString(handle) );
    fLow_Buffer[GetIndexFromTime(time)] = buffer[0];
    ArraySetAsSeries( fLow_Buffer, false );
    // Read the Close array
    ArraySetAsSeries( fClose_Buffer, true );
    FileReadString(handle);     // time
    for( int i = 0; i < depthForecast; i++ )
        buffer[i] = StringToDouble( FileReadString(handle) );
    fClose_Buffer[GetIndexFromTime(time)] = buffer[0];
    ArraySetAsSeries( fClose_Buffer, false );
}

//+------------------------------------------------------------------+
// Reload a graphical representation
void IndicatorsUpdate()
{
    // master windows
    Comment( "Status MAS_Assistant(", _Symbol, _Period, ") = ", assistState, "\n",
                "Status MAS_Autotrading(", _Symbol, _Period, ") = ", autotraderState );
    ChartRedraw();
}

#endif 
