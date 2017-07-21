//+---------------------------------------------------------------------------+
//|                                                  MASs_DataSetPreparer.mq4 |
//|                                          Copyright 2017, Terentew Aleksey |
//|                                 https://www.mql5.com/ru/users/terentjew23 |
//+---------------------------------------------------------------------------+
#property copyright     "Copyright 2016-2017, Terentew Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property description   "MASs_DataSetPreparer"
#property description   "The script saves the historical data for the parameters specified in the configuration file."
#property description   "I recommend this script https://www.mql5.com/ru/code/15022"
#property version       "1.0"
#property strict

//-----------------Global variables-------------------------------------------+
input string    configFile = "MASs_DataSetPreparer.conf";
input string    csvSeparator = ";";
string      modelList[1][64];
int         fullData;
string      symbolsList[20][64];
int         periodsList[10];
string      indicatorsList[10][64];

//+----------------Main funtion-----------------------------------------------+
void OnStart()
{
    loadConfigFile();
    
    saveHistoryFiles();
}

//+----------------Functions--------------------------------------------------+
int loadConfigFile()
{
    bool mainSection = false;
    int handle;
    string buffer, temp;
    handle = FileOpen( configFile, FILE_READ | FILE_SHARE_READ | FILE_TXT );
    if( handle != INVALID_HANDLE ) {
        while( !FileIsEnding( handle ) ) {
            buffer = FileReadString( handle );
            if( StringFind( buffer, "[Main]" ) >= 0 ) {
                mainSection = true;
                continue;
            }
            if( StringFind( buffer, "Model_Names=" ) >= 0 && mainSection ) {
                temp = StringSubstr( buffer, 12 );
		        StringReplace( temp, "\"", "" );
                StringSplitMAS( temp, ';', modelList );
                mainSection = false;
                continue;
            }
            for( int i = 0; i < ArrayRange(modelList,0); i++ ) {
                if( StringFind( buffer, StringConcatenate( "[", modelList[i][0], "]" ) ) >= 0 ) {
                    buffer = FileReadString( handle );
                    while( modelReadParameters( buffer ) ) {
                        buffer = FileReadString( handle );
                    }
                }
            }
            if( StringFind( buffer, "#" ) >= 0 ) {
                continue;
            }
        }
        FileClose( handle );
    } else {
        PrintFormat( "err: Config file not open. %d", GetLastError() );
        return 1;
    }
    return 0;
};

void saveHistoryFiles()
{
    for( int model = 0; model < ArrayRange(modelList,0); model++ ) {
        for( int symb = 0; symb < ArrayRange(symbolsList,0); symb++ ) {
            for( int tf = 0; tf < ArraySize(periodsList); tf++ ) {
                if( periodsList[tf] == 0 ) continue;
                string fileName = StringConcatenate( modelList[model][0], "/", 
                                        symbolsList[symb][0], periodsList[tf], ".csv" );
                saveHistory( symbolsList[symb][0], periodsList[tf], fileName );
                /*for( int ind = 0; ind < ArrayRange(indicatorsList,0); ind++ ){
                    fileName = StringConcatenate( modelList[model][0], "/", 
                                            symbolsList[symb][0], periodsList[tf], 
                                            indicatorsList[ind][0], ".csv" );
                    saveIndHistory( symbolsList[symb][0], periodsList[tf], indicatorsList[ind][0], fileName );
                } */
            }
        }
    }
};

void saveHistory(const string &symbol, const int &timeframe, const string &file)
{
    ushort  csvSep = StringGetChar( csvSeparator, 0 );
    int     digits = (int)MarketInfo( symbol, MODE_DIGITS );
    int     limit, csvFile;
    if( fullData )
        limit = iBars( symbol, timeframe ) - 1;
    else
        limit = GetIndexFirstBar( timeframe );
    csvFile = FileOpen( file, FILE_WRITE | FILE_CSV, csvSep );
    //FileWrite( csvFile, 401, Copyright, symbol, timeframe, (int)MarketInfo( symbol, MODE_DIGITS ), 
    //            iTime( symbol, timeframe, limit - 1 ), iTime( symbol, timeframe, 0 ) );
    for( int i = limit - 1; i >= 0; i-- ) {
        FileSeek( csvFile, 0, SEEK_END );
        FileWrite( csvFile, iTime( symbol, timeframe, i ), 
                            DoubleToStr( iOpen(  symbol, timeframe, i ), digits ), 
                            DoubleToStr( iHigh(  symbol, timeframe, i ), digits ), 
                            DoubleToStr( iLow(   symbol, timeframe, i ), digits ), 
                            DoubleToStr( iClose( symbol, timeframe, i ), digits ), 
                            iVolume(_Symbol, timeframe, i) );
    }
    FileClose( csvFile );
};

