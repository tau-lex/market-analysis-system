#include "include/presenter.h"
#include "include/settingsmas.h"

#include <QApplication>
#include <QMap>
#include <QMessageBox>
#include <QDebug>

Presenter::Presenter(QObject *parent) : QObject(parent),
    settings(new Settings),
    mainWindow(new MainWindow),
    settingsForm(new SettingsForm),
    kitConfigForm(new KitConfigForm)
{
    loadSettings();
    settingsForm->setSettingsPtr( settings );
    loadKits( settings->sessionList );

    //setConnections();
}

Presenter::~Presenter()
{
    delete kitConfigForm;
    delete settingsForm;
    delete mainWindow;
    QMapIterator<QString, Trio *> i(mapKits);
    while( i.hasNext() ) {
        i.next();
        //delete i.value()->configKit;
        //delete i.value()->itemMAKit;
        //delete i.value()->tabKit;
        delete i.value();
    }
    delete settings;
}

void Presenter::openMainWindow()
{
    mainWindow->show();
}

void Presenter::openSettingsForm()
{
    settingsForm->show();
}

void Presenter::openKitConfigForm()
{
    kitConfigForm->show();
}

void Presenter::errorMessage(const QString text)
{
    //QMessageBox::warning( this, tr("Program Error!"), text );
}

void Presenter::setCurrentKit(const QString name)
{
    currentKit = name;
    kitConfigForm->setConfigMt4Ptr( mapKits[currentKit]->configKit );
}

void Presenter::newMAKit(void)
{
    QString name = tr("New Market Kit");
    qint32 idx = 1;
    while( settings->savedKitsList.contains(name) ) {
        idx += 1;
        name = tr("New Market Kit (%1)").arg( idx );
    }
    mapKits[name] = new Trio( this, mainWindow, name );
    setConnections( name );
    //?
}

void Presenter::openMAKit(const QString name)
{
    if( !settings->savedKitsList.contains( name ) )
        return;
    mapKits[name] = new Trio( this, mainWindow, name );
    setConnections( name );
    loadMAKit( name );
    //?
}

void Presenter::deleteMAKit(const QString name)
{
    mapKits[name]->configKit->remove();
    closeMAKit( name );
    SettingsMAS::Instance().deleteMAKit( name );
}

void Presenter::closeMAKit(const QString name)
{
    saveMAKit( name );
    deleteConnections( name );
    delete mapKits[name]->configKit;
    mapKits[name]->configKit = 0;
    delete mapKits[name]->itemMAKit;
    mapKits[name]->itemMAKit = 0;
    delete mapKits[name]->tabKit;
    mapKits[name]->tabKit = 0;
}

void Presenter::renameMAKit(const QString oldName, const QString newName)
{
    if( oldName == newName )
        return;
    mapKits[newName] = new Trio;
    mapKits[newName] = mapKits[oldName];
    mapKits[oldName] = 0;
    mapKits.erase( mapKits.find( oldName ) );
    SettingsMAS::Instance().save( mapKits[newName]->configKit );
    SettingsMAS::Instance().deleteMAKit( oldName );
}

void Presenter::runTraining(const QString name)
{
    mapKits[name]->configKit->isRun = true;
    emit mapKits[name]->itemMAKit->runTraining();
}

void Presenter::runWork(const QString name)
{
    mapKits[name]->configKit->isRun = true;
    emit mapKits[name]->itemMAKit->runPrediction();
}

void Presenter::stopWork(const QString name)
{
    mapKits[name]->configKit->isRun = false;
    emit mapKits[name]->itemMAKit->stop();
}

void Presenter::createTab()
{

}

void Presenter::loadSettings()
{
    SettingsMAS::Instance().load( settings );
}

void Presenter::saveSettings()
{
    SettingsMAS::Instance().save( settings );
}

void Presenter::loadMAKit(const QString name)
{
    SettingsMAS::Instance().load( mapKits[name]->configKit );
}

void Presenter::saveMAKit(const QString name)
{
    SettingsMAS::Instance().save( mapKits[name]->configKit );
}

void Presenter::loadKits(const QStringList &list)
{
    foreach( auto &kit, list )
        loadMAKit( kit );
}

void Presenter::saveKits(const QStringList &list)
{
    foreach( auto &kit, list )
        saveMAKit( kit );
}

void Presenter::setConnections()
{

}

void Presenter::setConnections(const QString name)
{
    connect( mapKits[name]->itemMAKit, SIGNAL( trained(QString) ),
             this, SIGNAL( trainDone(QString) ) );
    connect( mapKits[name]->itemMAKit, SIGNAL( progress(QString, qint32) ),
             this, SIGNAL( progress(QString, qint32) ) );
    connect( mapKits[name]->itemMAKit, SIGNAL( message(QString,QString) ),
             this, SIGNAL( writeToConsole(QString,QString) ) );
}

void Presenter::deleteConnections(const QString name)
{
    disconnect( mapKits[name]->itemMAKit, SIGNAL( trained(QString) ),
                this, SIGNAL( trainDone(QString) ) );
    disconnect( mapKits[name]->itemMAKit, SIGNAL( progress(QString, qint32) ),
                this, SIGNAL( progress(QString, qint32) ) );
    disconnect( mapKits[name]->itemMAKit, SIGNAL( message(QString,QString) ),
                this, SIGNAL( writeToConsole(QString,QString) ) );
}

Presenter::Trio::Trio(QObject *parent1, MainWindow *parent2, QString name)
{
    configKit = new ConfigMT4( name );
    itemMAKit = new MarketAssayKit( parent1, configKit );
    tabKit = new MainWindow::KitTabWidget( parent2, name );
}

Presenter::Trio::~Trio()
{
    delete configKit;
    delete itemMAKit;
    delete tabKit;
}
