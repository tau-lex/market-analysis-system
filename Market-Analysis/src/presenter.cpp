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
    setConnections();
    loadSettings();
    settingsForm->setSettingsPtr( settings );
    //kitConfigForm->setSettingsPtr( settings );
    foreach( QString kit, settings->sessionList ) {
        openMAKit( kit );
        qDebug() << kit ;
    }
}

Presenter::~Presenter()
{
    QMapIterator<QString, Trio *> i(mapKits);
    while( i.hasNext() ) {
        i.next();
        //delete i.value()->configKit;
        //delete i.value()->itemMAKit;
        //delete i.value()->tabKit;
        delete i.value();
    }
    delete kitConfigForm;
    delete settingsForm;
    delete mainWindow;
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

void Presenter::openKitConfigForm(const QString name)
{
    name;
    kitConfigForm->show();
}

void Presenter::errorMessage(const QString text)
{
    QMessageBox::warning( mainWindow, tr("Program Error!"), text );
}

void Presenter::setCurrentKit(const QString name)
{
    currentKit = name;
    kitConfigForm->setConfigMt4Ptr( mapKits[currentKit]->configKit );
    updateActionsButtons( name );
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
    updateTab( name );
    mainWindow->addNewTab( name, mapKits[name]->tabKit );
}

void Presenter::openDialog()
{
    openMAKit( "default" );
    // question what open
}

void Presenter::openMAKit(QString name)
{
    if( !settings->savedKitsList.contains( name ) && name != "default" )
        return;
    mapKits[name] = new Trio( this, mainWindow, name );
    setConnections( name );
    loadMAKit( name );
    updateTab( name );
    mainWindow->addNewTab( name, mapKits[name]->tabKit );
}

void Presenter::closeMAKit(const QString name)
{
    saveMAKit( name );
    mainWindow->deleteTabConnections( mapKits[name]->tabKit );
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
    mapKits[newName] = mapKits[oldName];
    mapKits[oldName] = 0;
    mapKits.erase( mapKits.find( oldName ) );
    mapKits[newName]->configKit->rename( newName );
    mapKits[newName]->tabKit->rename( newName );
    //saveMAKit( newName );
    SettingsMAS::Instance().deleteMAKit( oldName );
    //updateTab( newName );
}

void Presenter::deleteMAKit(const QString name)
{
    closeMAKit( name );
    SettingsMAS::Instance().deleteMAKit( name );
    delete mapKits[name];
    mapKits[name] = 0;
    mapKits.erase( mapKits.find( name ) );
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

void Presenter::updateTab(const QString name)
{
    MainWindow::KitTabWidget *tab = mapKits[name]->tabKit;
    ConfigMT4 *config = mapKits[name]->configKit;
    tab->name = config->nameKit;
    tab->nameKitName->setText( config->nameKit );
    tab->serverName->setText( config->server );
    tab->pathToMt4Name->setText( config->mt4Path );
    tab->inputListView->clear();
    tab->inputListView->addItems( config->input );
    tab->outputListView->clear();
    tab->outputListView->addItems( config->output );
    // + calculate timeseries bars
    tab->inputSize->setText( QString("%1 * %2 = %3")
                             .arg( config->input.size() )
                             .arg( config->depthHistory )
                             .arg( config->depthHistory * config->input.size() ) );
    tab->outputSize->setText( QString("%1 * %2 = %3")
                              .arg( config->output.size() )
                              .arg( config->depthPrediction )
                              .arg( config->depthPrediction * config->output.size() ) );
    tab->progressBar->setValue( config->progress );
    tab->configurationButton->setEnabled( !config->isRun );
    tab->trainingButton->setEnabled( !config->isRun );
    tab->workButton->setEnabled( !config->isRun ? config->isTrained : false );
    tab->stopButton->setEnabled( config->isRun );
    tab->deleteButton->setEnabled( !config->isRun );
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

//void Presenter::loadKits(const QStringList &list)
//{
//    foreach( auto &kit, list )
//        loadMAKit( kit );
//}

//void Presenter::saveKits(const QStringList &list)
//{
//    foreach( auto &kit, list )
//        saveMAKit( kit );
//}

void Presenter::updateActionsButtons(const QString name)
{
    bool actions[5];
    actions[0] = !mapKits[name]->configKit->isRun;//config
    actions[1] = !mapKits[name]->configKit->isRun;//start training
    actions[2] = !mapKits[name]->configKit->isRun ?
                mapKits[name]->configKit->isTrained : false;//start forecasting
    actions[3] = mapKits[name]->configKit->isRun;//stop
    actions[4] = !mapKits[name]->configKit->isRun;//delete
    mainWindow->updateActions( actions );
}

void Presenter::setConnections()
{
    connect( mainWindow, SIGNAL( settings() ), this, SLOT( openSettingsForm() ) );
    connect( mainWindow, SIGNAL( kitConfigs(QString) ),
            this, SLOT( openKitConfigForm(QString) ) );
    connect( mainWindow, SIGNAL( currentTab(QString) ),
             this, SLOT( setCurrentKit(QString) ) );
    connect( mainWindow, SIGNAL( addNewKit() ), this, SLOT( newMAKit() ) );
    connect( mainWindow, SIGNAL( openKit() ), this, SLOT( openDialog() ) );
    connect( mainWindow, SIGNAL( closedKit(QString) ),
             this, SLOT( closeMAKit(QString) ) );
    connect( mainWindow, SIGNAL( renamedKit(QString,QString) ),
             this, SLOT( renameMAKit(QString,QString) ) );
    connect( mainWindow, SIGNAL( deleteKit(QString) ),
             this, SLOT( deleteMAKit(QString) ) );
    connect( mainWindow, SIGNAL( runTrainingKit(QString) ),
             this, SLOT( runTraining(QString) ) );
    connect( mainWindow, SIGNAL( runWorkKit(QString) ),
             this, SLOT( runWork(QString) ) );
    connect( mainWindow, SIGNAL( stopWorkKit(QString) ),
             this, SLOT( stopWork(QString) ) );
    connect( mainWindow, SIGNAL( closeWindow() ), this, SLOT( closeWindow() ) );
    connect( kitConfigForm, SIGNAL( saved(QString) ), this, SLOT( updateTab(QString) ) );
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

void Presenter::closeWindow()
{
    if(QMessageBox::No == QMessageBox::question( mainWindow,
                                                 tr("Close Market Analysis System?"),
                                                 tr("Are you sure that you want to close program?"),
                                                 QMessageBox::Yes,
                                                 QMessageBox::No ) ) {
        return;
    }
    QApplication::closeAllWindows();
    QApplication::exit();
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
