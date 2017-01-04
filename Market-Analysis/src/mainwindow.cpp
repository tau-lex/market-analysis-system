#include "include/mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    presenter(new Presenter(this)),
    settings(new SettingsForm(this)),
    kitConfig(new KitConfigForm(this))
{
    ui->setupUi(this);
    settings->setSettingsPtr( presenter->getSettingsPtr() );

    setConnections();

    newSession( presenter->previousSession() );
}

MainWindow::~MainWindow()
{
    delete presenter;
    foreach( KitTabWidget *item, tabList ) {
        delete item->kitTab;
    }
    delete ui;
}

void MainWindow::updateTab(const QString name)
{
    for( qint32 i = 0; i < tabList.size(); i++ )
        if( tabList[i]->name == name )
            updateTab( i );
}

void MainWindow::setProgress(const QString kit, const qint32 value)
{
    foreach( KitTabWidget *tab, tabList )
        if( tab->name == kit )
            tab->progressBar->setValue(value);
}

void MainWindow::consoleMessage(const QString kit, const QString text)
{
    foreach( KitTabWidget *tab, tabList ) {
        if( tab->name == kit )
            tab->consoleTextEdit->appendPlainText( text );
    }
}

void MainWindow::errorMessage(const QString kit, const QString text)
{
    if( kit == "MainWindow" || kit == "Settings" )
        QMessageBox::warning( this, tr("Program Error!"), text );
    else {
        QMessageBox::warning( this, tr("Kit \"%1\" Error!").arg(kit), text );
        consoleMessage( kit, text );
    }
}

void MainWindow::addNew()
{
    try {
        if( countTabs >= MAX_TAB )
                throw 1;
        qint32 ind = 1;
        foreach( KitTabWidget *tab, tabList )
            if( tab->name.contains( tr("New MAS Kit") ) )
                ind++;
        QString newKit = tr("New MAS Kit #%1").arg(ind);
        emit addNewKit( newKit );
        if( !openTab( countTabs, newKit ) ) {
            emit deleteKit( newKit );
            throw 2;
        }
    } catch(int e) {
        switch( e ) {
        case 1: {
            errorMessage( "MainWindow",
                          tr("You have exceeded the allowed number of tabs - %1").arg( MAX_TAB ) );
            break;
        } case 2: {
            errorMessage( "MainWindow", tr("Oups! error - %1").arg(e) );
            break;
        }
        }
    }
}

void MainWindow::open()
{
    try {
        if( countTabs >= MAX_TAB )
                throw 1;
        qint32 ind = 1; // kostyl !  => QDialog.getString()
        foreach( KitTabWidget *tab, tabList )
            if( tab->name.contains( tr("default") ) )
                ind++;
        // kostyl !
        QString openKitStr = tr("default #%1").arg(ind);
        emit openKit( openKitStr );
        if( !openTab( countTabs, openKitStr ) ) {
            emit deleteKit( openKitStr );
            throw 2;
        }
    } catch(int e) {
        switch( e ) {
        case 1: {
            errorMessage( "MainWindow",
                          tr("You have exceeded the allowed number of tabs - %1").arg( MAX_TAB ) );
            break;
        } case 2: {
            errorMessage( "MainWindow", tr("Oups! error - %1").arg(e) );
            break;
        }
        }
    }
}

void MainWindow::save()
{
    if( currentTab >= 0 ) {
        updateTab( currentTab );
        emit saveKit( tabList[currentTab]->name );
    }
}

void MainWindow::closeTab()
{
    if( currentTab >= 0 )
        closeTab( currentTab );
}

void MainWindow::openSettings()
{
    settings->show();
}

void MainWindow::openKitConfig()
{
    if( currentTab >= 0 ) {
        kitConfig->setConfigMt4Ptr( presenter->getConfigMt4Ptr( tabList[currentTab]->name ) );
        kitConfig->show();
    }
}

void MainWindow::runTraining()
{
    if( currentTab >= 0 )
        emit runTrainingKit( tabList[currentTab]->name );
}

void MainWindow::runWork()
{
    if( currentTab >= 0 )
        emit runWorkKit( tabList[currentTab]->name );
}

void MainWindow::stopWork()
{
    if( currentTab >= 0 )
        emit stopWorkKit( tabList[currentTab]->name );
}

