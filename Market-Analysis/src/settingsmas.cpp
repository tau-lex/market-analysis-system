#include "include/settingsmas.h"
#include <QSettings>
#include <QVector>

SettingsMAS::SettingsMAS(QObject *parent) : QObject(parent)
{ }

SettingsMAS &SettingsMAS::Instance()
{
    static SettingsMAS singleInstance;
    return singleInstance;
}

void SettingsMAS::load(Settings *settings)
{
    settings->sessionList.append( "default" );
}

void SettingsMAS::save(const Settings *settings)
{

}

void SettingsMAS::load(ConfigMT4 *configKit)
{
    configKit->nameKit = "default";
    configKit->input.append("EURUSD.pro1440");
    configKit->input.append("GBPUSD.pro1440");
    configKit->input.append("USDJPY.pro1440");
    configKit->input.append("AUDUSD.pro1440");
    configKit->input.append("S&P5001440");
    configKit->input.append("DAX1440");
    configKit->input.append("FTSE1001440");
    configKit->input.append("BRENT1440");
    configKit->input.append("XAUUSD.pro1440");
    configKit->input.append("YEAR");
    configKit->input.append("MONTH");
    configKit->input.append("DAY");
    configKit->input.append("HOUR");
    configKit->input.append("WEEKDAY");
    configKit->output.append("XAUUSD.pro1440");
    //emit loaded( configKit->nameKit );
}

void SettingsMAS::save(const ConfigMT4 *configKit)
{

}

void SettingsMAS::deleteMAKit(const QString &kit)
{
    //
}

void SettingsMAS::renameMAKit(const QString &oldName, const QString &newName)
{
    deleteMAKit( oldName );
    //
}
