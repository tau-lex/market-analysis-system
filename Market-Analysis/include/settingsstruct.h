#ifndef SETTINGSSTRUCT_H
#define SETTINGSSTRUCT_H

#include <QObject>
#include <QApplication>
#include <QDir>
//#include <QDateTime>

struct Settings {
    qint32          maxOpenTabs = 5;
    QStringList     savedKitsList;
    QStringList     sessionList;
    //QString         defaultKit = "default";
    qint32          winPosX;
    qint32          winPosY;
    qint32          winSizeX;
    qint32          winSizeY;
};

struct ConfigMT4 {
    ConfigMT4(QString name) : nameKit( name ) {
        setPath();
    }
    QString nameKit;
    QString kitPath;
    QString mt4Path = "C:/Program Files (x86)/STForex MetaTrader 4"; // default "C:\\"
    QString historyPath = "/history/STForex-Live/"; // default ?
    const QString configFile = "/MQL4/Files/mas_mt4.conf";
    const QString newHistoryPath = "/MQL4/Files/MAS_MarketData/h";
    const QString predictionPath = "/MQL4/Files/MAS_Prediction/p";
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
    bool isLoaded = false;
    bool isRun = false;
    bool isTrained = true;
    qint32 progress = 0;
    //=======Functions=======
    void rename(const QString newName) {
        renamePath( newName );
        nameKit = newName;
    }
    void remove() {
//        if( !QDir().exists(kitPath) )
//            QDir().rmdir( kitPath );
    }

private:
    void setPath() {
        QString mDir = QApplication::applicationDirPath();
        mDir += "/Market Kits/";
        mDir += nameKit;
        if( !QDir().exists(mDir) )
            QDir().mkdir( mDir );
        //else
        //    throw;
    }
    void renamePath(const QString newName) {
        QString mDir = QApplication::applicationDirPath();
        mDir += "/Market Kits/";
        QString mDir1 = mDir + nameKit;
        QString mDir2 = mDir + newName;
        if( !QDir().exists(mDir1) )
            QDir().rename( mDir1, mDir2 );
        //else
        //    throw;
    }
};

#endif // SETTINGSSTRUCT_H
