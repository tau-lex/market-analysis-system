#include "include/settingsmas.h"
#include <QApplication>
#include <QSettings>
#include <QVariant>
#include <QDir>

SettingsMAS::SettingsMAS(QObject *parent) : QObject(parent)
{
    global = new QSettings( qApp->organizationName(),
                            qApp->applicationName(), this );
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
    global->beginGroup( "Global" );
    readArray( "Saved_Kits", "Kit", global, settings->savedKits );
    readArray( "Last_Session", "Session", global, settings->session );
    settings->savedKits.removeAll("");
    settings->session.removeAll("");
    global->endGroup();
    global->beginGroup( "Window" );
    settings->maxOpenTabs = global->value( "Max_Tabs" ).toInt();
    settings->winPosX = global->value( "Pos_X" ).toInt();
    settings->winPosY = global->value( "Pos_Y" ).toInt();
    settings->winSizeX = global->value( "Size_X" ).toInt();
    settings->winSizeY = global->value( "Size_Y" ).toInt();
    global->endGroup();
    QString mDir = qApp->applicationDirPath();
    mDir += "/Market Kits";
    if( !QDir().exists(mDir) )
        QDir().mkdir(mDir);
}

void SettingsMAS::save(const Settings *settings)
{
    clear();
    global->beginGroup( "Global" );
    writeArray( "Saved_Kits", "Kit", global, settings->savedKits );
    writeArray( "Last_Session", "Session", global, settings->session );
    global->endGroup();
    global->beginGroup( "Window" );
    global->setValue( "Max_Tabs", settings->maxOpenTabs );
    global->setValue( "Pos_X", settings->winPosX );
    global->setValue( "Pos_Y", settings->winPosY );
    global->setValue( "Size_X", settings->winSizeX );
    global->setValue( "Size_Y", settings->winSizeY );
    global->endGroup();
}

bool SettingsMAS::load(ConfigMT4 *configKit)
{
    if( configKit->nameKit.contains( "New Market Kit" ) ) {
        loadDefault( configKit );
        return true;
    }
    QString configFile = QString("%1/%2").arg( configKit->kitPath )
                                         .arg( "config.ini" );
    if( !QDir().exists(configFile) ) {
        return false;
    }
    kitFile = new QSettings( configFile, QSettings::IniFormat);
    kitFile->beginGroup( "Main" );
    configKit->nameKit =            kitFile->value( "Kit_Name" ).toString();
    configKit->kitPath =            kitFile->value( "Kit_Path" ).toString();
    configKit->mt4Path =            kitFile->value( "Mt4_Path" ).toString();
    configKit->mt4Account =         kitFile->value( "Mt4_Account" ).toInt();
    configKit->server =             kitFile->value( "Mt4_Server" ).toString();
    configKit->historyPath =        kitFile->value( "History_Path" ).toString();
    readArray( "Servers", "Srv", kitFile, configKit->servers );
    readArray( "Symbols", "Smb", kitFile, configKit->symbols );
    kitFile->endGroup();
    kitFile->beginGroup( "Model_Parameters" );
    readArray( "Periods", "Tf", kitFile, configKit->periods );
    readArray( "Input", "In", kitFile, configKit->input );
    readArray( "Output", "Out", kitFile, configKit->output );
    configKit->recurrentModel =     kitFile->value( "Recurrent_Model" ).toBool();
    configKit->readVolume =         kitFile->value( "Read_Volume" ).toBool();
    configKit->depthHistory =       kitFile->value( "Depth_History" ).toInt();
    configKit->depthPrediction =    kitFile->value( "Depth_Prediction" ).toInt();
    configKit->layersCount =        kitFile->value( "LayersNN_Count" ).toInt();
    readArray( "LayersNN_Sizes", "Size", kitFile, configKit->layersSize );
    configKit->trainingMethod =     kitFile->value( "Training_Method" ).toString();
    readArray( "Training_Allocation", "Part", kitFile, configKit->divideInstances );
    configKit->lastTraining.fromTime_t( kitFile->value( "Last_Training" ).toInt() );
    configKit->lastChange.fromTime_t( kitFile->value( "Last_Change" ).toInt() );
    configKit->isReady =            kitFile->value( "Is_Ready" ).toBool();
    configKit->isTrained =          kitFile->value( "Is_Trained" ).toBool();
    if( configKit->isTrained )
        configKit->isLoaded = true;
    kitFile->endGroup();
    delete kitFile;
    kitFile = 0;
    loadMt4Conf( configKit );
    return true;
}

void SettingsMAS::save(const ConfigMT4 *configKit)
{
    kitFile = new QSettings( QString("%1/%2").arg( configKit->kitPath )
                             .arg( "config.ini" ), QSettings::IniFormat );
    kitFile->beginGroup( "Main" );
    kitFile->setValue( "Kit_Name",         configKit->nameKit );
    kitFile->setValue( "Kit_Path",         configKit->kitPath );
    kitFile->setValue( "Mt4_Path",         configKit->mt4Path );
    kitFile->setValue( "Mt4_Account",      configKit->mt4Account );
    kitFile->setValue( "Mt4_Server",       configKit->server );
    kitFile->setValue( "History_Path",     configKit->historyPath );
    writeArray( "Servers", "Srv", kitFile, configKit->servers );
    writeArray( "Symbols", "Smb", kitFile, configKit->symbols );
    kitFile->endGroup();
    kitFile->beginGroup( "Model_Parameters" );
    writeArray( "Periods", "Tf", kitFile,  configKit->periods );
    writeArray( "Input", "In", kitFile,    configKit->input );
    writeArray( "Output", "Out", kitFile,  configKit->output );
    kitFile->setValue( "Recurrent_Model",  configKit->recurrentModel );
    kitFile->setValue( "Read_Volume",      configKit->readVolume );
    kitFile->setValue( "Depth_History",    configKit->depthHistory );
    kitFile->setValue( "Depth_Prediction", configKit->depthPrediction );
    kitFile->setValue( "LayersNN_Count",   configKit->layersCount );
    writeArray( "LayersNN_Sizes", "Size", kitFile, configKit->layersSize );
    kitFile->setValue( "Training_Method",  configKit->trainingMethod );
    writeArray( "Training_Allocation", "Part", kitFile, configKit->divideInstances );
    kitFile->setValue( "Last_Training",    configKit->lastTraining.toTime_t() );
    kitFile->setValue( "Last_Change",      configKit->lastChange.toTime_t() );
    kitFile->setValue( "Is_Ready",         configKit->isReady );
    kitFile->setValue( "Is_Trained",       configKit->isTrained );
    kitFile->endGroup();
    delete kitFile;
    kitFile = 0;
    saveMt4Conf( configKit );
}

