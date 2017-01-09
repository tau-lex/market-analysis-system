#ifndef SETTINGSSTRUCT_H
#define SETTINGSSTRUCT_H

#include <QObject>
#include <QDateTime>

struct Settings {
    qint32          maxOpenTabs = 5;
    QStringList     savedKits;
    QStringList     session;
    qint32          winPosX;
    qint32          winPosY;
    qint32          winSizeX;
    qint32          winSizeY;
};

struct ConfigMT4 {
    ConfigMT4(QString name) : nameKit( name ) {
        setPath(); setModels(); setSymbolsOfTime();
    }
    ~ConfigMT4() { }
    QString         nameKit;
    QString         kitPath;
    QString         mt4Path = "C:/";
    QString         server;
    QString         historyPath = "/history/"; // default ?
    const QString   configFile = "/MQL4/Files/mas_mt4.conf";
    const QString   newHistoryPath = "/MQL4/Files/MAS_MarketData/h";
    const QString   predictionPath = "/MQL4/Files/MAS_Prediction/p";
    QList<qint32>   periods;
    bool            volumeIn = false;
    QStringList     input;
    QStringList     output;
    qint32          depthHistory = 1;
    qint32          depthPrediction = 1;
    qint32          layersCount = 1;
    qint32          layersSize[10] = { 10 };
    QString         trainingModel;
    qint32          divideInstances[3] = { 60, 20, 20 };
    QDateTime       lastTraining;
    bool            isLoaded = false;
    bool            isReady = false;
    bool            isTrained = false;
    bool            isRun = false;
    qint32          progress = 0;
    QStringList     servers;
    QStringList     symbols;
    QStringList     symbolsOfTime;
    QStringList     trainingModels;
//===========Functions==============================
    void rename(const QString newName);
    void remove();
    bool isTimeSymbol(QString symbol);
    void updateServerParameters();
private:
    void setPath(void);
    void renamePath(const QString newName);
    void setServer(void);
    void setSymbols(void);
    void setSymbolsOfTime(void);
    void setModels(void);
};

#endif // SETTINGSSTRUCT_H
