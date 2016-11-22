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
// File names
string configFile;
string outDataPath;
string fileName;
// Status MAS modules
bool assistState;
bool autotraderState;
//
string lastWritedString;
bool endFile;

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
//--- indicator buffers mapping
    SetIndexBuffer( 0, Forecast_OpenBuffer );
    SetIndexBuffer( 1, Forecast_CloseBuffer );
    SetIndexBuffer( 2, Real_OpenBuffer );
    SetIndexBuffer( 3, Real_CloseBuffer );
    
//---
    configFile = StringConcatenate( "MarketData", "/", "config.ini" );
    outDataPath = StringConcatenate( "MarketData", "/", _Symbol, "/", _Period, "/" );
    fileName = StringConcatenate( outDataPath, TimeYear(TimeCurrent()), ".", TimeMonth(TimeCurrent()), ".csv" );
    
    endFile = false;
    
//---
    assistState = true;
    autotraderState = false;
    
//---
    return(INIT_SUCCEEDED);
}
  
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
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
    ReadConfigFile();
    WriteFile();
    IndicatorsUpdate();
    
    return(rates_total);
}

//+------------------------------------------------------------------+
//| Functions                                                        |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
void WriteFile()
{
    int limit,i;
    ulong msec = GetMicrosecondCount(); // debug: write time
    /*
    int counted_bars = IndicatorCounted();
    if( counted_bars > 0 ) counted_bars--;
    limit = Bars - counted_bars - 1; 
    */
    limit = GetFirstBarMonth();
    
    // Create and Open file (FILE_WRITE | FILE_READ - дозапись. FILE_WRITE - перезапись.)
    int handle = FileOpen(fileName, FILE_WRITE | FILE_CSV, ",");
    // Name column headers
    FileWrite(handle, "Open Time", " Open", " High", " Low", " Close", " Volume");
    
    for( i = limit; i >= 0; i-- ) 
    {
        // Go to end of file
        FileSeek(handle, 0, SEEK_END);
        
        FileWrite(handle, Time[i], Format(Open[i]), Format(High[i]), Format(Low[i]), Format(Close[i]), Volume[i]);
    }
    // Close file
    FileClose(handle);
    
    Print("File writed. MSec = ", (GetMicrosecondCount() - msec));
    
    return;
}

//+------------------------------------------------------------------+
void ReadConfigFile()
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
int GetFirstBarMonth()
{
    int firstBar = 0;
    while( true )
    {
        if( TimeMonth(Time[firstBar]) != Month() )
            break;
        firstBar++;
    }
    return firstBar;
}