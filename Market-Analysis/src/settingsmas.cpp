#include "include/settingsmas.h"
#include <QApplication>
#include <QSettings>
#include <QVariant>

SettingsMAS::SettingsMAS(QObject *parent) : QObject(parent)
{
    global = new QSettings( QApplication::organizationName(),
                            QApplication::applicationName(),
                            this );
}

SettingsMAS::~SettingsMAS()
{
    if( global )
        delete global;
    if( kitFile )
        delete kitFile;
}

SettingsMAS &SettingsMAS::Instance()
{
    static SettingsMAS singleInstance;
    return singleInstance;
}

void SettingsMAS::load(Settings *settings)
{
    settings->maxOpenTabs = global->value( _s.maxTabs ).toInt();
    qint32 size = global->value( _s.savedSize, 0 ).toInt();
    for( qint32 i = 0; i < size; i++ )
        settings->savedKits.append( global->value( QString("%1%2")
                                                   .arg( _s.savedKit )
                                                   .arg( i ) ).toString() );
    size = global->value( _s.lastSize, 0 ).toInt();
    for( qint32 i = 0; i < size; i++ )
        settings->session.append( global->value( QString("%1%2")
                                                     .arg( _s.lastKit )
                                                     .arg( i ) ).toString() );
    settings->winPosX = global->value( _s.posX ).toInt();
    settings->winPosY = global->value( _s.posY ).toInt();
    settings->winSizeX = global->value( _s.sizeX ).toInt();
    settings->winSizeY = global->value( _s.sizeY ).toInt();
    settings->savedKits.removeAll("");
    settings->session.removeAll("");
}

void SettingsMAS::save(const Settings *settings)
{
    clear();
    global->setValue( _s.maxTabs, settings->maxOpenTabs );
    global->setValue( _s.savedSize, settings->savedKits.size() );
    for( qint32 i = 0; i < settings->savedKits.size(); i++)
        global->setValue( QString("%1%2").arg( _s.savedKit ).arg( i ),
                          settings->savedKits[i] );
    global->setValue( _s.lastSize, settings->session.size() );
    for( qint32 i = 0; i < settings->session.size(); i++)
        global->setValue( QString("%1%2").arg( _s.lastKit ).arg( i ),
                          settings->session[i] );
    global->setValue( _s.posX, settings->winPosX );
    global->setValue( _s.posY, settings->winPosY );
    global->setValue( _s.sizeX, settings->winSizeX );
    global->setValue( _s.sizeY, settings->winSizeY );
}

void SettingsMAS::load(ConfigMT4 *configKit)
{
    if( configKit->nameKit.contains( "New Market Kit" ) ) {
        loadDefault( configKit );
        return;
    }
    kitFile = new QSettings( QString("%1/%2").arg( configKit->kitPath )
                             .arg( "config.ini" ), QSettings::IniFormat);
//    configKit->nameKit = kitFile->;
//    configKit->kitPath;
//    configKit->mt4Path;
//    configKit->server;
//    configKit->historyPath;
//    configKit->configFile;
//    configKit->newHistoryPath;
//    configKit->predictionPath;
//    configKit->periods;
//    configKit->volumeIn;
//    configKit->input;
//    configKit->output;
//    configKit->depthHistory;
//    configKit->depthPrediction;
//    configKit->layersCount;
//    configKit->layersSize;
//    configKit->trainingModel;
//    configKit->divideInstances;
//    configKit->lastTraining;
//    configKit->isLoaded;
//    configKit->isReady;
//    configKit->isTrained;
//    configKit->isRun;
//    configKit->progress;
//    configKit->servers;
//    configKit->symbols;
//    configKit->symbolsOfTime;
//    configKit->trainingModels;

}

void SettingsMAS::save(const ConfigMT4 *configKit)
{
    configKit;
}

void SettingsMAS::deleteMAKit(ConfigMT4 *configKit)
{
    // del configs in mas_mt4.conf
    // del conf
    configKit->remove();
}

void SettingsMAS::loadDefault(ConfigMT4 *configKit)
{
    configKit->input.append("EURUSD.pro1440");
    configKit->input.append( "YEAR" );
    configKit->input.append( "MONTH" );
    configKit->input.append( "DAY" );
    configKit->input.append( "HOUR" );
    configKit->input.append( "WEEKDAY" );
    configKit->output.append("EURUSD.pro1440");
    configKit->layersCount = 1;
    configKit->layersSize[0] = 9;
}

void SettingsMAS::clear()
{
    qint32 idx = 0;
    while( global->contains( QString("%1%2").arg( _s.savedKit ).arg( idx ) ) ) {
        global->remove( QString("%1%2").arg( _s.savedKit ).arg( idx ) );
        idx++;
    }
    idx = 0;
    while( global->contains( QString("%1%2").arg( _s.lastKit ).arg( idx ) ) ) {
        global->remove( QString("%1%2").arg( _s.lastKit ).arg( idx ) );
        idx++;
    }
}
