//+---------------------------------------------------------------------------+
//|                                                           MAS_Include.mqh |
//|                                          Copyright 2017, Terentew Aleksey |
//|                                 https://www.mql5.com/ru/users/terentjew23 |
//+---------------------------------------------------------------------------+
#property copyright     "Copyright 2017, Terentew Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property strict
//+---------------------------------------------------------------------------+
//| defines                                                                   |
//+---------------------------------------------------------------------------+
#define     COPYRIGHT   "Copyright 2017, Terentew Aleksey"

//+---------------------------------------------------------------------------+
//| Global variables                                                          |
//+---------------------------------------------------------------------------+
ulong       tickCount;

//+---------------------------------------------------------------------------+
//| Functions                                                                 |
//+---------------------------------------------------------------------------+
bool NewBar(const int tf = PERIOD_CURRENT)
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
    /*
    static datetime NewTime=0;
   if(NewTime!=iTime(Symbol(),TF,0))
    {      
     NewTime=iTime(Symbol(),TF,0);
     return(true);
    }
   return(false); */
};

double Impulse(const int bar, const int period = PERIOD_CURRENT,
               const int pEMA = 13, const int pMACD_F = 12, 
               const int pMACD_S = 26, const int pMACD_Sig = 9)
{
    double ema0 = iMA( NULL, period, pEMA, 0, MODE_EMA, PRICE_CLOSE, bar );
    double ema1 = iMA( NULL, period, pEMA, 0, MODE_EMA, PRICE_CLOSE, bar+1 );
    double macd0 = iMACD( NULL, period, pMACD_F, pMACD_S, pMACD_Sig, PRICE_CLOSE, MODE_MAIN, bar );
    double macd1 = iMACD( NULL, period, pMACD_F, pMACD_S, pMACD_Sig, PRICE_CLOSE, MODE_MAIN, bar+1 );
    if( ema0 > ema1 && macd0 > macd1 )
        return 1.0;         // Buy
    if( ema0 < ema1 && macd0 < macd1 )
        return -1.0;        // Sell
    return 0.0;
};

int GetIndexFromTime(const datetime time_bar, 
                     const int period = 0, const string symbol = NULL)
{
    int index = Bars( symbol, period, iTime(symbol, period,0), time_bar );
//    while( iTime( symbol, period, index ) >= time )
//        index++;
    return index;
};

ENUM_TIMEFRAMES GetMorePeriod(const ENUM_TIMEFRAMES period){
    int tmp = period == 0 ? Period() : period;
    switch( tmp ) {
        case PERIOD_M1:  return(PERIOD_M5);
        case PERIOD_M5:  return(PERIOD_M15);
        case PERIOD_M15: return(PERIOD_M30);
        case PERIOD_M30: return(PERIOD_H1);
        case PERIOD_H1:  return(PERIOD_H4);
        case PERIOD_H4:  return(PERIOD_D1);
        case PERIOD_D1:  return(PERIOD_W1);
        case PERIOD_W1:  return(PERIOD_MN1);
        case PERIOD_MN1: return(PERIOD_MN1);
        default:         return(PERIOD_CURRENT);
    }
};

ENUM_TIMEFRAMES GetLessPeriod(const ENUM_TIMEFRAMES period){
    int tmp = period == 0 ? Period() : period;
    switch( tmp ) {
        case PERIOD_M1:  return(PERIOD_M1);
        case PERIOD_M5:  return(PERIOD_M1);
        case PERIOD_M15: return(PERIOD_M5);
        case PERIOD_M30: return(PERIOD_M15);
        case PERIOD_H1:  return(PERIOD_M30);
        case PERIOD_H4:  return(PERIOD_H1);
        case PERIOD_D1:  return(PERIOD_H4);
        case PERIOD_W1:  return(PERIOD_D1);
        case PERIOD_MN1: return(PERIOD_W1);
        default:         return(PERIOD_CURRENT);
    }
};

int GetSymbolsList(const bool selected, string &symbols[])
{
    string symbolsFileName;
    int symbolsNumber, offset;
    if( selected ) 
        symbolsFileName = "symbols.sel";
    else
        symbolsFileName = "symbols.raw";
    int hFile = FileOpenHistory( symbolsFileName, FILE_BIN|FILE_READ );
    if( hFile < 0 ) 
        return -1;
    if( selected ) {
        symbolsNumber = ( (int)FileSize(hFile) - 4 ) / 128;
        offset = 116;
    } else { 
        symbolsNumber = (int)FileSize(hFile) / 1936;
        offset = 1924;
    }
    ArrayResize( symbols, symbolsNumber );
    if( selected )
        FileSeek( hFile, 4, SEEK_SET );
    for( int i = 0; i < symbolsNumber; i++ ) {
        symbols[i] = FileReadString( hFile, 12 );
        FileSeek( hFile, offset, SEEK_CUR );
    }
    FileClose( hFile );
    return symbolsNumber;
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

double StrToDbl(const string str)
{
    int i, k = 1;
    double r = 0, p = 1;
    for( i = 0; i < StringLen(str); i++ ) {
        if( k < 0 )
			p = p * 10;
        if( StringGetChar( str, i ) == '.' )
            k = -k;
        else
            r = r * 10 + ( StringGetChar( str, i ) - '0' );
    }
    return r / p;
};