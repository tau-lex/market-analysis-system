//+---------------------------------------------------------------------------+
//|                                                        MASi_Assistant.mq4 |
//|                                         Copyright 2017, Terentyev Aleksey |
//|                                 https://www.mql5.com/ru/users/terentjew23 |
//+---------------------------------------------------------------------------+
#property copyright     "Copyright 2017, Terentyev Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property description   "This indicator is a module in the Market Analysis System programm complex."
#property description   "MASi_Assistant save history and read forecast for Market Assay Kit."
#property description   "License GNU LGPL v.3"
#property version       "1.3.7"
#property strict

#include                "MASh_Include.mqh"
#include                "MASh_MasterWindows.mqh"

//---------------------Indicators---------------------------------------------+
#property indicator_chart_window
#property indicator_buffers 3
//--- plot Forecast_High
#property indicator_label1  "Forecast High"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrBlue
//#property indicator_style1  STYLE_DASH
#property indicator_width1  1
//--- plot Forecast_Low
#property indicator_label2  "Forecast Low"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrRed
//#property indicator_style2  STYLE_DASH
#property indicator_width2  1
//--- plot Forecast_Close
#property indicator_label3  "Forecast Close"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrLimeGreen
//#property indicator_style3  STYLE_SOLID
#property indicator_width3  1
//--- indicator buffers
double      HighBuffer[];
double      LowBuffer[];
double      CloseBuffer[];

//-----------------Global variables-------------------------------------------+
const string    Copyright = COPYRIGHT;
const string    comment = "MAS_Assistant v1.3.7";
input string    configFile = "mas.conf";
input bool      messagesOn = true;
input string    csvSeparator = ";";
bool            isReady = false;
bool            configIsReaded = false;
bool            symbolsIsWrited = false;
string          kitList[][64];
string          inputSymbols[][64];
string          outputSymbols[][64];
string          kitName = "none";
string          outputSymbol;
int             depthForecast;
string          mainSavePath = "MAS_MarketData/";
string          mainReadPath = "MAS_Prediction/";

//+--------------------UserInterface Class------------------------------------+
#ifdef MAS_MASTERWINDOWS
int Mint[][3] =     { { 1, 0,   0  },
                      { 2, 100, 0  },
                      { 4, 100, 50 } };
string Mstr[][3] =  { { "MAS_Assistant", "",               "" },
                      { "Kit name",      "none",           "" },
                      { "Control Bar",   "hh:mm dd.MM.yy", "" } };