void MainWindow::delete_Kit()
{
    if( currentTab < 0 )
        return;
    QString selected = tabList[currentTab]->name;
    if( QMessageBox::Yes == QMessageBox::question( this, tr("Delete Kit?"),
                                                   tr("Are you sure that you want to delete set \"%1\"?")
                                                   .arg(selected) ) ) {
        closeTab( currentTab );
        emit deleteKit( selected );
    }
}

void MainWindow::openHelp()
{
    QMessageBox::about( this, tr("Help"),
                        tr("The <b>Market Analysis System</b> example demonstrates... ") );
}

void MainWindow::openAbout()
{
    QMessageBox::about( this, tr("About Market Analysis System"),
                        tr("The <b>Market Analysis System</b> example demonstrates ... ") );
}

void MainWindow::newSession(const QStringList list)
{
    foreach( QString kit, list )
        if( openTab( countTabs, kit ) )
            emit openKit( kit );
}

bool MainWindow::openTab(const qint32 idx, const QString name)
{
    if( idx >= MAX_TAB )
        return false;
    tabList.append( new KitTabWidget );
    addTabToUi( idx, name );
    setTabName( idx, name );
    ui->vTabWidget->setCurrentIndex( idx );
    countTabs++;
    return true;
}

void MainWindow::closeTab(const qint32 idx)
{
    try {
        if( currentTab < 0 )
            throw 5;
        QString selected = tabList[idx]->name;
        if( tabList[idx]->changed ) {
            if( QMessageBox::Yes == QMessageBox::question( this, tr("Save Kit?"),
                                                       tr("Are you sure that you want to delete set \"%1\"?")
                                                       .arg(selected) ) ) {
                emit saveKit( selected );
            }
        }
        tabList[idx]->kitTab->close();
        deleteTabFromUi( idx );
        emit closedKit( selected );
        countTabs--;
        currentTab = ui->vTabWidget->currentIndex();
        //updateTab( tabList[currentTab]->name );
        updateTabButtons( currentTab );
    } catch(int e) {
        errorMessage( "MainWindow", tr("CloseTab(int) Error - #%1").arg(e) );
    }
}

void MainWindow::selectTab(const qint32 idx)
{
    currentTab = idx;
    if( currentTab >= 0 )
        updateTabButtons( currentTab );
}

void MainWindow::setTabName( const qint32 idx, const QString name )
{
    QString oldName = tabList[idx]->name;
    tabList[idx]->name = name;
    tabList[idx]->config->nameKit = name;
    tabList[idx]->nameKitName->setText( name );
    ui->vTabWidget->setTabText( idx, name );
    if( oldName != tabList[idx]->name )
        emit renamedKit( oldName, tabList[idx]->name );
}

void MainWindow::updateTab(const qint32 idx)
{
    if( currentTab < 0 )
        return;
    KitTabWidget *tab = tabList[idx];
    if( tab->name != tab->config->nameKit )
        setTabName( idx, tab->config->nameKit );
    tab->serverName->setText( tab->config->server );
    tab->pathToMt4Name->setText( tab->config->mt4Path );
    //tab->inputListView = tab->config;
    //tab->outputListView = tab->config;
    tab->inputSize->setText( QString("%1").arg(tab->config->depthHistory) ); // * tab->config->'inList'
    tab->outputSize->setText( QString("%1").arg(tab->config->depthPrediction) ); // * tab->config->'outList'
    tab->progressBar->setValue( tab->config->progress );
    updateTabButtons( idx );
}

void MainWindow::updateTabButtons(const qint32 idx)
{
    if( currentTab < 0 )
        return;
    KitTabWidget *tab = tabList[idx];
    tab->configurationButton->setEnabled( !tab->config->isRun );
    ui->actionKit_Configuration->setEnabled( !tab->config->isRun );
    tab->trainingButton->setEnabled( !tab->config->isRun );
    ui->actionTrain_NN->setEnabled( !tab->config->isTrained );
    tab->workButton->setEnabled( !tab->config->isRun );
    ui->actionStart_forecasting->setEnabled( !tab->config->isRun );
    tab->stopButton->setEnabled( tab->config->isRun );
    ui->actionStop->setEnabled( tab->config->isRun );
    tab->deleteButton->setEnabled( !tab->config->isRun );
    ui->actionDelete_Kit->setEnabled( !tab->config->isRun );
}

