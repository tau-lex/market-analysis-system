#include "include/presenter.h"
#include "include/settingsmas.h"

#include <QDir>
#include <QApplication>
#include <QDebug>

Presenter::Presenter(QObject *parent) : QObject(parent)
{
    settings = new Settings;
    SettingsMAS::Instance().load( settings );
    loadKits( settings->sessionList );

    //setConnections();
}

Presenter::~Presenter()
{
    QMapIterator<QString, Pair *> i(mapKits);
    while( i.hasNext() ) {
        i.next();
        delete i.value()->configKit;
        delete i.value()->itemKit;
    }
    delete settings;
}

QStringList Presenter::previousSession() const
{
    return settings->sessionList;
}

Settings *Presenter::getSettingsPtr() const
{
    return settings;
}

ConfigMT4 *Presenter::getConfigMt4Ptr(const QString name)
{
    if( mapKits.contains( name ) )
        return mapKits[name]->configKit;
    newMAKit( name );
    return mapKits[name]->configKit;
}

void Presenter::newMAKit(const QString name)
{
    if( mapKits.contains( name ) ) {
        error( name, tr("Can't open new kit!\nSet\"%1\" has been created!")
               .arg(name) );
        return; //skip
    }
    mapKits[name] = new Pair;
    mapKits[name]->configKit = new ConfigMT4;
    mapKits[name]->configKit->nameKit = name;
    mapKits[name]->itemKit = new MarketAssayKit;
    mapKits[name]->itemKit->setKitPtr( mapKits[name]->configKit );
    setConnections( name );
    QString mDir = QApplication::applicationDirPath();
    mDir += "/Market Kits/";
    mDir += name;
    if(!QDir().exists(mDir))
        QDir().mkdir(mDir);
    mapKits[name]->configKit->kitPath = mDir;
}

void Presenter::openMAKit(const QString name)
{
    if( !mapKits.contains( name ) )
        loadMAKit( name );
}

void Presenter::saveMAKit(const QString name)
{
    SettingsMAS::Instance().save( mapKits[name]->configKit );
    //SettingsMAS::Instance().save( mapKits[name].itemKit ); ?
}

void Presenter::loadMAKit(const QString name)
{
    if( !mapKits.contains( name ) )
        newMAKit( name );
    SettingsMAS::Instance().load( mapKits[name]->configKit );
}

void Presenter::deleteMAKit(const QString name)
{
    delete mapKits[name]->configKit;
    mapKits[name]->configKit = 0;
    delete mapKits[name]->itemKit;
    mapKits[name]->itemKit = 0;
    SettingsMAS::Instance().deleteMAKit( name );
}

void Presenter::closeMAKit(const QString name)
{
    try {
        if( !mapKits.contains( name ) )
            throw 11;
        deleteConnections( name );
        delete mapKits[name]->configKit;
        mapKits[name]->configKit = 0;
        delete mapKits[name]->itemKit;
        mapKits[name]->itemKit = 0;
        qDebug() << "Close -" << name;
    } catch(int e) {
        emit error( "Presenter", tr("Close Market Assay Kit \"%1\" error - %2")
                    .arg( name )
                    .arg( e ) );
    }
}

void Presenter::renameMAKit(const QString oldName, const QString newName)
{
    if( oldName == newName )
        return;
    mapKits[newName] = new Pair;
    mapKits[newName] = mapKits[oldName];
    mapKits[oldName] = 0;
    mapKits.erase( mapKits.find( oldName ) );
    SettingsMAS::Instance().save( mapKits[newName]->configKit );
    SettingsMAS::Instance().deleteMAKit( oldName );
}

void Presenter::runTraining(const QString name)
{
    mapKits[name]->configKit->isRun = true;
    emit mapKits[name]->itemKit->runTraining();
}

void Presenter::runWork(const QString name)
{
    mapKits[name]->configKit->isRun = true;
    emit mapKits[name]->itemKit->runPrediction();
}

void Presenter::stopWork(const QString name)
{
    mapKits[name]->configKit->isRun = false;
    emit mapKits[name]->itemKit->stop();
}

void Presenter::loadKits(const QStringList list)
{
    foreach( auto &kit, list )
        openMAKit( kit );
}

void Presenter::saveKits(const QStringList list)
{
    foreach( auto &kit, list )
        SettingsMAS::Instance().save( mapKits[kit]->configKit );
}

void Presenter::setConnections(const QString name)
{
    connect( mapKits[name]->itemKit, SIGNAL( trained(QString) ),
             this, SIGNAL( trainDone(QString) ) );
    connect( mapKits[name]->itemKit, SIGNAL( progress(QString, qint32) ),
             this, SIGNAL( progress(QString, qint32) ) );
    connect( mapKits[name]->itemKit, SIGNAL( message(QString,QString) ),
             this, SIGNAL( writeToConsole(QString,QString) ) );
}

void Presenter::deleteConnections(const QString name)
{
    disconnect( mapKits[name]->itemKit, SIGNAL( trained(QString) ),
                this, SIGNAL( trainDone(QString) ) );
    disconnect( mapKits[name]->itemKit, SIGNAL( progress(QString, qint32) ),
                this, SIGNAL( progress(QString, qint32) ) );
    disconnect( mapKits[name]->itemKit, SIGNAL( message(QString,QString) ),
                this, SIGNAL( writeToConsole(QString,QString) ) );
}
