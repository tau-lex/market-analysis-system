//+------------------------------------------------------------------+
//|                                                MAS_Assistant.mq4 |
//|                                 Copyright 2016, Terentew Aleksey |
//|                        https://www.mql5.com/ru/users/terentjew23 |
//+------------------------------------------------------------------+
#property copyright     "Copyright 2016, Terentew Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property description   ""
#property version       "1.1.6"
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
const char  csvChar = ';';
// File parameters
string      mainSavePath;
string      mainReadPath;
string      configFile;
string      currentYM;
string      saveFileName;
string      readFileName;
// Forecast parameters
int         versionForecast;
string      copyrightForecast;
string      symbolForecast;
int         periodForecast;
int         digitsForecast;
datetime    startTimeseries;
datetime    endTimeseries;
int         depthForecast;
// Status MAS modules
bool        assistState;
bool        autotraderState;
// Configuration
bool        onePeriod;
int         periods[3];



//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
    // Indicator buffers mapping
    SetIndexBuffer(0, fHigh_Buffer);
    SetIndexShift(0, 0);
    SetIndexBuffer( 1, fLow_Buffer);
    SetIndexShift(1, 0);
    SetIndexBuffer( 2, fClose_Buffer);
    SetIndexShift(2, 0);
    // Set File parameters
    configFile = "mas_mt4.conf";
    mainSavePath = "MAS_MarketData/";
    mainReadPath = "MAS_Prediction/";
    currentYM = StringConcatenate( TimeYear(TimeCurrent()), ".", TimeMonth(TimeCurrent()) );
    //saveFileName = StringConcatenate( mainSavePath, "/", _Symbol, "/h", currentYM, "-", _Period );
    //readFileName = StringConcatenate( mainReadPath, "/", _Symbol, "/p", currentYM, "-", _Period );
    // Set Configuration
    SetConfigs();
    // Set status MAS modules
    assistState = true;
    autotraderState = false;
    
    return(INIT_SUCCEEDED);
}



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
    WriteHistoryFile();
    // Read the new forecast data
    if( prev_calculated > 0 )
        ReadForecastFile();
    // Update on the graph indicator
    IndicatorsUpdate();
    
    return(rates_total);
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
    // FileOpen + FILE_SHARE_READ
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
    time = StringToTime( FileReadString(handle) );
    for( int i = 0; i < depthForecast; i++ )
        buffer[i] = StringToDouble( FileReadString(handle) );
    fLow_Buffer[GetIndexFromTime(time)] = buffer[0];
    ArraySetAsSeries( fLow_Buffer, false );
    // Read the Close array
    ArraySetAsSeries( fClose_Buffer, true );
    time = StringToTime( FileReadString(handle) );
    for( int i = 0; i < depthForecast; i++ )
        buffer[i] = StringToDouble( FileReadString(handle) );
    fClose_Buffer[GetIndexFromTime(time)] = buffer[0];
    ArraySetAsSeries( fClose_Buffer, false );
}

//+------------------------------------------------------------------+
// Get the index of the first bar of the month (2)
int GetIndexFirstBarMonth(int timeframe)
{
    int firstBarMonth = 0;
    while( TimeMonth( iTime(_Symbol, timeframe, firstBarMonth) ) == Month() ||
            TimeMonth( iTime(_Symbol, timeframe, firstBarMonth) ) == 12 )
        firstBarMonth++;
    return firstBarMonth;
}

//+------------------------------------------------------------------+
// Get the index of time
int GetIndexFromTime(datetime time)
{
    int index = 0;
    while( Time[index] >= time ) index++;
    
    return index;
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
