//+---------------------------------------------------------------------------+
//|                                                           MAS_Impulse.mq4 |
//|                                          Copyright 2017, Terentew Aleksey |
//|                                 https://www.mql5.com/ru/users/terentjew23 |
//+---------------------------------------------------------------------------+
<<<<<<< HEAD
#property copyright     "Copyright 2017, Terentew Aleksey"
#property link          "https://www.mql5.com/ru/users/terentjew23"
#property description   "Impulse system."
#property description   "Works on any time scale. Send signals to buy and sell."
#property description   "The idea of Alexander Elder."
#property version       "1.1"
#property strict

#include                "MAS_Include.mqh"

//---------------------Indicators---------------------------------------------+
#property indicator_separate_window
#property indicator_minimum -1
#property indicator_maximum 1
=======
#property copyright "Copyright 2017, Terentew Aleksey"
#property link      "https://www.mql5.com/ru/users/terentjew23"
#property version   "1.00"
#property strict
#property indicator_separate_window
>>>>>>> MQL
#property indicator_buffers 2
#property indicator_plots   2
//--- plot
#property indicator_label1  "Buy"
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_color1  clrGreen
#property indicator_style1  STYLE_SOLID
#property indicator_width1  3
#property indicator_label2  "Sell"
#property indicator_type2   DRAW_HISTOGRAM
#property indicator_color2  clrRed
#property indicator_style2  STYLE_SOLID
#property indicator_width2  3
//--- indicator buffers
double      GreenBuffer[];
double      RedBuffer[];
<<<<<<< HEAD

=======
>>>>>>> MQL
//-----------------Global variables-------------------------------------------+
input int   EMA = 13;
input int   MACD_FAST = 12;
input int   MACD_SLOW = 26;
input int   MACD_SIGNAL = 9;

<<<<<<< HEAD
//+---------------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer( 0,GreenBuffer );
    SetIndexBuffer( 1,RedBuffer );
    IndicatorShortName( "Impulse("+IntegerToString(EMA)+","+IntegerToString(MACD_FAST)+","+
                        IntegerToString(MACD_SLOW)+","+IntegerToString(MACD_SIGNAL)+")" );
=======
ulong       tickCount;
//+---------------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer(0,GreenBuffer);
    SetIndexBuffer(1,RedBuffer);
    IndicatorShortName("Impulse("+IntegerToString(EMA)+","+IntegerToString(MACD_FAST)+","+
                        IntegerToString(MACD_SLOW)+","+IntegerToString(MACD_SIGNAL)+")");
>>>>>>> MQL
    if( EMA <= 1 || MACD_FAST <= 1 || MACD_SLOW <= 1 || MACD_SIGNAL <= 1 || MACD_FAST >= MACD_SLOW ) {
        Print( "Wrong input parameters" );
        return( INIT_FAILED );
    }
    return( INIT_SUCCEEDED );
}
<<<<<<< HEAD

=======
>>>>>>> MQL
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
    if( rates_total <= MACD_SIGNAL ) {
        return(0);
    }
    int limit = rates_total - prev_calculated;
    if( prev_calculated > 0 ) {
        limit++;
    }
    for( int i = 0; i < limit; i++ ) {
        GreenBuffer[i] = 0.0;
        RedBuffer[i] = 0.0;
<<<<<<< HEAD
        double tmp = Impulse( i, PERIOD_CURRENT, EMA, MACD_FAST, MACD_SLOW, MACD_SIGNAL );
=======
        double tmp = Impulse( i, EMA, MACD_FAST, MACD_SLOW, MACD_SIGNAL );
>>>>>>> MQL
        if( tmp > 0 )
            GreenBuffer[i] = tmp;
        if( tmp < 0 )
            RedBuffer[i] = tmp;
<<<<<<< HEAD
//        double tmp = Impulse( i, EMA, MACD_FAST, MACD_SLOW, MACD_SIGNAL );
//        if( tmp > 0 )
//            GreenBuffer[i] = Low[i] - iATR(Symbol(),0,21,i)/3;
//        if( tmp < 0 )
//            RedBuffer[i] = High[i] + iATR(Symbol(),0,21,i)/3;
    }
    return( rates_total );
}

=======
    }
    return( rates_total );
}
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
};

double Impulse(const int bar, 
               const int p_ema = 13, const int p_macd1 = 12, 
               const int p_macd2 = 26, const int p_macd3 = 9)
{
    double _ema0 = iMA( NULL, PERIOD_CURRENT, p_ema, 0, MODE_EMA, PRICE_CLOSE, bar );
    double _ema1 = iMA( NULL, PERIOD_CURRENT, p_ema, 0, MODE_EMA, PRICE_CLOSE, bar+1 );
    double _macd0 = iMACD( NULL, PERIOD_CURRENT, p_macd1, p_macd2, p_macd3, PRICE_CLOSE, MODE_MAIN, bar );
    double _macd1 = iMACD( NULL, PERIOD_CURRENT, p_macd1, p_macd2, p_macd3, PRICE_CLOSE, MODE_MAIN, bar+1 );
    if( _ema0 > _ema1 && _macd0 > _macd1 )
        return 1.0;         // Buy
    if( _ema0 < _ema1 && _macd0 < _macd1 )
        return -1.0;        // Sell
    return 0.0;
}
>>>>>>> MQL
