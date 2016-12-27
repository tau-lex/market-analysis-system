#include "include/configmas.h"

ConfigMAS::ConfigMAS(QObject *parent) : QObject(parent)
{ }

ConfigMAS &ConfigMAS::Instance()
{
    static ConfigMAS singleInstance;
    return singleInstance;
}

void ConfigMAS::load(const Settings *settings)
{

}

void ConfigMAS::save(const Settings *settings)
{

}

void ConfigMAS::load(const ConfigMT4 *configKit)
{

}

void ConfigMAS::save(const ConfigMT4 *configKit)
{

}

void ConfigMAS::load(QVector<ConfigMT4 *> &configKitList)
{

}

void ConfigMAS::save(const QVector<ConfigMT4 *> &configKitList)
{

}

qint32 ConfigMAS::addKit(const QString &kit)
{
    settings.beginWriteArray( "kits" );
    qint32 ind = getCountOfKits() + 1;
    settings.setArrayIndex( ind );
    settings.setValue( "name", kit );
    settings.endArray();
    //autosave();
    return ind;
}

void ConfigMAS::deleteKit(const QString &kit)
{
    QStringList listOfKits;
    qint32 size = settings.beginReadArray( "kits" );
    for( qint32 i = 0; i < size; i++ ) {
        settings.setArrayIndex(i);
        listOfKits.append( settings.value("name").toString() );
    }
    settings.endArray();
    listOfKits.removeOne( kit );
    settings.beginWriteArray( "kits" );
    for( qint32 i = 0; i < listOfKits.size(); i++ ) {
        settings.setArrayIndex( i );
        settings.setValue( "name", listOfKits[i] );
    }
    settings.endArray();
    //autosave();
}

void ConfigMAS::renameKit(const QString &oldName, const QString &newName)
{
    deleteKit( oldName );
    addKit( newName );
    //autosave();
}

void ConfigMAS::setDefaultKit(const QString &kit)
{
    settings.setValue( "default", kit);
    //autosave();
}

const QString ConfigMAS::getDefaultKit() const
{
    return settings.value("default").toString();
}

const qint32 ConfigMAS::getCountOfKits()
{
    qint32 size = settings.beginReadArray( "kits" );
    settings.endArray();
    return size;
}

const QStringList ConfigMAS::getListOfKits()
{
    QStringList listOfKits;
    qint32 size = settings.beginReadArray( "kits" );
    for( qint32 i = 0; i < size; i++ ) {
        settings.setArrayIndex( i );
        listOfKits.append( settings.value("name").toString() );
    }
    return listOfKits;
}