class UiAssistant : public CWin
{
private:
    long            Y_hide;
    long            Y_obj;
    long            H_obj;
    long            idChart;
    int             idWind;
    string          nameMAKit;
    string          symbol;
    datetime        controlBars[];
    int             idx;
private:
    void Redraw(const int line, const string text) {
        string lineName = StringConcatenate( "MAS_Assistant.Exp.STR", line );
        int Y = w_ypos + line * (Property.H + DELTA);
        if( line == 1 )
            STR1.Draw( lineName, w_xpos, Y, w_bsize, 100, "Kit name", text );
        else
            STR2.Draw( lineName, w_xpos, Y, w_bsize, 100, "Control Bar", text );
    }
public:
    void UiAssistant() { on_event = false; }
    void Run(const long chId, const int wId)
    {
        idChart = chId; idWind = wId;
        ObjectsDeleteAll( idChart, idWind, EMPTY );
        SetWin( "MAS_Assistant.Exp", 30, 40, 300, CORNER_RIGHT_UPPER );
        Draw( Mint, Mstr, 2 );
    }
    void SetMAKit(const string tmp) 
    { 
        nameMAKit = tmp;
        Redraw( 1, nameMAKit );
    }
    void SetMAOutSymbol(const string tmp) { symbol = tmp; }
    void SetControlBars(const datetime &bars[])
    {
        ArrayFree( controlBars ); ArrayResize( controlBars, ArraySize( bars ) );
        for( int i = 0; i < ArraySize(bars); i++ )
            controlBars[i] = bars[i];
        Redraw( 2, TimeToString( controlBars[0] ) );
        ReadForecast( symbol, controlBars[0] );
        idx = 0;
    }
    void Hide() { }
    void Deinit() 
    {
        ObjectsDeleteAll( idChart, idWind, EMPTY );
        ChartIndicatorDelete( 0, 0, "MAS_Assistant" );
    }
    virtual void OnEvent(const int id, const long &lparam, const double &dparam, const string &sparam)
    {
        if( on_event && StringFind(sparam, "MAS_Assistant.Exp", 0) >= 0 ) {
            STR0.OnEvent( id, lparam, dparam, sparam );
            STR1.OnEvent( id, lparam, dparam, sparam );
            STR2.OnEvent( id, lparam, dparam, sparam );
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CREATE ) {
                if( ArraySize( controlBars ) > 0 )
                    ReadForecast( symbol, controlBars[idx] );
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_ENDEDIT
                            && StringFind(sparam, ".STR1", 0) > 0 ) {
                Redraw( 1, nameMAKit );
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CLICK
                            && StringFind(sparam, ".STR2", 0) > 0
                            && StringFind(sparam, ".Button3", 0) > 0 ) {
                if( idx > 0 ) {
                    idx = 0;
                    Redraw( 2, TimeToString( controlBars[idx] ) );
                    ReadForecast( symbol, controlBars[idx] );
                }
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CLICK
                            && StringFind(sparam, ".STR2", 0) > 0
                            && StringFind(sparam, ".Button4", 0) > 0 ) {
                if( idx > 0 ) {
                    idx--;
                    Redraw( 2, TimeToString( controlBars[idx] ) );
                    ReadForecast( symbol, controlBars[idx] );
                }
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CLICK
                            && StringFind(sparam, ".STR2", 0) > 0
                            && StringFind(sparam, ".Button5", 0) > 0 ) {
                if( idx < (ArraySize( controlBars ) - 1) ) {
                    idx++;
                    Redraw( 2, TimeToString( controlBars[idx] ) );
                    ReadForecast( symbol, controlBars[idx] );
                }
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CLICK
                            && StringFind(sparam, ".STR2", 0) > 0
                            && StringFind(sparam, ".Button6", 0) > 0 ) {
                if( idx < (ArraySize( controlBars ) - 1) ) {
                    idx = ArraySize( controlBars ) - 1;
                    Redraw( 2, TimeToString( controlBars[idx] ) );
                    ReadForecast( symbol, controlBars[idx] );
                }
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CLICK
                            && StringFind(sparam, ".Button0", 0) > 0 ) {
                Hide();
            }
            if( (ENUM_CHART_EVENT)id == CHARTEVENT_OBJECT_CLICK
                            && StringFind(sparam, ".Button1", 0) > 0 ) {
                Deinit();
                ExpertRemove();
            }
        }
    }
};
#endif // MAS_MASTERWINDOWS

//+------------------------UI-------------------------------------------------+
UiAssistant     ui;

