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
    QString nameKit;
    QString kitPath;
    QString mt4Path = "C:/";
    QString server;
    QString historyPath = "/history/"; // default ?
    const QString configFile = "/MQL4/Files/mas_mt4.conf";
    const QString newHistoryPath = "/MQL4/Files/MAS_MarketData/h";
    const QString predictionPath = "/MQL4/Files/MAS_Prediction/p";
    QList<qint32> periods;
    bool volumeIn = false;
    QStringList input;
    QStringList output;
    qint32 depthHistory = 1;
    qint32 depthPrediction = 1;
    qint32 layersCount = 1;
    qint32 layersSize[10] = { 10 };
    QString trainingModel;
    qint32 divideInstances[3] = { 60, 20, 20 };
    //QDateTime lastTraining;
    bool isLoaded = false;
    bool isReady = false;
    bool isTrained = false;
    bool isRun = false;
    qint32 progress = 0;
    QStringList servers;
    QStringList symbols;
    QStringList symbolsOfTime;
    QStringList trainingModels;
//===========Functions==============================
    void rename(const QString newName) {
        if( nameKit != newName ) {
            renamePath( newName );
            nameKit = newName;
        }
    }
    void remove() {
//        if( !QDir().exists(kitPath) )
//            QDir().rmdir( kitPath );
    }
    bool isTimeSymbol(QString symbol) {
        foreach( auto time, symbolsOfTime )
            if( symbol == time )
                return true;
        return false;
    }
    void updateServerParameters() {
        //setPath();
        setServer();
        setSymbols();
    }
private:
    void setPath(void) {
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
    void setServer(void) {
        if( mt4Path.size() <= 5 )
            return;
        QDir path( QString("%1%2").arg( mt4Path, "/history" ) );
        QStringList files = path.entryList( QDir::Dirs );
        files.removeOne( "default" );
        files.removeOne( "deleted" );
        files.removeOne( "mailbox" );
        files.removeOne( "signals" );
        files.removeOne( "symbolsets" );
        files.removeOne( "." );
        files.removeOne( ".." );
        servers = files;
        if( server == "" )
            if( !server.isEmpty() )
                server = servers.first();
    }
    void setSymbols(void) {
        symbols.clear();
        // read mas_mt4.conf
        symbols.append("EURUSD.pro");
        symbols.append("GBPUSD.pro");
        symbols.append("USDJPY.pro");
        symbols.append("AUDUSD.pro");
        symbols.append("S&P500");
        symbols.append("DAX");
        symbols.append("FTSE100");
        symbols.append("BRENT");
        symbols.append("XAUUSD.pro");
    }
    void setSymbolsOfTime(void) {
        symbolsOfTime.append("YEAR");
        symbolsOfTime.append("MONTH");
        symbolsOfTime.append("DAY");
        symbolsOfTime.append("YEARDAY");
        symbolsOfTime.append("HOUR");
        symbolsOfTime.append("MINUTE");
        symbolsOfTime.append("WEEKDAY");
    }
    void setModels(void) {
        trainingModels.append( "Random Search" );
        trainingModels.append( "Gradient Descent" );
        trainingModels.append( "Newton Method" );
        trainingModels.append( "Conjugate Gradient" );
        trainingModels.append( "Quasi Newton Method" );
        trainingModels.append( "Evolutionary Algorithm" );
        trainingModels.append( "Levenberg Marquardt Algorithm" );
        trainingModel = "Quasi Newton Method";
    }
};

#endif // SETTINGSSTRUCT_H
