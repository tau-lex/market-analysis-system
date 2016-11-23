//+------------------------------------------------------------------+
//|                                                MAS_Assistant.mq4 |
//|                                 Copyright 2016, Terentew Aleksey |
//|                        https://www.mql5.com/ru/users/terentjew23 |
//+------------------------------------------------------------------+
#property copyright     "Copyright 2016, Terentew Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property description   ""
#property version       "1.2"
#property strict

//---------------------Indicators------------------------------------+
#property indicator_chart_window
#property indicator_buffers 4
#property indicator_plots   4
//--- plot Forecast_Open
#property indicator_label1  "Forecast_Open"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrOrangeRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- plot Forecast_Close
#property indicator_label2  "Forecast_Close"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrFireBrick
#property indicator_style2  STYLE_SOLID
#property indicator_width2  1
//--- plot Real_Open
#property indicator_label3  "Real_Open"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrMediumSpringGreen
#property indicator_style3  STYLE_DASH
//#property indicator_style3  STYLE_DOT
#property indicator_width3  1
//--- plot Real_Close
#property indicator_label4  "Real_Close"
#property indicator_type4   DRAW_LINE
#property indicator_color4  clrMediumSeaGreen
#property indicator_style4  STYLE_DASH
#property indicator_width4  1
//--- indicator buffers
double            Forecast_OpenBuffer[];
double            Forecast_CloseBuffer[];
double            Real_OpenBuffer[];
double            Real_CloseBuffer[];

//-----------------Global variables----------------------------------+
const string Copyright = "Copyright 2016, Terentew Aleksey";
const char csvChar = ';';
// File parameters
string configFile;
string fileName;
string pivot = ".pvt";
string murray = ".mry";
string fibo = ".fb";
string csv = ".csv";
string pathToSaveFile;

// Status MAS modules
bool assistState;
bool autotraderState;

// Configuration
bool onePeriod;
int periods[3];
bool mainTimeSeries;
bool pivotTimeSeries;
bool murrayTimeSeries;
bool fiboPivotTimeSeries;
//+------------------------------------------------------------------+



//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
    // Indicator buffers mapping
    SetIndexBuffer( 0, Forecast_OpenBuffer );
    SetIndexBuffer( 1, Forecast_CloseBuffer );
    SetIndexBuffer( 2, Real_OpenBuffer );
    SetIndexBuffer( 3, Real_CloseBuffer );
    
    // Set File parameters
    configFile = StringConcatenate( "MarketData", "/", "mas.conf" );
    fileName = StringConcatenate( TimeYear(TimeCurrent()), ".", TimeMonth(TimeCurrent()) );
    //pathToSaveFile = StringConcatenate( "MarketData", "/", _Symbol, _Period, "/" , fileName );
    
    // Set Configuration
    //ReadConfigFile();
    onePeriod = false;
    periods[0] = 60;
    periods[1] = 240;
    periods[2] = 1440;
    
    mainTimeSeries = true;
    pivotTimeSeries = false;
    murrayTimeSeries = false;
    fiboPivotTimeSeries = false;
    
    // Set status MAS modules
    assistState = true;
    autotraderState = false;
    
    // 
    return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+


  
//+------------------------------------------------------------------+
//| Main function. Called with tick                                  |
//+------------------------------------------------------------------+
int OnCalculate( const int rates_total,
                     const int prev_calculated,
                     const datetime &time[],
                     const double &open[],
                     const double &high[],
                     const double &low[],
                     const double &close[],
                     const long &tick_volume[],
                     const long &volume[],
                     const int &spread[] )
{
    //ulong msec = GetMicrosecondCount(); // debug: write time
    WriteFiles();
    //Print( "Files writed. mksec = ", (GetMicrosecondCount() - msec) ); // debug: write time
    
    ReadForecastFile();
    IndicatorsUpdate();
    
    return(rates_total);
}
//+------------------------------------------------------------------+



//+------------------------------------------------------------------+
//| Functions                                                        |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
void WriteFiles()
{
    // Main
    if( onePeriod )
        WriteMain( _Period );
    else
        for(int i = 0; i < 3; i++)
            WriteMain( periods[i] );
    // Pivot points
    if( pivotTimeSeries )
    {
        if( onePeriod )
            WritePivot( _Period );
        else
            for(int i = 0; i < 3; i++)
                WritePivot( periods[i] );
    }
    // Indicator Murray
    if( murrayTimeSeries )
    {
        if( onePeriod )
            WriteMurray( _Period );
        else
            for(int i = 0; i < 3; i++)
                WriteMurray( periods[i] );
    }
    // Fibo-Pivot points
    if( fiboPivotTimeSeries )
    {
        if( onePeriod )
            WriteFiboPivot( _Period );
        else
            for(int i = 0; i < 3; i++)
                WriteFiboPivot( periods[i] );
    }
    
    return;
}