void MainWindow::setConnections()
{
    {   // actions and widgets
        connect( ui->actionNew_Kit, SIGNAL( triggered(bool) ), this, SLOT( addNew() ) );
        connect( ui->actionOpen_Kit, SIGNAL( triggered(bool) ), this, SLOT( open() ) );
        connect( ui->actionSave_Kit, SIGNAL( triggered(bool) ), this, SLOT( save() ) );
        connect( ui->actionClose_Kit, SIGNAL( triggered(bool) ),
                 this, SLOT( closeTab() ) );
        connect( ui->actionSettings, SIGNAL( triggered(bool) ),
                 this, SLOT( openSettings() ) );
        connect( ui->actionKit_Configuration, SIGNAL( triggered(bool) ),
                 this, SLOT( openKitConfig() ) );
        connect( ui->actionTrain_NN, SIGNAL( triggered(bool) ),
                 this, SLOT( runTraining() ) );
        connect( ui->actionStart_forecasting, SIGNAL( triggered(bool) ),
                 this, SLOT( runWork() ) );
        connect( ui->actionStop, SIGNAL( triggered(bool) ), this, SLOT( stopWork() ) );
        connect( ui->actionDelete_Kit, SIGNAL( triggered(bool) ),
                 this, SLOT( delete_Kit() ) );
        connect( ui->actionHelp, SIGNAL( triggered(bool) ), this, SLOT( openHelp() ) );
        connect( ui->actionAbout, SIGNAL( triggered(bool) ), this, SLOT( openAbout() ) );
        connect( ui->actionExit, &QAction::triggered, this, &MainWindow::close );
        connect( ui->vTabWidget, SIGNAL( tabCloseRequested(int) ),
                 this, SLOT( closeTab(qint32) ) );
        connect( ui->vTabWidget, SIGNAL( currentChanged(int) ),
                 this, SLOT( selectTab(qint32) ) );
    } { // signals from MainWindow
        connect( this, SIGNAL( addNewKit(QString) ),
                 presenter, SLOT( newMAKit(QString) ) );
        connect( this, SIGNAL( openKit(QString) ),
                 presenter, SLOT( openMAKit(QString) ) );
        connect( this, SIGNAL( saveKit(QString) ),
                 presenter, SLOT( saveMAKit(QString) ) );
        connect( this, SIGNAL( deleteKit(QString) ),
                 presenter, SLOT( deleteMAKit(QString) ) );
        connect( this, SIGNAL( closedKit(QString) ),
                 presenter, SLOT( closeMAKit(QString) ) );
        connect( this, SIGNAL( renamedKit(QString, QString) ),
                 presenter, SLOT( renameMAKit(QString,QString) ) );
        connect( this, SIGNAL( runTrainingKit(QString) ),
                 presenter, SLOT( runTraining(QString) ) );
        connect( this, SIGNAL( runWorkKit(QString) ),
                 presenter, SLOT( runWork(QString) ) );
        connect( this, SIGNAL( stopWorkKit(QString) ),
                 presenter, SLOT( stopWork(QString) ) );
    } { // signals from MAKit or Presenter to MAinWindow Slots
        connect( presenter, SIGNAL( updatedKit(QString) ),
                 this, SLOT( updateTab(QString) ) );
        connect( presenter, SIGNAL( trainDone(QString) ),
                 this, SLOT( updateTab(QString) ) );
        connect( presenter, SIGNAL( progress(QString, qint32) ),
                 this, SLOT( setProgress(QString, qint32) ) );
        connect( presenter, SIGNAL( writeToConsole(QString, QString) ),
                 this, SLOT( consoleMessage(QString, QString) ) );
        connect( presenter, SIGNAL( error(QString, QString) ),
                 this, SLOT( errorMessage(QString, QString) ) );
    }
}

