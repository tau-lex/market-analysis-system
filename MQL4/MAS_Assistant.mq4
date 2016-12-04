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
#property indicator_buffers 3
#property indicator_plots   3
//--- plot Forecast_High
#property indicator_label1  "Forecast_High"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrOrangeRed
#property indicator_style1  STYLE_DOT
#property indicator_width1  1
//--- plot Forecast_Low
#property indicator_label2  "Forecast_Low"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrFireBrick
#property indicator_style2  STYLE_DOT
#property indicator_width2  1
//--- plot Forecast_Close
#property indicator_label3  "Forecast_Close"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrMediumSpringGreen
#property indicator_style3  STYLE_DASH
#property indicator_width3  1
//#property indicator_style3  STYLE_DOT | STYLE_DASH

//--- indicator buffers
double  fHigh_Buffer[];
double  fLow_Buffer[];
double  fClose_Buffer[];

//-----------------Global variables----------------------------------+
const string Copyright = "Copyright 2016, Terentew Aleksey";
const char csvChar = ';';
// File parameters
string mainSavePath;
string mainReadPath;
string configFile;
string fileName;
string pathToSaveFile;

// Status MAS modules
bool assistState;
bool autotraderState;

// Configuration
bool onePeriod;
int  periods[3];

//+------------------------------------------------------------------+



//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
    // Indicator buffers mapping
    SetIndexBuffer( 0, fHigh_Buffer );
    SetIndexBuffer( 1, fLow_Buffer );
    SetIndexBuffer( 2, fClose_Buffer );
    
    // Set File parameters
    configFile = "mas_mt4.conf";
    mainSavePath = "MAS_MarketData";
    mainReadPath = "MAS_Prediction"
    currentYM = StringConcatenate( TimeYear(TimeCurrent()), ".", TimeMonth(TimeCurrent()) );
    //pathToSaveFile = StringConcatenate( mainSavePath, '/', _Symbol, '/', currentYM, '-', _Period );
    
    // Set Configuration
    SetConfigs();
    
    // Set status MAS modules
    assistState = true;
    autotraderState = false;
    
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
    // Record new historical data to a file
    WriteHistoryCsvFiles();
    // Read the new forecast data
    ReadForecastFile();
    // Update on the graph indicator
    IndicatorsUpdate();
    
    return(rates_total);
}
//+------------------------------------------------------------------+



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
    
    // FileOpen + FILE_SHARE_READ
    
    return;
}

//+------------------------------------------------------------------+
void WriteHistoryCsvFiles()
{
    if( onePeriod )
        WriteMain( _Period );
    else
        for(int i = 0; i < 3; i++)
            WriteMain( periods[i] );
    
    return;
}

//+------------------------------------------------------------------+
void WriteMain(int timeframe)
{
    // Path to save file
    pathToSaveFile = StringConcatenate( mainSavePath, '/', _Symbol, '/', currentYM, '-', timeframe, ".csv" );
    // Find first bar in current month
    int limit = GetFirstBarMonth( timeframe );
    // Create and Open file (FILE_WRITE | FILE_READ - add. FILE_WRITE - rewrite.)
    int handle = FileOpen( pathToSaveFile, FILE_WRITE | FILE_CSV, csvChar );
    // Name column headers
    FileWrite( handle, 401, Copyright, _Symbol, timeframe, _Digits, iTime(_Symbol, timeframe, limit - 1), Time[0] );
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