void SettingsMAS::loadMt4Conf(ConfigMT4 *configKit)
{
    kitFile = new QSettings( QString("%1%2").arg( configKit->mt4Path )
                             .arg( configKit->configFile ), QSettings::IniFormat);
    kitFile->beginGroup( "Main" );
    readArray( "Symbols", "Smb", kitFile, configKit->symbols );
    configKit->mt4Account = kitFile->value( "Mt4_Account" ).toInt();
    kitFile->endGroup();
    delete kitFile;
    kitFile = 0;
}

void SettingsMAS::saveMt4Conf(const ConfigMT4 *configKit)
{
    kitFile = new QSettings( QString("%1%2").arg( configKit->mt4Path )
                             .arg( configKit->configFile ), QSettings::IniFormat);
    kitFile->beginGroup( "Main" );
    QStringList temp;
    readArray( "Kit_Names", "Kit", kitFile, temp );
    if( !temp.contains( configKit->nameKit ) )
        temp.append( configKit->nameKit );
    writeArray( "Kit_Names", "Kit", kitFile, temp );
    kitFile->endGroup();
    kitFile->beginGroup( configKit->nameKit );
    kitFile->setValue( "Depth_Prediction", configKit->depthPrediction );
    writeArray( "Input", "In", kitFile,    configKit->input );
    writeArray( "Output", "Out", kitFile,  configKit->output );
    kitFile->endGroup();
    delete kitFile;
    kitFile = 0;
}

void SettingsMAS::deleteMAKit(ConfigMT4 *configKit)
{
    kitFile = new QSettings( QString("%1%2")
                             .arg( configKit->mt4Path )
                             .arg( configKit->configFile ), QSettings::IniFormat);
    kitFile->beginGroup( "Main" );
    QStringList temp;
    readArray( "Kit_Names", "Kit", kitFile, temp );
    temp.removeOne( configKit->nameKit );
    writeArray( "Kit_Names", "Kit", kitFile, temp );
    kitFile->endGroup();
    kitFile->beginGroup( configKit->nameKit );
    kitFile->remove( "Depth_Prediction" );
    kitFile->remove( "Input" );
    kitFile->remove( "Output" );
    kitFile->endGroup();
    delete kitFile;
    kitFile = 0;
    configKit->removePath( configKit->kitPath );
}

void SettingsMAS::readArray(const QString &arrayName, const QString &valueName,
                            QSettings *setups, QStringList &list)
{
    Q_UNUSED(valueName);
    list.clear();
    foreach(QString item, setups->value( arrayName ).toString().split( ";", QString::SkipEmptyParts ) )
        list.append( item );
}

void SettingsMAS::readArray(const QString &arrayName, const QString &valueName,
                            QSettings *setups, QList<qint32> &list)
{
    list.clear();
    qint32 size = setups->beginReadArray( arrayName );
    for( qint32 i = 0; i < size; i++ ) {
        setups->setArrayIndex( i );
        list.append( setups->value( valueName ).toInt() );
    }
    setups->endArray();
}

void SettingsMAS::writeArray(const QString &arrayName, const QString &valueName,
                             QSettings *setups, const QStringList &list)
{
    Q_UNUSED(valueName);
    QString tmp = "";
    foreach( QString str, list ) {
        tmp += str; tmp += ";";
    }
    tmp.remove( tmp.size() - 1, 1);
    setups->setValue( arrayName, tmp );
}

void SettingsMAS::writeArray(const QString &arrayName, const QString &valueName,
                             QSettings *setups, const QList<qint32> &list)
{
    setups->beginWriteArray( arrayName );
    for( qint32 i = 0; i < list.size(); i++) {
        setups->setArrayIndex( i );
        setups->setValue( valueName, list[i] );
    }
    setups->endArray();
}

void SettingsMAS::loadDefault(ConfigMT4 *configKit)
{
    configKit->input.append( "YEAR" );
    configKit->input.append( "MONTH" );
    configKit->input.append( "DAY" );
    configKit->input.append( "WEEKDAY" );
    configKit->input.append( "EURUSD.pro1440" );
    configKit->output.append( "EURUSD.pro1440" );
    configKit->periods.append( 1440 );
}

void SettingsMAS::clear()
{
    global->beginGroup( "Global" );
    qint32 i = 0;
    while( global->contains( QString("Saved_Kits_%1").arg( i ) ) ) {
        global->remove( QString("Saved_Kits_%1").arg( i ) );
        i++;
    }
    i = 0;
    while( global->contains( QString("Last_Session_%1").arg( i ) ) ) {
        global->remove( QString("Last_Session_%1").arg( i ) );
        i++;
    }
    global->endGroup();
}
