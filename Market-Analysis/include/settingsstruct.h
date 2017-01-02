#ifndef SETTINGSSTRUCT_H
#define SETTINGSSTRUCT_H

#include <QObject>
#include <QDateTime>

struct Settings {
    qint32      maxOpenTabs;
    QStringList sessionList;
    QString defaultKit = "default";
};

struct ConfigMT4 {
    QString nameKit = "default";
    QString kitPath;
    QString mt4Path = "C:\\Program Files (x86)\\STForex MetaTrader 4"; // default "C:\\"
    QString historyPath = "\\history\\STForex-Live\\"; // default ?
    const QString configFile = "\\MQL4\\Files\\mas_mt4.conf";
    const QString newHistoryPath = "\\MQL4\\Files\\MAS_MarketData\\";
    const QString predictionPath = "\\MQL4\\Files\\MAS_Prediction\\";
    QString server = "STForex-Live";

    qint32 period = 1440;
    bool volumeIn = false;
    QStringList input;
    QStringList output;
    qint32 depthHistory = 1;
    qint32 depthPrediction = 1;
    qint32 layersCount = 3;
    qint32 layersSize[3] = { 21, 11, 6 };
    qint32 divideInstances[3] = { 60, 20, 20 };
    //QDateTime lastTraining;
    bool isRun = false;
    bool isTrained = false;
    qint32 progress = 0;
};

#endif // SETTINGSSTRUCT_H
