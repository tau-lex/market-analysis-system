//+---------------------------------------------------------------------------+
//|                                                      MASi_ImpulseHist.mq4 |
//|                                         Copyright 2017, Terentyev Aleksey |
//|                                 https://www.mql5.com/ru/users/terentyev23 |
//+---------------------------------------------------------------------------+
#property copyright     "Copyright 2017, Terentyev Aleksey"
#property link          "https://www.mql5.com/ru/users/terentyev23"
#property description   "Impulse system."
#property description   "Works on any time scale. Send signals to buy and sell."
#property description   "The idea of Alexander Elder."
#property version       "1.2"
#property strict

//---------------------Indicators---------------------------------------------+
#property indicator_separate_window
//#property indicator_height  50
#property indicator_minimum -1
#property indicator_maximum 1
#property indicator_buffers 4
#property indicator_plots   4
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
#property indicator_label3  ""
#property indicator_type3   DRAW_HISTOGRAM
#property indicator_color3  clrDimGray
#property indicator_style3  STYLE_SOLID
#property indicator_width3  3
#property indicator_label4  "Sell"
#property indicator_type4   DRAW_HISTOGRAM
#property indicator_color4  clrDimGray
#property indicator_style4  STYLE_SOLID
#property indicator_width4  3
//--- indicator buffers
double      GreenBuffer[], RedBuffer[];
double      Gray1Buffer[], Gray2Buffer[];

//-----------------Global variables-------------------------------------------+
//---
input int   EMA = 13;           // EMA 
input int   MACD_FAST = 12;     // MACD Fast
input int   MACD_SLOW = 26;     // MACD Slow
input int   MACD_SIGNAL = 9;    // MACD Signal
input bool  ON_GREYBAR = false; // Enable neutral signal
//---

//+---------------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer( 0, GreenBuffer );
    SetIndexBuffer( 1, RedBuffer );
    if( ON_GREYBAR ) {
        SetIndexBuffer( 2, Gray1Buffer );
        SetIndexBuffer( 3, Gray2Buffer );
    }
    IndicatorShortName( "Impulse (" + IntegerToString(EMA) + ", " + IntegerToString(MACD_FAST) + ", " +
                        IntegerToString(MACD_SLOW) + ", " + IntegerToString(MACD_SIGNAL) + " )" );
    if( EMA <= 1 || MACD_FAST <= 1 || MACD_SLOW <= 1 || MACD_SIGNAL <= 1 || MACD_FAST >= MACD_SLOW ) {
        Print( "Wrong input parameters" );
        return INIT_FAILED;
    }
    return INIT_SUCCEEDED;
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
    if( rates_total <= MACD_SIGNAL ) {
        return rates_total - 1;
    }
    int limit = rates_total - prev_calculated;
    if( prev_calculated > 0 ) {
        limit++;
    }
    for( int idx = 0; idx < limit; idx++ ) {
        GreenBuffer[idx] = 0.0;
        RedBuffer[idx] = 0.0;
        double tmp = Impulse( idx, NULL, PERIOD_CURRENT, EMA, MACD_FAST, MACD_SLOW, MACD_SIGNAL );
        if( tmp > 0 ) {
            GreenBuffer[idx] = tmp;
        } else if( tmp < 0 ) {
            RedBuffer[idx] = tmp;
        } else if( ON_GREYBAR ) {   // Size of gray bars
            Gray1Buffer[idx] = 0.5; 
            Gray2Buffer[idx] = -0.5;
        }
    }
    return rates_total;
}

//+---------------------------------------------------------------------------+
double Impulse(const int bar, 
               const string symbol = NULL, const int period = PERIOD_CURRENT,
               const int pEMA = 13, const int pMACD_F = 12, 
               const int pMACD_S = 26, const int pMACD_Sig = 9)
{   // Impulse indicator.  ©Alexander Elder
    double ema0 = iMA( symbol, period, pEMA, 0, MODE_EMA, PRICE_CLOSE, bar );
    double ema1 = iMA( symbol, period, pEMA, 0, MODE_EMA, PRICE_CLOSE, bar+1 );
            // iOsMA or Origin MACD Histogram
    double macd0 = iOsMA( symbol, period, pMACD_F, pMACD_S, pMACD_Sig, PRICE_CLOSE, bar );
    double macd1 = iOsMA( symbol, period, pMACD_F, pMACD_S, pMACD_Sig, PRICE_CLOSE, bar+1 );
    if( ema1 < ema0 && macd1 < macd0 )
        return 1.0;         // Impulse Up
    if( ema1 > ema0 && macd1 > macd0 )
        return -1.0;        // Impulse Down
    return 0.0;
}