//+------------------------------------------------------------------+
void WriteMain(int timeframe)
{
    pathToSaveFile = StringConcatenate( "MarketData", "/", _Symbol, timeframe, "/" , fileName, csv );
    /*
    int counted_bars = IndicatorCounted();
    if( counted_bars > 0 ) counted_bars--;
    limit = Bars - counted_bars - 1; 
    */
    int limit = GetFirstBarMonth( timeframe );
    
    // Create and Open file (FILE_WRITE | FILE_READ - дозапись. FILE_WRITE - перезапись.)
    int handle = FileOpen(pathToSaveFile, FILE_WRITE | FILE_CSV, csvChar);
    // Name column headers
    FileWrite(handle, 401, Copyright, _Symbol, timeframe, _Digits, iTime(_Symbol, timeframe, limit - 1), Time[0] );
    
    for( int i = limit - 1; i >= 0; i-- ) 
    {
        // Go to end of file
        FileSeek(handle, 0, SEEK_END);
        
        FileWrite(handle, iTime(_Symbol, timeframe, i), 
                            DoubleToStr( iOpen(_Symbol, timeframe, i), _Digits ), 
                            DoubleToStr( iHigh(_Symbol, timeframe, i), _Digits ), 
                            DoubleToStr( iLow(_Symbol, timeframe, i), _Digits ), 
                            DoubleToStr( iClose(_Symbol, timeframe, i), _Digits ), 
                            iVolume(_Symbol, timeframe, i) );
    }
    FileClose(handle);
    return;
}

//+------------------------------------------------------------------+
void WritePivot(int timeframe)
{
    pathToSaveFile = StringConcatenate( "MarketData", "/", _Symbol, timeframe, "/" , fileName, pivot, csv );
    int limit = GetFirstBarMonth( timeframe );
    
    int handle = FileOpen(pathToSaveFile, FILE_WRITE | FILE_CSV, csvChar);
    FileWrite(handle, "Open Time"/*, pivot points */);
    
    for( int i = limit - 1; i >= 0; i-- ) 
    {
        FileSeek(handle, 0, SEEK_END);
        FileWrite(handle, iTime(_Symbol, timeframe, i)/*, 
                            pivot points 
                            */ );
    }
    FileClose(handle);
    return;
}

//+------------------------------------------------------------------+
void WriteMurray(int timeframe)
{
    pathToSaveFile = StringConcatenate( "MarketData", "/", _Symbol, timeframe, "/" , fileName, murray, csv );
    int limit = GetFirstBarMonth( timeframe );
    
    int handle = FileOpen(pathToSaveFile, FILE_WRITE | FILE_CSV, csvChar);
    FileWrite(handle, "Open Time"/*, Murray points */);
    
    for( int i = limit - 1; i >= 0; i-- ) 
    {
        FileSeek(handle, 0, SEEK_END);
        FileWrite(handle, iTime(_Symbol, timeframe, i)/*, 
                            Murray points 
                            */ );
    }
    FileClose(handle);
    return;
}

//+------------------------------------------------------------------+
void WriteFiboPivot(int timeframe)
{
    pathToSaveFile = StringConcatenate( "MarketData", "/", _Symbol, timeframe, "/" , fileName, fibo, csv );
    int limit = GetFirstBarMonth( timeframe );
    
    int handle = FileOpen(pathToSaveFile, FILE_WRITE | FILE_CSV, csvChar);
    FileWrite(handle, "Open Time"/*, Fibo points */);
    
    for( int i = limit - 1; i >= 0; i-- ) 
    {
        FileSeek(handle, 0, SEEK_END);
        FileWrite(handle, iTime(_Symbol, timeframe, i)/*, 
                            Fibo points 
                            */ );
    }
    FileClose(handle);
    return;
}

//+------------------------------------------------------------------+
void ReadConfigFile()
{
    // FileOpen + FILE_SHARE_READ
    
    return;
}

//+------------------------------------------------------------------+
void ReadForecastFile()
{
    // FileOpen + FILE_SHARE_READ
    
    return;
}

//+------------------------------------------------------------------+
// Reload a graphical representation
void IndicatorsUpdate()
{
    Comment( "Status MAS_Assistant(", _Symbol, _Period, ") = ", assistState, "\n",
                "Status MAS_Autotrading(", _Symbol, _Period, ") = ", autotraderState );
    
    return;
}

//+------------------------------------------------------------------+
// Get the string length of double precision
string Format(double v)
{
    string s = DoubleToStr( v, _Digits );
    int len = StringLen(s);
    for(int i=0; i<=len-1; i++)
        if( StringGetCharacter(s, i) == 46 ) 
            StringSetCharacter(s, i, 44);
    return s;
}

//+------------------------------------------------------------------+
// Get the index of the first bar of the month
int GetFirstBarMonth(int timeframe)
{
    int firstBar = 0;
    while( true )
    {
        if( TimeMonth( iTime(_Symbol, timeframe, firstBar) ) != Month() )
            break;
        firstBar++;
    }
    return firstBar;
}