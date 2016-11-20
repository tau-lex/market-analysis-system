//+------------------------------------------------------------------+
//|                                                MAS_Assistant.mq4 |
//|                                 Copyright 2016, Terentew Aleksey |
//|                        https://www.mql5.com/ru/users/terentjew23 |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Terentew Aleksey"
#property link      "https://www.mql5.com/ru/users/terentjew23"
#property version   "0.1"
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
double         Forecast_OpenBuffer[];
double         Forecast_CloseBuffer[];
double         Real_OpenBuffer[];
double         Real_CloseBuffer[];


//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
//--- indicator buffers mapping
   SetIndexBuffer(0,Forecast_OpenBuffer);
   SetIndexBuffer(1,Forecast_CloseBuffer);
   SetIndexBuffer(2,Real_OpenBuffer);
   SetIndexBuffer(3,Real_CloseBuffer);
   
//---
   return(INIT_SUCCEEDED);
}
  
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
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
   WriteFile();
   ReadFile();
   IndicatorsUpdate();
   
//--- return value of prev_calculated for next call
   return(rates_total);
}

//+------------------------------------------------------------------+
//| Functions                                                        |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
void WriteFile()
{

}

//+------------------------------------------------------------------+
void ReadFile()
{

}

//+------------------------------------------------------------------+
void IndicatorsUpdate()
{

}