void MainWindow::addTabToUi(const qint32 idx, const QString name)
{
    try {       // setupUi
        tabList[idx]->config = presenter->getConfigMt4Ptr( name );
        tabList[idx]->name = name;
        tabList[idx]->kitTab = new QWidget( ui->vTabWidget );
        tabList[idx]->kitTab->setObjectName( name );
        tabList[idx]->vLayoutTab = new QVBoxLayout( tabList[idx]->kitTab );
        tabList[idx]->vLayoutTab->setSpacing(6);
        tabList[idx]->vLayoutTab->setContentsMargins( 11, 11, 11, 11 );
        tabList[idx]->vLayoutTab->setObjectName( QStringLiteral("vLayoutTab") );
        {// Name
            tabList[idx]->hGBoxKitName = new QGroupBox( tabList[idx]->kitTab );
            tabList[idx]->hGBoxKitName->setObjectName( QStringLiteral("hGBoxKitName") );
            tabList[idx]->hLayoutName = new QHBoxLayout( tabList[idx]->hGBoxKitName );
            tabList[idx]->hLayoutName->setSpacing(6);
            tabList[idx]->hLayoutName->setContentsMargins( 11, 11, 11, 11 );
            tabList[idx]->hLayoutName->setObjectName( QStringLiteral("hLayoutName") );
            tabList[idx]->hLayoutName->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->nameKitLabel = new QLabel( tabList[idx]->hGBoxKitName );
            tabList[idx]->nameKitLabel->setObjectName( QStringLiteral("nameKitLabel") );
            tabList[idx]->nameKitLabel->setMinimumSize( QSize(0, 16) );
            tabList[idx]->nameKitLabel->setBaseSize( QSize(0, 0) );
            QFont font;
            font.setPointSize(11);
            tabList[idx]->nameKitLabel->setFont( font );
            tabList[idx]->nameKitLabel->setFrameShape( QFrame::NoFrame );
            tabList[idx]->nameKitLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                                      |Qt::AlignVCenter );
            tabList[idx]->hLayoutName->addWidget( tabList[idx]->nameKitLabel );
            tabList[idx]->nameKitName = new QLabel( tabList[idx]->hGBoxKitName );
            tabList[idx]->nameKitName->setObjectName( QStringLiteral("nameKitName") );
            tabList[idx]->nameKitName->setMinimumSize( QSize(0, 16) );
            tabList[idx]->nameKitName->setFont( font );
            tabList[idx]->hLayoutName->addWidget( tabList[idx]->nameKitName );
            tabList[idx]->hLayoutName->setStretch( 0, 1 );
            tabList[idx]->hLayoutName->setStretch( 1, 5 );
            tabList[idx]->vLayoutTab->addWidget( tabList[idx]->hGBoxKitName );
        } {// Server + MT4 Path
            tabList[idx]->hGBoxPathMt4 = new QGroupBox( tabList[idx]->kitTab );
            tabList[idx]->hGBoxPathMt4->setObjectName( QStringLiteral("hGBoxPathMt4") );
            tabList[idx]->hLayoutPath = new QHBoxLayout( tabList[idx]->hGBoxPathMt4 );
            tabList[idx]->hLayoutPath->setSpacing(6);
            tabList[idx]->hLayoutPath->setContentsMargins( 11, 11, 11, 11 );
            tabList[idx]->hLayoutPath->setObjectName( QStringLiteral("hLayoutPath") );
            tabList[idx]->hLayoutPath->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->serverLabel = new QLabel( tabList[idx]->hGBoxPathMt4 );
            tabList[idx]->serverLabel->setObjectName( QStringLiteral("serverLabel") );
            tabList[idx]->serverLabel->setMinimumSize( QSize(0, 16) );
            QFont font1;
            font1.setPointSize(9);
            tabList[idx]->serverLabel->setFont( font1 );
            tabList[idx]->serverLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                                     |Qt::AlignVCenter );
            tabList[idx]->hLayoutPath->addWidget( tabList[idx]->serverLabel );
            tabList[idx]->serverName = new QLabel( tabList[idx]->hGBoxPathMt4 );
            tabList[idx]->serverName->setObjectName( QStringLiteral("serverName") );
            tabList[idx]->serverName->setMinimumSize( QSize(0, 16) );
            tabList[idx]->serverName->setFont( font1 );
            tabList[idx]->hLayoutPath->addWidget( tabList[idx]->serverName );
            tabList[idx]->pathToMt4Label = new QLabel( tabList[idx]->hGBoxPathMt4 );
            tabList[idx]->pathToMt4Label->setObjectName( QStringLiteral("pathToMt4Label") );
            tabList[idx]->pathToMt4Label->setMinimumSize( QSize(0, 16) );
            tabList[idx]->pathToMt4Label->setFont( font1 );
            tabList[idx]->pathToMt4Label->setFrameShape( QFrame::NoFrame );
            tabList[idx]->pathToMt4Label->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                                        |Qt::AlignVCenter );
            tabList[idx]->hLayoutPath->addWidget( tabList[idx]->pathToMt4Label );
            tabList[idx]->pathToMt4Name = new QLabel( tabList[idx]->hGBoxPathMt4 );
            tabList[idx]->pathToMt4Name->setObjectName( QStringLiteral("pathToMt4Name") );
            tabList[idx]->pathToMt4Name->setMinimumSize( QSize(0, 16) );
            tabList[idx]->pathToMt4Name->setFont( font1 );
            tabList[idx]->pathToMt4Name->setAlignment( Qt::AlignLeading|Qt::AlignLeft
                                                       |Qt::AlignVCenter );
            tabList[idx]->hLayoutPath->addWidget( tabList[idx]->pathToMt4Name );
            tabList[idx]->hLayoutPath->setStretch( 0, 1 );
            tabList[idx]->hLayoutPath->setStretch( 1, 2 );
            tabList[idx]->hLayoutPath->setStretch( 2, 1 );
            tabList[idx]->hLayoutPath->setStretch( 3, 2 );
            tabList[idx]->vLayoutTab->addWidget( tabList[idx]->hGBoxPathMt4 );
        } {// Input/Output Layers + Buttons
            tabList[idx]->hLayoutConf = new QHBoxLayout( tabList[idx]->kitTab );
            tabList[idx]->hLayoutConf->setSpacing(6);
            tabList[idx]->hLayoutConf->setObjectName( QStringLiteral("hLayoutConf") );
            tabList[idx]->hLayoutConf->setContentsMargins( 0, 0, 0, 0 );
            tabList[idx]->vGBoxInput = new QGroupBox( tabList[idx]->kitTab );
            tabList[idx]->vGBoxInput->setObjectName( QStringLiteral("vGBoxInput") );
            tabList[idx]->vGBoxInput->setAlignment( Qt::AlignLeading|Qt::AlignLeft
                                                    |Qt::AlignVCenter );
            tabList[idx]->vLayoutInput = new QVBoxLayout( tabList[idx]->vGBoxInput );
            tabList[idx]->vLayoutInput->setSpacing(6);
            tabList[idx]->vLayoutInput->setContentsMargins( 11, 11, 11, 11 );
            tabList[idx]->vLayoutInput->setObjectName( QStringLiteral("vLayoutInput") );
            tabList[idx]->vLayoutInput->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->inputListView = new QListView( tabList[idx]->vGBoxInput );
            tabList[idx]->inputListView->setObjectName( QStringLiteral("inputListView") );
            tabList[idx]->vLayoutInput->addWidget( tabList[idx]->inputListView );
            tabList[idx]->hLayoutInputSize = new QHBoxLayout( tabList[idx]->vGBoxInput );
            tabList[idx]->hLayoutInputSize->setSpacing(6);
            tabList[idx]->hLayoutInputSize->setObjectName( QStringLiteral("hLayoutInputSize") );
            tabList[idx]->hLayoutInputSize->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->inputLabel = new QLabel( tabList[idx]->vGBoxInput );
            tabList[idx]->inputLabel->setObjectName( QStringLiteral("inputLabel") );
            tabList[idx]->inputLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                                    |Qt::AlignVCenter );
            tabList[idx]->hLayoutInputSize->addWidget( tabList[idx]->inputLabel );
            tabList[idx]->inputSize = new QLabel( tabList[idx]->vGBoxInput );
            tabList[idx]->inputSize->setObjectName( QStringLiteral("inputSize") );
            tabList[idx]->hLayoutInputSize->addWidget( tabList[idx]->inputSize );
            tabList[idx]->hLayoutInputSize->setStretch( 0, 1 );
            tabList[idx]->hLayoutInputSize->setStretch( 1, 2 );
            tabList[idx]->vLayoutInput->addLayout( tabList[idx]->hLayoutInputSize );
            tabList[idx]->hLayoutConf->addWidget( tabList[idx]->vGBoxInput );
            tabList[idx]->vLayoutSymbol = new QVBoxLayout( tabList[idx]->kitTab );
            tabList[idx]->vLayoutSymbol->setSpacing(6);
            tabList[idx]->vLayoutSymbol->setObjectName( QStringLiteral("vLayoutSymbol") );
            tabList[idx]->vLayoutSymbol->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->verticalSpacer_2 = new QSpacerItem( 20, 40, QSizePolicy::Minimum,
                                                     QSizePolicy::Expanding );
            tabList[idx]->vLayoutSymbol->addItem( tabList[idx]->verticalSpacer_2 );
            tabList[idx]->arrowLabel = new QLabel( tabList[idx]->kitTab );
            tabList[idx]->arrowLabel->setObjectName( QStringLiteral("arrowLabel") );
            QSizePolicy sizePolicy( QSizePolicy::Preferred, QSizePolicy::Preferred );
            sizePolicy.setHorizontalStretch(0);
            sizePolicy.setVerticalStretch(0);
            sizePolicy.setHeightForWidth( tabList[idx]->arrowLabel->sizePolicy()
                                          .hasHeightForWidth() );
            tabList[idx]->arrowLabel->setSizePolicy( sizePolicy );
            tabList[idx]->arrowLabel->setMinimumSize( QSize(16, 16) );
            tabList[idx]->arrowLabel->setMaximumSize( QSize(64, 64) );
            tabList[idx]->arrowLabel->setAutoFillBackground(false);
            tabList[idx]->arrowLabel->setFrameShape( QFrame::NoFrame );
            tabList[idx]->arrowLabel->setFrameShadow( QFrame::Plain );
            tabList[idx]->arrowLabel->setTextFormat( Qt::AutoText );
            tabList[idx]->arrowLabel->setPixmap( QPixmap( QString::fromUtf8(":/img/right_64.png") ) );
            tabList[idx]->arrowLabel->setScaledContents(true);
            tabList[idx]->arrowLabel->setTextInteractionFlags( Qt::NoTextInteraction );
            tabList[idx]->vLayoutSymbol->addWidget( tabList[idx]->arrowLabel );
            tabList[idx]->verticalSpacer_3 = new QSpacerItem( 20, 40, QSizePolicy::Minimum,
                                                     QSizePolicy::Expanding );
            tabList[idx]->vLayoutSymbol->addItem( tabList[idx]->verticalSpacer_3 );
            tabList[idx]->vLayoutSymbol->setStretch( 0, 2 );
            tabList[idx]->vLayoutSymbol->setStretch( 1, 1 );
            tabList[idx]->vLayoutSymbol->setStretch( 2, 2 );
            tabList[idx]->hLayoutConf->addLayout( tabList[idx]->vLayoutSymbol );
            tabList[idx]->vGBoxOutput = new QGroupBox( tabList[idx]->kitTab );
            tabList[idx]->vGBoxOutput->setObjectName( QStringLiteral("vGBoxOutput") );
            tabList[idx]->vGBoxOutput->setAlignment( Qt::AlignLeading|Qt::AlignLeft
                                                     |Qt::AlignVCenter );
            tabList[idx]->vLayoutOutput = new QVBoxLayout( tabList[idx]->vGBoxOutput );
            tabList[idx]->vLayoutOutput->setSpacing(6);
            tabList[idx]->vLayoutOutput->setContentsMargins( 11, 11, 11, 11 );
            tabList[idx]->vLayoutOutput->setObjectName( QStringLiteral("vLayoutOutput") );
            tabList[idx]->vLayoutOutput->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->outputListView = new QListView( tabList[idx]->vGBoxOutput );
            tabList[idx]->outputListView->setObjectName( QStringLiteral("outputListView") );
            tabList[idx]->vLayoutOutput->addWidget( tabList[idx]->outputListView );
            tabList[idx]->hLayoutOutputSize = new QHBoxLayout( tabList[idx]->vGBoxOutput );
            tabList[idx]->hLayoutOutputSize->setSpacing(6);
            tabList[idx]->hLayoutOutputSize->setObjectName( QStringLiteral("hLayoutOutputSize") );
            tabList[idx]->hLayoutOutputSize->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->outputLabel = new QLabel( tabList[idx]->vGBoxOutput );
            tabList[idx]->outputLabel->setObjectName( QStringLiteral("outputLabel") );
            tabList[idx]->outputLabel->setLayoutDirection( Qt::LeftToRight );
            tabList[idx]->outputLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                                     |Qt::AlignVCenter );
            tabList[idx]->hLayoutOutputSize->addWidget( tabList[idx]->outputLabel );
            tabList[idx]->outputSize = new QLabel( tabList[idx]->vGBoxOutput );
            tabList[idx]->outputSize->setObjectName( QStringLiteral("outputSize") );
            tabList[idx]->hLayoutOutputSize->addWidget( tabList[idx]->outputSize );
            tabList[idx]->hLayoutOutputSize->setStretch( 0, 1 );
            tabList[idx]->hLayoutOutputSize->setStretch( 1, 2 );
            tabList[idx]->vLayoutOutput->addLayout( tabList[idx]->hLayoutOutputSize );
            tabList[idx]->hLayoutConf->addWidget( tabList[idx]->vGBoxOutput );
        } {//..// Buttons
            tabList[idx]->vLayoutButtons = new QVBoxLayout( tabList[idx]->kitTab );
            tabList[idx]->vLayoutButtons->setSpacing(6);
            tabList[idx]->vLayoutButtons->setObjectName( QStringLiteral("vLayoutButtons") );
            tabList[idx]->vLayoutButtons->setContentsMargins( 3, 3, 3, 3 );
            tabList[idx]->configurationButton = new QPushButton( tabList[idx]->kitTab );
            tabList[idx]->configurationButton->setObjectName( QStringLiteral("configurationButton") );
            QIcon icon9;
            icon9.addFile( QStringLiteral(":/img/gear_64.png"), QSize(),
                           QIcon::Normal, QIcon::Off );
            tabList[idx]->configurationButton->setIcon( icon9 );
            tabList[idx]->vLayoutButtons->addWidget( tabList[idx]->configurationButton );
            tabList[idx]->trainingButton = new QPushButton( tabList[idx]->kitTab );
            tabList[idx]->trainingButton->setObjectName( QStringLiteral("trainingButton") );
            QIcon icon91;
            icon91.addFile( QStringLiteral(":/img/clipboard_pencil_64.png"), QSize(),
                           QIcon::Normal, QIcon::Off );
            tabList[idx]->trainingButton->setIcon( icon91 );
            tabList[idx]->vLayoutButtons->addWidget( tabList[idx]->trainingButton );
            tabList[idx]->workButton = new QPushButton( tabList[idx]->kitTab );
            tabList[idx]->workButton->setObjectName( QStringLiteral("workButton") );
            QIcon icon92;
            icon92.addFile( QStringLiteral(":/img/statistics2_diagram_64.png"), QSize(),
                           QIcon::Normal, QIcon::Off );
            tabList[idx]->workButton->setIcon( icon92 );
            tabList[idx]->vLayoutButtons->addWidget( tabList[idx]->workButton );
            tabList[idx]->stopButton = new QPushButton( tabList[idx]->kitTab );
            tabList[idx]->stopButton->setObjectName( QStringLiteral("stopButton") );
            QIcon icon93;
            icon93.addFile( QStringLiteral(":/img/stop_64.png"), QSize(),
                           QIcon::Normal, QIcon::Off );
            tabList[idx]->stopButton->setIcon( icon93 );
            tabList[idx]->vLayoutButtons->addWidget( tabList[idx]->stopButton );
            tabList[idx]->deleteButton = new QPushButton( tabList[idx]->kitTab );
            tabList[idx]->deleteButton->setObjectName( QStringLiteral("deleteButton") );
            QIcon icon94;
            icon94.addFile( QStringLiteral(":/img/warning_64.png"), QSize(),
                           QIcon::Normal, QIcon::Off );
            tabList[idx]->deleteButton->setIcon( icon94 );
            tabList[idx]->vLayoutButtons->addWidget( tabList[idx]->deleteButton );
            tabList[idx]->verticalSpacer = new QSpacerItem( 20, 40, QSizePolicy::Minimum,
                                                            QSizePolicy::Expanding );
            tabList[idx]->vLayoutButtons->addItem( tabList[idx]->verticalSpacer );
            tabList[idx]->hLayoutConf->addLayout( tabList[idx]->vLayoutButtons );
            tabList[idx]->vLayoutTab->addLayout( tabList[idx]->hLayoutConf );
        } // Progress Bar
        tabList[idx]->progressBar = new QProgressBar( tabList[idx]->kitTab );
        tabList[idx]->progressBar->setObjectName( QStringLiteral("progressBar") );
        tabList[idx]->progressBar->setMaximum(100);
        tabList[idx]->progressBar->setValue(0);
        tabList[idx]->vLayoutTab->addWidget( tabList[idx]->progressBar );
        // Console
        tabList[idx]->consoleTextEdit = new QPlainTextEdit( tabList[idx]->kitTab );
        tabList[idx]->consoleTextEdit->setObjectName( QStringLiteral("consoleTextEdit") );
        tabList[idx]->consoleTextEdit->setReadOnly(true);
        tabList[idx]->vLayoutTab->addWidget( tabList[idx]->consoleTextEdit );
        tabList[idx]->vLayoutTab->setStretch( 2, 2 );
        tabList[idx]->vLayoutTab->setStretch( 4, 2 );
        QIcon icon10;
        icon10.addFile( QStringLiteral(":/img/briefcase_64.png"),
                        QSize(), QIcon::Normal, QIcon::Off );
        ui->vTabWidget->addTab( tabList[idx]->kitTab, icon10, QString() );
        updateTab( idx );
    } catch(...) {   // setupUi
        errorMessage( "MainWindow", tr("Open %1 tab error!").arg(name) );
        delete tabList[idx]->kitTab;
        delete tabList[idx]->verticalSpacer;
        delete tabList[idx]->verticalSpacer_2;
        delete tabList[idx]->verticalSpacer_3;
    }
    {   // retranslateUi
        tabList[idx]->nameKitLabel->setText(QApplication::translate("MainWindow",
                                                             "Kit name :", 0));
        tabList[idx]->nameKitName->setText(QString());
        tabList[idx]->serverLabel->setText(QApplication::translate("MainWindow",
                                                            "Server :", 0));
        tabList[idx]->serverName->setText(QString());
        tabList[idx]->pathToMt4Label->setText(QApplication::translate("MainWindow",
                                                               "Path to MT4 :", 0));
        tabList[idx]->pathToMt4Name->setText(QString());
        tabList[idx]->vGBoxInput->setTitle(QApplication::translate("MainWindow",
                                                            "Input neural network :", 0));
        tabList[idx]->inputLabel->setText(QApplication::translate("MainWindow",
                                                           "History size :", 0));
        tabList[idx]->inputSize->setText(QString());
        tabList[idx]->arrowLabel->setText(QString());
        tabList[idx]->vGBoxOutput->setTitle(QApplication::translate("MainWindow",
                                                             "Output neural network :", 0));
        tabList[idx]->outputLabel->setText(QApplication::translate("MainWindow",
                                                            "Prediction size :", 0));
        tabList[idx]->outputSize->setText(QString());
        tabList[idx]->configurationButton->setText(QApplication::translate("MainWindow",
                                                                    "Configuration", 0));
        tabList[idx]->trainingButton->setText(QApplication::translate("MainWindow",
                                                                    "Train", 0));
        tabList[idx]->workButton->setText(QApplication::translate("MainWindow",
                                                                    "Run work", 0));
        tabList[idx]->stopButton->setText(QApplication::translate("MainWindow",
                                                                    "Stop", 0));
        tabList[idx]->deleteButton->setText(QApplication::translate("MainWindow",
                                                                    "Delete", 0));
        tabList[idx]->progressBar->setFormat(QApplication::translate("MainWindow",
                                                                     "%p%", 0));
    }   // retranslateUi
    addTabConnections( idx );
}

