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
    if( kitConfigFile )
        delete kitConfigFile;
}

SettingsMAS &SettingsMAS::Instance()
{
    static SettingsMAS singleInstance;
    return singleInstance;
}

void SettingsMAS::load(Settings *settings)
{
    settings->maxOpenTabs = global->value( sKeys.maxTabs ).toInt();
    qint32 size = global->value( sKeys.savedSize, 0 ).toInt();
    for( qint32 i = 0; i < size; i++ )
        settings->savedKitsList
                .append( global->value( QString("%1%2")
                                        .arg( sKeys.savedKit )
                                        .arg( i ), "" ).toString() );
    size = global->value( sKeys.lastSize, 0 ).toInt();
    for( qint32 i = 0; i < size; i++ )
        settings->sessionList
                .append( global->value( QString("%1%2")
                                        .arg( sKeys.lastKit )
                                        .arg( i ), "" ).toString() );
    settings->winPosX = global->value( sKeys.posX ).toInt();
    settings->winPosY = global->value( sKeys.posY ).toInt();
    settings->winSizeX = global->value( sKeys.sizeX ).toInt();
    settings->winSizeY = global->value( sKeys.sizeY ).toInt();
    settings->savedKitsList.removeAll("");
    settings->sessionList.removeAll("");
}

void SettingsMAS::save(const Settings *settings)
{
    global->setValue( sKeys.maxTabs, settings->maxOpenTabs );
    global->setValue( sKeys.savedSize, settings->savedKitsList.size() );
    for( qint32 i = 0; i < settings->savedKitsList.size(); i++)
        global->setValue( QString("%1%2").arg( sKeys.savedKit ).arg( i ),
                          settings->savedKitsList[i] );
    global->setValue( sKeys.lastSize, settings->sessionList.size() );
    for( qint32 i = 0; i < settings->sessionList.size(); i++)
        global->setValue( QString("%1%2").arg( sKeys.lastKit ).arg( i ),
                          settings->sessionList[i] );
    global->setValue( sKeys.posX, settings->winPosX );
    global->setValue( sKeys.posY, settings->winPosY );
    global->setValue( sKeys.sizeX, settings->winSizeX );
    global->setValue( sKeys.sizeY, settings->winSizeY );
}

void SettingsMAS::load(ConfigMT4 *configKit)
{
    if( configKit->nameKit.contains( "New Market Kit" ) )
        loadDefault( configKit );


    //emit loaded( configKit->nameKit );
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
