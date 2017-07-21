#include "include/settingsstruct.h"
#include <QApplication>
#include <QDir>

void ConfigMT4::rename(const QString newName) {
    if( nameKit != newName ) {
        renamePath( newName );
        nameKit = newName;
    }
}

void ConfigMT4::removePath(QString path) {
    QDir dir( path );
    QStringList lstDirs = dir.entryList( QDir::Dirs|QDir::AllDirs|QDir::NoDotAndDotDot );
    QStringList lstFiles = dir.entryList(QDir::Files);
    foreach( QString entry, lstFiles ) {
        QString entryAbsPath = dir.absolutePath() + "/" + entry;
        QFile::setPermissions(entryAbsPath, QFile::ReadOwner | QFile::WriteOwner);
        QFile::remove(entryAbsPath);
    }
    foreach (QString entry, lstDirs) {
        QString entryAbsPath = dir.absolutePath() + "/" + entry;
        removePath( entryAbsPath );
    }
    QDir().rmdir( dir.absolutePath() );
}

bool ConfigMT4::isTimeSymbol(QString symbol) {
    foreach( auto time, symbolsOfTime )
        if( symbol == time )
            return true;
    return false;
}

void ConfigMT4::updateServerParameters() {
    setServer();
//    setSymbols();
}

qint32 ConfigMT4::sumInput()
{
    qint32 res = 0;
    foreach( QString in, input ) {
        if( isTimeSymbol( in ) ) {
            res += 1;
        } else {
            res += recurrentModel ? 4 : 4 * depthHistory;
            if( readVolume )
                res += recurrentModel ? 1 : depthHistory;
        }
    }
    return res;
}

qint32 ConfigMT4::sumOutput()
{
    qint32 res = 0;
    foreach( QString out, output ) {
        if( isTimeSymbol( out ) ) {
            res += 1;
        } else {
            res += 3 * depthPrediction;
        }
    }
    return res;
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
    removePath( kitPath );
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

void ConfigMT4::setTrainingMethods() {
    trainingMethods.append( "Random Search" );
    trainingMethods.append( "Gradient Descent" );
    trainingMethods.append( "Newton Method" );
    trainingMethods.append( "Conjugate Gradient" );
    trainingMethods.append( "Quasi Newton Method" );
    trainingMethods.append( "Evolutionary Algorithm" );
    trainingMethods.append( "Levenberg Marquardt Algorithm" );
    trainingMethod = "Quasi Newton Method";
}