void saveIndHistory(const string &symbol, const int &timeframe, const string &indicator, const string &file)
{
    ushort  csvSep = StringGetChar( csvSeparator, 0 );
    int     limit, csvFile;
    if( fullData )
        limit = iBars( symbol, timeframe ) - 1;
    else
        limit = GetIndexFirstBar( timeframe );
    csvFile = FileOpen( file, FILE_WRITE | FILE_CSV, csvSep );
    //FileWrite( csvFile, 401, Copyright, symbol, timeframe, (int)MarketInfo( symbol, MODE_DIGITS ), 
    //            iTime( symbol, timeframe, limit - 1 ), iTime( symbol, timeframe, 0 ) );
    for( int i = limit - 1; i >= 0; i-- ) {
        FileSeek( csvFile, 0, SEEK_END );
        FileWrite( csvFile, "" );
    }
    FileClose( csvFile );
};

bool modelReadParameters(const string &line)
{
    string temp;
    if( StringFind( line, "Full_Data=" ) >= 0 ) {
        temp = StringSubstr( line, 10 );
        fullData = StringToInteger( temp );
        return true;
    }
    if( StringFind( line, "Periods=" ) >= 0 ) {
        temp = StringSubstr( line, 8 );
		StringReplace( temp, "\"", "" );
		string tempList[][64];
        StringSplitMAS( temp, ';', tempList );
        for( int i = 0; i < ArrayRange(tempList,0); i++ )
            periodsList[i] = StringToInteger( tempList[i][0] );
        return true;
    }
    if( StringFind( line, "Symbols=" ) >= 0 ) {
        temp = StringSubstr( line, 8 );
		StringReplace( temp, "\"", "" );
        StringSplitMAS( temp, ';', symbolsList );
        return true;
    }
    if( StringFind( line, "Indicators=" ) >= 0 ) {
        temp = StringSubstr( line, 11 );
		StringReplace( temp, "\"", "" );
        //StringSplitMAS( temp, ';', indicatorsList );
        return true;
    }
    return false;
};

int StringSplitMAS(const string string_value, const ushort separator, string &result[][64])
{
    if( StringLen( string_value ) <= 0 || string_value == NULL )
        return 0;
    int lastChar = 0, currentChar = 0, size = StringLen(string_value), sizeRes = 0, sepIdxs[50];
    ArrayInitialize( sepIdxs, 0 );
    for( int idx = 0; idx < size; idx++) {
        if( StringGetChar(string_value, idx) == separator ) {
            sepIdxs[sizeRes] = idx;
            sizeRes += 1;
            if( sizeRes >= ArraySize(sepIdxs) )
                ArrayResize( sepIdxs, ArraySize(sepIdxs) + 50 );
        }
    }
    ArrayResize( result, sizeRes + 1 );
    if( sizeRes == 0 ) {
        result[sizeRes][0] = string_value;
        return sizeRes + 1;
    }
    for( int idx = 0; idx <= sizeRes; idx++) {
        if( idx == 0 ) {
            result[idx][0] = StringSubstr( string_value, 0, sepIdxs[idx] );
            continue;
        }
        result[idx][0] = StringSubstr( string_value, sepIdxs[idx-1] + 1, 
                                                     sepIdxs[idx] - sepIdxs[idx-1] - 1 );
    }
    return sizeRes + 1;
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

int GetIndexFromTime(const datetime time, const int timeframe = 0)
{
    int index = 0;
    while( iTime( _Symbol, timeframe, index ) >= time )
        index++;
    return index;
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

