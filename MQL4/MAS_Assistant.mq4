//+------------------------------------------------------------------+
//|                                                MAS_Assistant.mq4 |
//|                                 Copyright 2016, Terentew Aleksey |
//|                        https://www.mql5.com/ru/users/terentjew23 |
//+------------------------------------------------------------------+
#property copyright     "Copyright 2016, Terentew Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property description   "This indicator is a modul in the Market Analysis System programm complex."
#property description   "MAS_Assistant save history and read forecast for Market Assay Kit."
#property version       "1.3.4"
#property strict
#include                <MAS_Include.mqh>
//---------------------Indicators---------------------------------------------+
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
#ifndef MAS_INCLUDE
    double  fHigh_Buffer[];
    double  fLow_Buffer[];
    double  fClose_Buffer[];
#endif

//-----------------Global variables-------------------------------------------+
const string    Copyright = "Copyright 2016, Terentew Aleksey";
const string    comment = "MAS_Assistant v1.3.4";
input string    configFile = "mas.conf";
input bool      messagesOn = true;
input char      csvChar = ';';
UiAssistant     ui;
// Configuration
bool        isReady = false;
bool        configIsReaded = false;
bool        symbolsIsWrited = false;
string      kitList[][64];
string      inputSymbols[][64];
string      outputSymbols[][64];
string      kitName = "none";
string      outputSymbol;
int         depthForecast;
//int         thisSymbolId;


//+---------------------------------------------------------------------------+
int OnInit()
{
#ifndef MAS_INCLUDE
Print( "Arrays from main file." );
#endif
    Comment( comment );
    ArraysClear();
    SetIndexBuffer( 0, fHigh_Buffer );
    SetIndexShift(  0, 0 );
    SetIndexBuffer( 1, fLow_Buffer );
    SetIndexShift(  1, 0 );
    SetIndexBuffer( 2, fClose_Buffer );
    SetIndexShift(  2, 0 );
    tickCount = 0;
    configIsReaded = ReadConfig( configFile, kitList, symbolsIsWrited );
    if( configIsReaded && ArraySize( kitList ) > 0 ) {
        kitName = kitList[0][0];
        ReadKitConfig( configFile, kitName, inputSymbols, outputSymbols, depthForecast );
        outputSymbol = outputSymbols[0][0];
        if( StringFind( outputSymbol, _Symbol ) >= 0 )
            isReady = true;
        ui.SetMAKit( kitName );
        ui.SetMASymbol( outputSymbol );
    }
    ui.Run( ChartID(), ChartWindowFind() );
    return( INIT_SUCCEEDED );
}

//+---------------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
    tickCount++;
    if( isReady ) {
        if( NewBar( _Period ) ) {
            Print( "New Bar Emit." );
            for( int idx = 0; idx < ArrayRange( inputSymbols, 0 ); idx++ )
                SaveHistory( inputSymbols[idx][0], Copyright );
        }
        if( NewForecast( outputSymbol ) ) {
            datetime controlBars[]; 
            ReadForecastBarSeries( outputSymbol, controlBars );
            ui.SetControlBars( controlBars );
        }
    } else {
        if( !configIsReaded ) {
            configIsReaded = ReadConfig( configFile, kitList, symbolsIsWrited );
            if( configIsReaded && ArrayRange( kitList, 0 ) > 0 ) {
                kitName = kitList[0][0];
                ReadKitConfig( configFile, kitName, inputSymbols, outputSymbols, depthForecast );
                outputSymbol = outputSymbols[0][0];
                if( StringFind( outputSymbol, _Symbol ) >= 0 )
                    isReady = true;
                ui.SetMAKit( kitName );
                ui.SetMASymbol( outputSymbol );
            }
        }
        if( configIsReaded && ArrayRange( kitList, 0 ) > 0 ) {
            if( StringFind( outputSymbol, _Symbol ) >= 0 ) {
                Print( "Assistant ready." );
                isReady = true;
                //string glVarOut = StringConcatenate( "MAS_", kitName, thisSymbolId );
                //GlobalVariableSet( glVarOut, 12.34 ); // <- id Window
            } else {
                for( int idx = 0; idx < ArrayRange( outputSymbols, 0 ); idx++ )
                    OpenNewWindow( outputSymbols[idx][0] );
                //if( thisWindowClose? )
                //    CloseThisWindow();
            }
        }
    }
    return( rates_total );
}

//+---------------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
    ui.OnEvent( id, lparam, dparam, sparam );
}

//+---------------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    ui.Deinit();
    Comment( "" );
}