//+---------------------------------------------------------------------------+
int OnInit()
{
    Comment( comment );
    SetIndexShift( 0, 0 );
    SetIndexShift( 1, 0 );
    SetIndexShift( 2, 0 );
    SetIndexBuffer( 0, HighBuffer );
    SetIndexBuffer( 1, LowBuffer );
    SetIndexBuffer( 2, CloseBuffer );
    tickCount = 0;
    //if( GlobalVariableCheck( "glSymbolsWrited" ) )
    //    symbolsIsWrited = (bool)GlobalVariableGet( "glSymbolsWrited" );
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
            if( messagesOn )
                Print( "msg: New bar." );
            for( int idx = 0; idx < ArrayRange( inputSymbols, 0 ); idx++ ) {
                if( SaveHistory( inputSymbols[idx][0] ) && messagesOn )
                    PrintFormat( "msg: History file %s.csv saved.", inputSymbols[idx][0] );
            }
        }
        if( NewForecast( 0, outputSymbol ) ) {
            if( messagesOn )
                PrintFormat( "msg: New forecast %s.", outputSymbol );
            datetime controlBars[]; 
            if( ReadForecastBarSeries( outputSymbol, controlBars ) == 0 ) {
                ui.SetControlBars( controlBars );
                PrintFormat( "Readed forcast file %s.csv.", outputSymbol );
            }
        }
    } else {
        if( !configIsReaded || ArrayRange( kitList, 0 ) <= 0 ) {
            configIsReaded = ReadConfig( configFile, kitList );
            if( configIsReaded && ArrayRange( kitList, 0 ) > 0 ) {
                kitName = kitList[0][0];
                ReadKitConfig( configFile, kitName, inputSymbols, outputSymbols, depthForecast );
                if( messagesOn )
                    PrintFormat( "msg: Kit %s readed. In=%s...%s, Out0=%s, Depth forecast=%d", kitName,
                                    inputSymbols[0][0], inputSymbols[ArrayRange(inputSymbols,0)-1][0], 
                                    outputSymbols[0][0], depthForecast );
                if( StringFind( outputSymbols[0][0], _Symbol ) >= 0 ) {
                    outputSymbol = outputSymbols[0][0];
                    PrintFormat( "Assistant for %s is ready.", outputSymbol );
                    isReady = true;
                }
                ui.SetMAKit( kitName );
                ui.SetMAOutSymbol( outputSymbol );
                datetime controlBars[]; 
                if( ReadForecastBarSeries( outputSymbol, controlBars ) == 0 )
                    ui.SetControlBars( controlBars );
            }
        }
        if( configIsReaded && ArrayRange( kitList, 0 ) > 0 ) {
            if( ArrayRange( outputSymbols, 0 ) > 0 ) {
                for( int idx = 0; idx < ArrayRange( outputSymbols, 0 ); idx++ ) {
                    if( SymbolIsTime( outputSymbols[idx][0] ) )
                        continue;
                    if( StringFind( outputSymbols[idx][0], _Symbol ) >= 0 && !isReady ) {
                        outputSymbol = outputSymbols[idx][0];
                        PrintFormat( "Assistant for %s is ready.", outputSymbol );
                        isReady = true;
//                        for( int idxh = 0; idxh < ArrayRange( inputSymbols, 0 ); idxh++ )  {
//                            if( SaveHistory( inputSymbols[idxh][0] ) && messagesOn )
//                                PrintFormat( "msg: History file %s.csv saved.", inputSymbols[idxh][0] );
//                        }
                        break;
                    }
                    if( StringFind( outputSymbols[idx][0], _Symbol ) < 0 &&
                            OpenNewWindow( outputSymbols[idx][0] ) > 0 )
                        if( messagesOn ) PrintFormat( "msg: Open %s chart.", outputSymbols[idx][0] );
                    else
                        PrintFormat( "err: Open aborted %s chart. %d", outputSymbols[idx][0], GetLastError() );
                }
                if( !isReady )
                    CloseThisWindow();
            } else {
                Print( "Assistant not found output symbols." );
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
    Comment( "" );
    ui.Deinit();
    ChartIndicatorDelete( 0, 0, "MAS_Assistant" );
}

//+---------------------------------------------------------------------------+
struct ForecastHeader {
    int         Version;
    string      Copyright;
    string      SymbolF;
    int         PeriodF;
    int         DigitsF;
    datetime    StartTS;
    datetime    EndTS;
    int         Depth;
};
//+---------------------------------------------------------------------------+
//| Functions                                                                 |
//+---------------------------------------------------------------------------+
bool NewBar(const int tf)
{
    static datetime lastTime = 0;
    bool condition = false;
    if( lastTime != TimeCurrent() ) {
        condition = ( ( TimeCurrent() - lastTime >= PeriodSeconds(tf) ) || 
                      ( TimeCurrent() % PeriodSeconds(tf) == 0 ) );
        if( condition ) {
            lastTime = TimeCurrent();
        }
    }
    if( tickCount <= 1 )
        return true;
    return condition;
};

bool NewForecast(const int tf, const string symb)
{
    static datetime lastTime = 0;
    bool condition = false;
    if( lastTime != TimeCurrent() ) {
        condition = ( ( TimeCurrent() - lastTime >= PeriodSeconds(tf) ) || 
                      ( TimeCurrent() % PeriodSeconds(tf) == 0 ) );
        if( condition ) {
            lastTime = TimeCurrent();
        }
    } 
    return condition;
};

bool SaveHistory(const string symb)
{
    if( SymbolIsTime( symb ) ) {
        return false;
    }
    ushort  csvSep = StringGetChar( csvSeparator, 0 );
    string  symbol, saveFile;
    int     timeframe = 0, limit, csvFile;
    SeparateMasSymbol( symb, symbol, timeframe );
    saveFile = StringConcatenate( mainSavePath, symb, ".csv" );
    limit = GetIndexFirstBar( timeframe );
    csvFile = FileOpen( saveFile, FILE_WRITE | FILE_CSV, csvSep );
    FileWrite( csvFile, 401, Copyright, symbol, timeframe, (int)MarketInfo( symbol, MODE_DIGITS ), 
                iTime( symbol, timeframe, limit - 1 ), iTime( symbol, timeframe, 0 ) );
    for( int i = limit - 1; i >= 0; i-- ) {
        FileSeek( csvFile, 0, SEEK_END );
        FileWrite( csvFile, iTime( symbol, timeframe, i ), 
                            DoubleToStr( iOpen(  symbol, timeframe, i ), (int)MarketInfo( symbol, MODE_DIGITS ) ), 
                            DoubleToStr( iHigh(  symbol, timeframe, i ), (int)MarketInfo( symbol, MODE_DIGITS ) ), 
                            DoubleToStr( iLow(   symbol, timeframe, i ), (int)MarketInfo( symbol, MODE_DIGITS ) ), 
                            DoubleToStr( iClose( symbol, timeframe, i ), (int)MarketInfo( symbol, MODE_DIGITS ) ), 
                            iVolume(_Symbol, timeframe, i) );
    }
    FileClose( csvFile );
    return true;
};

bool ReadConfig(const string file, string &list[][64] )
{
    bool mainSection = false;
    string fileBuffer[5][256], symbolsString, tmp;
    int size = 0, idx = 0, kitIdx = -1;
    ushort sep = StringGetChar( csvSeparator, 0 );
    if( !symbolsIsWrited )
        GetSymbolsString( true, symbolsString );
    int config = FileOpen( file, FILE_READ | FILE_SHARE_READ | FILE_TXT );
    if( config != INVALID_HANDLE ) {
        while( !FileIsEnding( config ) ) {
            fileBuffer[size][0] = FileReadString( config );
            size++;
            if( size >= ArrayRange( fileBuffer, 0 ) )
                ArrayResize( fileBuffer, size + 5 );
        }
        FileClose( config );
    } else {
        PrintFormat( "err: Config file not open. %d", GetLastError() );
        return false;
    }
    while( idx < size ) {
        if( StringFind( fileBuffer[idx][0], "[Main]" ) >= 0 ) {
            mainSection = true;
        }
        if( StringFind( fileBuffer[idx][0], "Kit_Names=" ) >= 0 && mainSection ) {
		    tmp = StringSubstr( fileBuffer[idx][0], 10 );
		    StringReplace( tmp, "\"", "" );
            StringSplitMAS( tmp, ';', list );
            kitIdx = idx;
        }
        if( StringFind( fileBuffer[idx][0], "Symbols=" ) >= 0 && mainSection ) {
            tmp = StringSubstr( fileBuffer[idx][0], 8 );
            if( StringLen( tmp ) <= 10 )
                fileBuffer[idx][0] = StringConcatenate( "Symbols=\"", symbolsString, "\"" );
            symbolsIsWrited = true;
            //GlobalVariableSet( "glSymbolsWrited", (double)symbolsIsWrited );
        }
        if( StringFind( fileBuffer[idx][0], "Mt4_Account=" ) >= 0 && mainSection ) {
            tmp = StringSubstr( fileBuffer[idx][0], 12 );
            if( StringToInteger( tmp ) != AccountNumber() )
                fileBuffer[idx][0] = "Mt4_Account=" + IntegerToString( AccountNumber() );
        }
        if( !symbolsIsWrited && kitIdx >= 1 && idx >= 2 ) {
            tmp = StringConcatenate( "Symbols=\"" + symbolsString + 
                                     "\"\r\nMt4_Account=" + IntegerToString(AccountNumber()) );
            fileBuffer[kitIdx][0] = StringConcatenate( fileBuffer[kitIdx][0], "\r\n", tmp );
            symbolsIsWrited = true;
            //GlobalVariableSet( "glSymbolsWrited", (double)symbolsIsWrited );
        }
        idx++;
    }
    config = FileOpen( file, FILE_WRITE | FILE_TXT );
    if( config != INVALID_HANDLE ) {
        for( idx = 0; idx < size; idx++ ) {
            FileWriteString( config, fileBuffer[idx][0] );
            if( fileBuffer[idx][0] == "" && fileBuffer[idx-1][0] == "" ) 
                continue;
            FileWriteString( config, "\r\n" );
        }
        FileClose( config );
    } else {
        PrintFormat( "err: Config file not opened for write. %d", GetLastError() );
        return false;
    }
    if( ArraySize(list) <= 0 )
        return false;
    return true;
};

void ReadKitConfig(const string file, const string kit,
                    string &inputList[][64], string &outputList[][64], int &depth)
{
    string tmpString, section = StringConcatenate( "[", kit, "]" );
    int config = FileOpen( file, FILE_READ | FILE_SHARE_READ | FILE_TXT );
    if( config != INVALID_HANDLE ) {
        while( !FileIsEnding( config ) ) {
            tmpString = FileReadString( config );
            if( StringFind( tmpString, section ) >= 0 ) {
                tmpString = FileReadString( config );
                if( StringFind( tmpString, "Depth_Prediction=" ) >= 0 ) {
                    depth = (int)StringToInteger( StringTrimRight( StringSubstr( tmpString, 17 ) ) );
                    tmpString = FileReadString( config );
                }
                if( StringFind( tmpString, "Input=" ) >= 0 ) {
                    StringReplace( tmpString, "\"", "" );
                    StringSplitMAS( StringTrimRight( StringSubstr( tmpString, 6 ) ), ';', inputList );
                    tmpString = FileReadString( config );
                }
                if( StringFind( tmpString, "Output=" ) >= 0 ) {
                    StringReplace( tmpString, "\"", "" );
                    StringSplitMAS( StringTrimRight( StringSubstr( tmpString, 7 ) ), ';', outputList );
                    tmpString = FileReadString( config );
                }
            }
        }
        FileClose( config );
    } else {
        PrintFormat( "err: Config file not open. %d", GetLastError() );
    }
};

int ReadForecastBarSeries(const string symb, datetime &seriesControlBars[], const char csvSep = ';')
{
    int idx = 0;
    ForecastHeader header;
    string readFile = StringConcatenate( mainReadPath, symb, ".csv" );
    int forecastFile = FileOpen( readFile, FILE_READ | FILE_SHARE_READ | FILE_CSV, csvSep );
    if( forecastFile != INVALID_HANDLE ) {
        if( ReadHeader( forecastFile, header ) ) {
            while( !FileIsEnding( forecastFile ) ) {
                if( idx >= ArraySize( seriesControlBars ) )
                    ArrayResize( seriesControlBars, ArraySize( seriesControlBars ) + 1 );
                seriesControlBars[idx] = ReadForcastBar( forecastFile, header.Depth );
                idx++;
            }
        } else {
            Print( "err: Wrong header of file! Reading is stopped." );
            FileClose( forecastFile );
            return 2;
        }
        FileClose( forecastFile );
    } else {
        Print( "err: File not open! ", readFile, "; ", GetLastError() );
        return 1;
    }
    return 0;
};

int ReadForecast(const string symb, const datetime controlBar, const char csvSep = ';')
{
    ForecastHeader header;
    string readFile = StringConcatenate( mainReadPath, symb, ".csv" );
    int forecastFile = FileOpen( readFile, FILE_READ | FILE_SHARE_READ | FILE_CSV, csvSep );
    if( forecastFile != INVALID_HANDLE ) {
        if( ReadHeader( forecastFile, header ) ) {
            while( !FileIsEnding( forecastFile ) ) {
                if( ReadForcastTS( forecastFile, header, controlBar ) )
                    break;
            }
        } else {
            Print( "err: Wrong header of file! Reading is stopped." );
            FileClose( forecastFile );
            return 2;
        }
        FileClose( forecastFile );
    } else {
        Print( "err: File not open! ", readFile, "; ", GetLastError() );
        return 1;
    }
    return 0;
};

bool ReadHeader(const int handle, ForecastHeader &fcst)
{
    bool ready = true;
    fcst.Version =   (int)StringToInteger( FileReadString( handle ) );
    fcst.Copyright = FileReadString( handle );
    fcst.SymbolF =   FileReadString( handle );
    fcst.PeriodF =   (int)StringToInteger( FileReadString( handle ) );
    fcst.DigitsF =   (int)StringToInteger( FileReadString( handle ) );
    fcst.StartTS =   StringToTime( FileReadString( handle ) );
    fcst.EndTS =     StringToTime( FileReadString( handle ) );
    fcst.Depth =     (int)StringToInteger( FileReadString( handle ) );
    if( fcst.SymbolF != _Symbol ) ready = false;
    return ready;
};

datetime ReadForcastBar(const int handle, const int depth)
{
    datetime bar = 0, tmp;
    for( int thr = 1; thr <= 3; thr++ ) {
        bar = StringToTime( FileReadString( handle ) );
        for( int i = 0; i < depth; i++ )
            tmp = StringToTime( FileReadString( handle ) );
    }
    return bar;
};

bool ReadForcastTS(const int handle, const ForecastHeader &head, const datetime bar)
{
    datetime tmpBar;
    string sbuffer[11];
    double buffer[11]; ArrayInitialize( buffer, 0.0 );
    int idx = 0;
    tmpBar = StringToTime( FileReadString( handle ) );
    if( tmpBar != bar ) {
        int trLine = head.Depth * 3 + 2;
        for( idx = 0; idx < trLine; idx++ )
            FileReadString( handle );
        return false;
    } else {
        int ctrlBarIdx = GetIndexFromTime( bar );
        ArraysClear( GetIndexFirstBar( _Period ) );
        //ArraySetAsSeries( HighBuffer, true );
        for( idx = 0; idx < head.Depth; idx++ ) {
            HighBuffer[ctrlBarIdx - idx] = StrToDouble( FileReadString( handle ) );
        }
        //ArraySetAsSeries( HighBuffer, false );
        FileReadString( handle ); //time
        for( idx = 0; idx < head.Depth; idx++ ) {
            LowBuffer[ctrlBarIdx - idx] = StrToDouble( FileReadString( handle ) );
        }
        FileReadString( handle ); //time
        for( idx = 0; idx < head.Depth; idx++ ) {
            CloseBuffer[ctrlBarIdx - idx] = StrToDouble( FileReadString( handle ) );
        }
        return true;
    }
};

void ArraysClear(const int depth = 50)
{
    for( int i = 0; i < depth+5; i++ )
        HighBuffer[i] = EMPTY_VALUE;
    for( int i = 0; i < depth+5; i++ )
        LowBuffer[i] = EMPTY_VALUE;
    for( int i = 0; i < depth+5; i++ )
        CloseBuffer[i] = EMPTY_VALUE;
};

long OpenNewWindow(const string symb)
{
    string symbol;
    int period;
    SeparateMasSymbol( symb, symbol, period );
    return ChartOpen( symbol, period );
};

void CloseThisWindow()
{
    ChartClose();
};

int GetSymbolsString(const bool selected, string &symbols)
{
    string symbolsList[];
    int size = GetSymbolsList( selected, symbolsList );
    if( size >= 1 ) {
        symbols = symbolsList[0];
        for( int i = 1; i < size; i++ )
            symbols = StringConcatenate( symbols, ";", symbolsList[i] );
    }
    return size;
};

void SeparateMasSymbol(const string masSymbol, string &symbol, int &period)
{
    int periods[] = {PERIOD_MN1, PERIOD_W1, PERIOD_D1, PERIOD_H4, PERIOD_H1,
                        PERIOD_M30, PERIOD_M15, PERIOD_M5, PERIOD_M1};
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
};

int GetIndexFirstBar(int timeframe = 0)
{
    if( timeframe == PERIOD_D1 )
        return 60;
    else if( timeframe == PERIOD_H4 )
        return 60;
    else if( timeframe == PERIOD_H1 )
        return 60;
    else if( timeframe == PERIOD_M30 )
        return 180;
    else if( timeframe == PERIOD_M15 )
        return 360;
    else if( timeframe == PERIOD_M5 )
        return 360;
    else if( timeframe == PERIOD_M1 )
        return 360;
    else if( timeframe == PERIOD_MN1 )
        return 20;
    return 0;
};

bool SymbolIsTime(const string symb)
{
    if( (symb == "YEAR") || (symb == "MONTH") || (symb == "DAY") || 
        (symb == "YEARDAY") || (symb == "WEEKDAY") || 
        (symb == "HOUR") || (symb == "MINUTE") )
        return true;
    return false;
};

void GetDell(const string name = "mas_")
{
    string vName;
    for(int i=ObjectsTotal()-1; i>=0;i--) {
        vName = ObjectName(i);
        if (StringFind(vName,name) !=-1) ObjectDelete(vName);
    }
};

void SetMyTemplate()
{
    //ChartApplyTemplate( 0, "MAS_Template.tpl" );
};

