#include "include/presenter.h"
#include "include/settingsmas.h"

#include <QApplication>
#include <QMap>
#include <QMessageBox>

Presenter::Presenter(QObject *parent) : QObject(parent),
    settings(new Settings),
    mainWindow(new MainWindow),
    settingsForm(new SettingsForm(mainWindow)),
    kitConfigForm(new KitConfigForm(mainWindow)),
    openKitDialog(new OpenKitDialog(mainWindow))
{
    setConnections();
    loadSettings();
    settingsForm->setSettingsPtr( settings );
    foreach( QString kit, settings->session )
        openMAKit( kit );
}

Presenter::~Presenter()
{
    QMapIterator<QString, Trio *> i(mapKits);
    while( i.hasNext() ) {
        i.next();
        delete i.value();
    }
    delete openKitDialog;
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
    updateTab( name );
}

void Presenter::newMAKit(void)
{
    qint32 idx = 1;
    QString name = tr("New Market Kit (%1)").arg( idx );
    while( settings->savedKits.contains(name) ) {
        idx += 1;
        name = tr("New Market Kit (%1)").arg( idx );
    }
    mapKits[name] = new Trio( this, mainWindow, name );
    setConnections( name );
    loadMAKit( name );
    mainWindow->addNewTab( name, mapKits[name]->tabKit );
    settings->savedKits.append( name );
    settings->session.append( name );
    setCurrentKit( name );
}

void Presenter::openDialog()
{
    openKitDialog->show( settings->savedKits );
}

void Presenter::openMAKit(QString name)
{
    if( !settings->savedKits.contains( name ) || name == "" )
        return;
    mapKits[name] = new Trio( this, mainWindow, name );
    setConnections( name );
    loadMAKit( name );
    mainWindow->addNewTab( name, mapKits[name]->tabKit );
    if( !settings->savedKits.contains(name) )
        settings->savedKits.append( name );
    if( !settings->session.contains( name ) )
        settings->session.append( name );
    setCurrentKit( name );
}

void Presenter::closeMAKit(const QString name)
{
    saveMAKit( name );
    mainWindow->deleteTabConnections( mapKits[name]->tabKit );
    deleteConnections( name );
    delete mapKits[name];
    mapKits[name] = 0;
    mapKits.erase( mapKits.find( name ) );
    settings->session.removeOne( name );
}

void Presenter::renameMAKit(const QString oldName, const QString newName)
{
    if( oldName == newName )
        return;
    mapKits[newName] = mapKits[oldName];
    SettingsMAS::Instance().deleteMAKit( mapKits[oldName]->configKit );
    mapKits[oldName] = 0;
    mapKits.erase( mapKits.find( oldName ) );
    mapKits[newName]->configKit->rename( newName );
    mapKits[newName]->tabKit->rename( newName );
    saveMAKit( newName );
    settings->savedKits.append( newName );
    settings->savedKits.removeOne( oldName );
    settings->session.append( newName );
    settings->session.removeOne( oldName );
    //updateTab( newName );
}

void Presenter::deleteMAKit(const QString name)
{
    SettingsMAS::Instance().deleteMAKit( mapKits[name]->configKit );
    mainWindow->deleteTabConnections( mapKits[name]->tabKit );
    deleteConnections( name );
    delete mapKits[name];
    mapKits[name] = 0;
    mapKits.erase( mapKits.find( name ) );
    settings->session.removeOne( name );
    settings->savedKits.removeOne( name );
}

void Presenter::runTraining(const QString name)
{
    mapKits[name]->configKit->isRun = true;
    emit mapKits[name]->itemMAKit->runTraining();
    updateTab( name );
}

void Presenter::runWork(const QString name)
{
    mapKits[name]->configKit->isRun = true;
    emit mapKits[name]->itemMAKit->runPrediction();
    updateTab( name );
}

void Presenter::stopWork(const QString name)
{
    mapKits[name]->configKit->isRun = false;
    emit mapKits[name]->itemMAKit->stop();
    updateTab( name );
}

void Presenter::updateTab(const QString name)
{
    MainWindow::KitTabWidget *tab = mapKits[name]->tabKit;
    ConfigMT4 *config = mapKits[name]->configKit;
    QString nname = name; // const fix
    if( tab->name != config->nameKit ||
            tab->nameKitName->text() != config->nameKit ) {
        renameMAKit( tab->name, config->nameKit );
        nname = config->nameKit; // here
    }
    tab->nameKitName->setText( nname );
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
    tab->trainingButton->setEnabled( !config->isRun ? config->isReady : false );
    tab->workButton->setEnabled( !config->isRun ? config->isTrained : false );
    tab->stopButton->setEnabled( config->isRun );
    tab->deleteButton->setEnabled( !config->isRun );
    updateActionsButtons( nname );
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

void Presenter::updateActionsButtons(const QString name)
{
    bool actions[5];
    actions[0] = !mapKits[name]->configKit->isRun;//config
    actions[1] = !mapKits[name]->configKit->isRun ?
                mapKits[name]->configKit->isReady : false;//start training
    actions[2] = !mapKits[name]->configKit->isRun ?
                mapKits[name]->configKit->isTrained : false;//start forecasting
    actions[3] = mapKits[name]->configKit->isRun;//stop
    actions[4] = !mapKits[name]->configKit->isRun;//delete
    mainWindow->updateActions( actions );
}

void Presenter::runTerminal(const QString name)
{
    QString terminal;
    terminal += mapKits[name]->configKit->mt4Path;
    terminal += "/terminal.exe";
    // run mt4 + mas_assistant
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
    connect( kitConfigForm, SIGNAL( saved(QString) ),
             this, SLOT( saveMAKit(QString) ) );
    connect( kitConfigForm, SIGNAL( savedUpd(QString) ),
             this, SLOT( updateTab(QString) ) );
    connect( kitConfigForm, SIGNAL( updateSymbols(ConfigMT4*) ),
             &SettingsMAS::Instance(), SLOT( loadMt4Conf(ConfigMT4*) ) );
    connect( openKitDialog, SIGNAL( openKit(QString) ),
             this, SLOT( openMAKit(QString) ) );
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
    if( QMessageBox::No == QMessageBox::question( mainWindow,
                                                  tr("Close Market Analysis System?"),
                                                  tr("Are you sure that you want to close program?"),
                                                  QMessageBox::Yes,
                                                  QMessageBox::No ) ) {
        return;
    }
    saveSettings();
    QApplication::closeAllWindows();
    QApplication::exit();
}

Presenter::Trio::Trio(Presenter *parent1, MainWindow *parent2, QString name)
{
    configKit = new ConfigMT4( name );
    itemMAKit = new MarketAssayKit( parent1, configKit );
    tabKit = new MainWindow::KitTabWidget( parent2->getTabWidget(), name );
}

Presenter::Trio::~Trio()
{
    delete configKit;
    delete itemMAKit;
    delete tabKit;
}