void MainWindow::addTabConnections(const qint32 idx)
{
    connect( tabList[idx]->configurationButton, &QPushButton::clicked,
             this, &MainWindow::openKitConfig );
    connect( tabList[idx]->trainingButton, &QPushButton::clicked,
             this, &MainWindow::runTraining );
    connect( tabList[idx]->workButton, &QPushButton::clicked,
             this, &MainWindow::runWork );
    connect( tabList[idx]->stopButton, &QPushButton::clicked,
             this, &MainWindow::stopWork );
    connect( tabList[idx]->deleteButton, &QPushButton::clicked,
             this, &MainWindow::delete_Kit );
}

void MainWindow::deleteTabFromUi(const qint32 idx)
{
    try {
        disconnect( tabList[idx]->configurationButton, &QPushButton::clicked,
                    this, &MainWindow::openKitConfig );
        disconnect( tabList[idx]->trainingButton, &QPushButton::clicked,
                    this, &MainWindow::runTraining );
        disconnect( tabList[idx]->workButton, &QPushButton::clicked,
                    this, &MainWindow::runWork );
        disconnect( tabList[idx]->stopButton, &QPushButton::clicked,
                    this, &MainWindow::stopWork );
        disconnect( tabList[idx]->deleteButton, &QPushButton::clicked,
                    this, &MainWindow::delete_Kit );
        delete tabList[idx]->kitTab;
        delete tabList[idx];
        tabList.removeAt( idx );
    } catch(...) {
        errorMessage( "MainWindow", tr("deleteTabFromUi() error") );
    }
}

void MainWindow::closeEvent(QCloseEvent *event)
{
    /*if (maybeSave()) {
        writeSettings();
        event->accept();
    } else {
        event->ignore();
    } */
    event->accept();
}

