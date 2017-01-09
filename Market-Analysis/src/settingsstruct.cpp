#include "include/settingsstruct.h"
#include <QApplication>
#include <QDir>


void ConfigMT4::rename(const QString newName) {
    if( nameKit != newName ) {
        renamePath( newName );
        nameKit = newName;
    }
}

void ConfigMT4::remove() {
    QDir rm( kitPath );
    rm.removeRecursively();
}

bool ConfigMT4::isTimeSymbol(QString symbol) {
    foreach( auto time, symbolsOfTime )
        if( symbol == time )
            return true;
    return false;
}

void ConfigMT4::updateServerParameters() {
    //setPath();
    setServer();
    setSymbols();
}

void ConfigMT4::setPath() {
    QString mDir = QApplication::applicationDirPath();
    mDir += "/Market Kits/";
    mDir += nameKit;
    if( !QDir().exists(mDir) )
        QDir().mkdir( mDir );
    kitPath = mDir;
}

void ConfigMT4::renamePath(const QString newName) {
    QString mDir2 = QApplication::applicationDirPath();
    mDir2 += "/Market Kits/";
    mDir2 += newName;
    if( !QDir().exists(kitPath) )
        QDir().rename( kitPath, mDir2 );
    kitPath = mDir2;
}

void ConfigMT4::setServer() {
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

void ConfigMT4::setSymbols() {
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

void ConfigMT4::setSymbolsOfTime() {
    symbolsOfTime.append("YEAR");
    symbolsOfTime.append("MONTH");
    symbolsOfTime.append("DAY");
    symbolsOfTime.append("YEARDAY");
    symbolsOfTime.append("HOUR");
    symbolsOfTime.append("MINUTE");
    symbolsOfTime.append("WEEKDAY");
}

void ConfigMT4::setModels() {
    trainingModels.append( "Random Search" );
    trainingModels.append( "Gradient Descent" );
    trainingModels.append( "Newton Method" );
    trainingModels.append( "Conjugate Gradient" );
    trainingModels.append( "Quasi Newton Method" );
    trainingModels.append( "Evolutionary Algorithm" );
    trainingModels.append( "Levenberg Marquardt Algorithm" );
    trainingModel = "Quasi Newton Method";
}
