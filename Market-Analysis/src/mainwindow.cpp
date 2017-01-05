#include "include/mainwindow.h"
#include "ui_mainwindow.h"
#include <QApplication>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    setConnections();
}

MainWindow::~MainWindow()
{
    delete ui;
}

Ui::MainWindow *MainWindow::getUi()
{
    return ui;
}

void MainWindow::updateActions(bool kitActions[])
{
    ui->actionKit_Configuration->setEnabled( kitActions[0] );
    ui->actionTrain_NN->setEnabled( kitActions[1] );
    ui->actionStart_forecasting->setEnabled( kitActions[2] );
    ui->actionStop->setEnabled( kitActions[3] );
    ui->actionDelete_Kit->setEnabled( kitActions[4] );
}

void MainWindow::addNewTab(const QString name, const MainWindow::KitTabWidget *tab)
{
    QIcon icon10;
    icon10.addFile( QStringLiteral(":/img/briefcase_64.png"),
                    QSize(), QIcon::Normal, QIcon::Off );
    ui->vTabWidget->addTab( tab->kitTab, icon10, name );
    newTabConnections( tab );
}

//void MainWindow::errorMessage(const QString kit, const QString text)
//{
//}

void MainWindow::addNew()
{
    emit addNewKit();
}

void MainWindow::open()
{
    emit openKit();
}

void MainWindow::save()
{
    if( ui->vTabWidget->count() > 0 )
        emit saveKit( ui->vTabWidget->currentWidget()->objectName() );
}

void MainWindow::closeTab()
{
    if( ui->vTabWidget->count() > 0 )
        closeTab( ui->vTabWidget->currentIndex() );
}

void MainWindow::openSettings()
{
    emit settings();
}

void MainWindow::openKitConfig()
{
    if( ui->vTabWidget->count() > 0 )
        emit kitConfigs( ui->vTabWidget->currentWidget()->objectName() );
}

void MainWindow::runTraining()
{
    if( ui->vTabWidget->count() > 0 )
        emit runTrainingKit( ui->vTabWidget->currentWidget()->objectName() );
}

void MainWindow::runWork()
{
    if( ui->vTabWidget->count() > 0 )
        emit runWorkKit( ui->vTabWidget->currentWidget()->objectName() );
}

void MainWindow::stopWork()
{
    if( ui->vTabWidget->count() > 0 )
        emit stopWorkKit( ui->vTabWidget->currentWidget()->objectName() );
}

void MainWindow::delete_Kit()
{
    if( ui->vTabWidget->count() > 0 ) {
        QString selected = ui->vTabWidget->currentWidget()->objectName();
        if( QMessageBox::Yes == QMessageBox::question( this, tr("Delete Kit?"),
                                                       tr("Are you sure that you want to delete set \"%1\"?")
                                                       .arg(selected) ) ) {
            closeTab( ui->vTabWidget->currentIndex() );
            emit deleteKit( selected );
        }
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
                        tr("The <b>Market Analysis System</b>. \
                            Version %1. \
                            Developed %2. \
                            %3 ")
                           .arg( QApplication::applicationVersion() )
                           .arg( QApplication::organizationName() )
                           .arg( QApplication::organizationDomain() ) );
}

void MainWindow::closeTab(const qint32 idx)
{
    if( ui->vTabWidget->currentIndex() != idx )
        return;
    QString selected = ui->vTabWidget->currentWidget()->objectName();
//    if( QMessageBox::Yes == QMessageBox::question( this, tr("Save Kit?"),
//                                                   tr("Are you sure that you want to delete set \"%1\"?")
//                                                   .arg( selected ) ) ) {
//        emit closedKit( selected );
//    }
    //deleteTabConnections(); ?
    ui->vTabWidget->currentWidget()->close();
    emit closedKit( selected );
}

void MainWindow::setCurrentTab(const qint32 idx)
{
    currentTabId = idx;
    if( ui->vTabWidget->count() > 0 )
        emit currentTab( ui->vTabWidget->currentWidget()->objectName() );
}

//          to presenter
//void MainWindow::updateTab(const qint32 idx)
//{
//    if( currentTab < 0 )
//        return;
//    KitTabWidget *tab = tabList[idx];
//    if( tab->name != tab->config->nameKit )
//        setTabName( idx, tab->config->nameKit );
//    tab->serverName->setText( tab->config->server );
//    tab->pathToMt4Name->setText( tab->config->mt4Path );
//    tab->inputListView = tab->config;
//    tab->outputListView = tab->config;
//    tab->inputSize->setText( QString("%1").arg(tab->config->depthHistory) ); // * tab->config->'inList'
//    tab->outputSize->setText( QString("%1").arg(tab->config->depthPrediction) ); // * tab->config->'outList'
//    tab->progressBar->setValue( tab->config->progress );
//    updateTabButtons( idx );
//}

//void MainWindow::updateTabButtons(const qint32 idx)
//{
//    if( currentTab < 0 )
//        return;
//    KitTabWidget *tab = tabList[idx];
//    tab->configurationButton->setEnabled( !tab->config->isRun );
//    ui->actionKit_Configuration->setEnabled( !tab->config->isRun );
//    tab->trainingButton->setEnabled( !tab->config->isRun );
//    ui->actionTrain_NN->setEnabled( !tab->config->isTrained );
//    tab->workButton->setEnabled( !tab->config->isRun );
//    ui->actionStart_forecasting->setEnabled( !tab->config->isRun );
//    tab->stopButton->setEnabled( tab->config->isRun );
//    ui->actionStop->setEnabled( tab->config->isRun );
//    tab->deleteButton->setEnabled( !tab->config->isRun );
//    ui->actionDelete_Kit->setEnabled( !tab->config->isRun );
//}

void MainWindow::setConnections()
{
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
             this, SLOT( setCurrentTab(qint32) ) );
}

void MainWindow::newTabConnections(const KitTabWidget *tab)
{
    connect( tab->configurationButton, &QPushButton::clicked,
             this, &MainWindow::openKitConfig );
    connect( tab->trainingButton, &QPushButton::clicked,
             this, &MainWindow::runTraining );
    connect( tab->workButton, &QPushButton::clicked,
             this, &MainWindow::runWork );
    connect( tab->stopButton, &QPushButton::clicked,
             this, &MainWindow::stopWork );
    connect( tab->deleteButton, &QPushButton::clicked,
             this, &MainWindow::delete_Kit );
}

void MainWindow::deleteTabConnections(const KitTabWidget *tab)
{
    disconnect( tab->configurationButton, &QPushButton::clicked,
                this, &MainWindow::openKitConfig );
    disconnect( tab->trainingButton, &QPushButton::clicked,
                this, &MainWindow::runTraining );
    disconnect( tab->workButton, &QPushButton::clicked,
                this, &MainWindow::runWork );
    disconnect( tab->stopButton, &QPushButton::clicked,
                this, &MainWindow::stopWork );
    disconnect( tab->deleteButton, &QPushButton::clicked,
                this, &MainWindow::delete_Kit );
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


MainWindow::KitTabWidget::KitTabWidget(MainWindow *parent, QString name) :
    parent(parent),
    name(name)
{
    kitTab = new QWidget( parent->getUi()->vTabWidget );
    kitTab->setObjectName( name );
    vLayoutTab = new QVBoxLayout( kitTab );
    vLayoutTab->setSpacing(6);
    vLayoutTab->setContentsMargins( 11, 11, 11, 11 );
    vLayoutTab->setObjectName( QStringLiteral("vLayoutTab") );
    {// Name
        hGBoxKitName = new QGroupBox( kitTab );
        hGBoxKitName->setObjectName( QStringLiteral("hGBoxKitName") );
        hLayoutName = new QHBoxLayout( hGBoxKitName );
        hLayoutName->setSpacing(6);
        hLayoutName->setContentsMargins( 11, 11, 11, 11 );
        hLayoutName->setObjectName( QStringLiteral("hLayoutName") );
        hLayoutName->setContentsMargins( 3, 3, 3, 3 );
        nameKitLabel = new QLabel( hGBoxKitName );
        nameKitLabel->setObjectName( QStringLiteral("nameKitLabel") );
        nameKitLabel->setMinimumSize( QSize(0, 16) );
        nameKitLabel->setBaseSize( QSize(0, 0) );
        QFont font;
        font.setPointSize(11);
        nameKitLabel->setFont( font );
        nameKitLabel->setFrameShape( QFrame::NoFrame );
        nameKitLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                    |Qt::AlignVCenter );
        hLayoutName->addWidget( nameKitLabel );
        nameKitName = new QLabel( hGBoxKitName );
        nameKitName->setObjectName( QStringLiteral("nameKitName") );
        nameKitName->setMinimumSize( QSize(0, 16) );
        nameKitName->setFont( font );
        hLayoutName->addWidget( nameKitName );
        hLayoutName->setStretch( 0, 1 );
        hLayoutName->setStretch( 1, 5 );
        vLayoutTab->addWidget( hGBoxKitName );
    } {// Server + MT4 Path
        hGBoxPathMt4 = new QGroupBox( kitTab );
        hGBoxPathMt4->setObjectName( QStringLiteral("hGBoxPathMt4") );
        hLayoutPath = new QHBoxLayout( hGBoxPathMt4 );
        hLayoutPath->setSpacing(6);
        hLayoutPath->setContentsMargins( 11, 11, 11, 11 );
        hLayoutPath->setObjectName( QStringLiteral("hLayoutPath") );
        hLayoutPath->setContentsMargins( 3, 3, 3, 3 );
        serverLabel = new QLabel( hGBoxPathMt4 );
        serverLabel->setObjectName( QStringLiteral("serverLabel") );
        serverLabel->setMinimumSize( QSize(0, 16) );
        QFont font1;
        font1.setPointSize(9);
        serverLabel->setFont( font1 );
        serverLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                   |Qt::AlignVCenter );
        hLayoutPath->addWidget( serverLabel );
        serverName = new QLabel( hGBoxPathMt4 );
        serverName->setObjectName( QStringLiteral("serverName") );
        serverName->setMinimumSize( QSize(0, 16) );
        serverName->setFont( font1 );
        hLayoutPath->addWidget( serverName );
        pathToMt4Label = new QLabel( hGBoxPathMt4 );
        pathToMt4Label->setObjectName( QStringLiteral("pathToMt4Label") );
        pathToMt4Label->setMinimumSize( QSize(0, 16) );
        pathToMt4Label->setFont( font1 );
        pathToMt4Label->setFrameShape( QFrame::NoFrame );
        pathToMt4Label->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                      |Qt::AlignVCenter );
        hLayoutPath->addWidget( pathToMt4Label );
        pathToMt4Name = new QLabel( hGBoxPathMt4 );
        pathToMt4Name->setObjectName( QStringLiteral("pathToMt4Name") );
        pathToMt4Name->setMinimumSize( QSize(0, 16) );
        pathToMt4Name->setFont( font1 );
        pathToMt4Name->setAlignment( Qt::AlignLeading|Qt::AlignLeft
                                     |Qt::AlignVCenter );
        hLayoutPath->addWidget( pathToMt4Name );
        hLayoutPath->setStretch( 0, 1 );
        hLayoutPath->setStretch( 1, 2 );
        hLayoutPath->setStretch( 2, 1 );
        hLayoutPath->setStretch( 3, 2 );
        vLayoutTab->addWidget( hGBoxPathMt4 );
    } {// Input/Output Layers + Buttons
        hLayoutConf = new QHBoxLayout( kitTab );
        hLayoutConf->setSpacing(6);
        hLayoutConf->setObjectName( QStringLiteral("hLayoutConf") );
        hLayoutConf->setContentsMargins( 0, 0, 0, 0 );
        vGBoxInput = new QGroupBox( kitTab );
        vGBoxInput->setObjectName( QStringLiteral("vGBoxInput") );
        vGBoxInput->setAlignment( Qt::AlignLeading|Qt::AlignLeft
                                  |Qt::AlignVCenter );
        vLayoutInput = new QVBoxLayout( vGBoxInput );
        vLayoutInput->setSpacing(6);
        vLayoutInput->setContentsMargins( 11, 11, 11, 11 );
        vLayoutInput->setObjectName( QStringLiteral("vLayoutInput") );
        vLayoutInput->setContentsMargins( 3, 3, 3, 3 );
        inputListView = new QListView( vGBoxInput );
        inputListView->setObjectName( QStringLiteral("inputListView") );
        vLayoutInput->addWidget( inputListView );
        hLayoutInputSize = new QHBoxLayout( vGBoxInput );
        hLayoutInputSize->setSpacing(6);
        hLayoutInputSize->setObjectName( QStringLiteral("hLayoutInputSize") );
        hLayoutInputSize->setContentsMargins( 3, 3, 3, 3 );
        inputLabel = new QLabel( vGBoxInput );
        inputLabel->setObjectName( QStringLiteral("inputLabel") );
        inputLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                  |Qt::AlignVCenter );
        hLayoutInputSize->addWidget( inputLabel );
        inputSize = new QLabel( vGBoxInput );
        inputSize->setObjectName( QStringLiteral("inputSize") );
        hLayoutInputSize->addWidget( inputSize );
        hLayoutInputSize->setStretch( 0, 1 );
        hLayoutInputSize->setStretch( 1, 2 );
        vLayoutInput->addLayout( hLayoutInputSize );
        hLayoutConf->addWidget( vGBoxInput );
        vLayoutSymbol = new QVBoxLayout( kitTab );
        vLayoutSymbol->setSpacing(6);
        vLayoutSymbol->setObjectName( QStringLiteral("vLayoutSymbol") );
        vLayoutSymbol->setContentsMargins( 3, 3, 3, 3 );
        verticalSpacer_2 = new QSpacerItem( 20, 40, QSizePolicy::Minimum,
                                   QSizePolicy::Expanding );
        vLayoutSymbol->addItem( verticalSpacer_2 );
        arrowLabel = new QLabel( kitTab );
        arrowLabel->setObjectName( QStringLiteral("arrowLabel") );
        QSizePolicy sizePolicy( QSizePolicy::Preferred, QSizePolicy::Preferred );
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth( arrowLabel->sizePolicy()
                                      .hasHeightForWidth() );
        arrowLabel->setSizePolicy( sizePolicy );
        arrowLabel->setMinimumSize( QSize(16, 16) );
        arrowLabel->setMaximumSize( QSize(64, 64) );
        arrowLabel->setAutoFillBackground(false);
        arrowLabel->setFrameShape( QFrame::NoFrame );
        arrowLabel->setFrameShadow( QFrame::Plain );
        arrowLabel->setTextFormat( Qt::AutoText );
        arrowLabel->setPixmap( QPixmap( QString::fromUtf8(":/img/right_64.png") ) );
        arrowLabel->setScaledContents(true);
        arrowLabel->setTextInteractionFlags( Qt::NoTextInteraction );
        vLayoutSymbol->addWidget( arrowLabel );
        verticalSpacer_3 = new QSpacerItem( 20, 40, QSizePolicy::Minimum,
                                   QSizePolicy::Expanding );
        vLayoutSymbol->addItem( verticalSpacer_3 );
        vLayoutSymbol->setStretch( 0, 2 );
        vLayoutSymbol->setStretch( 1, 1 );
        vLayoutSymbol->setStretch( 2, 2 );
        hLayoutConf->addLayout( vLayoutSymbol );
        vGBoxOutput = new QGroupBox( kitTab );
        vGBoxOutput->setObjectName( QStringLiteral("vGBoxOutput") );
        vGBoxOutput->setAlignment( Qt::AlignLeading|Qt::AlignLeft
                                   |Qt::AlignVCenter );
        vLayoutOutput = new QVBoxLayout( vGBoxOutput );
        vLayoutOutput->setSpacing(6);
        vLayoutOutput->setContentsMargins( 11, 11, 11, 11 );
        vLayoutOutput->setObjectName( QStringLiteral("vLayoutOutput") );
        vLayoutOutput->setContentsMargins( 3, 3, 3, 3 );
        outputListView = new QListView( vGBoxOutput );
        outputListView->setObjectName( QStringLiteral("outputListView") );
        vLayoutOutput->addWidget( outputListView );
        hLayoutOutputSize = new QHBoxLayout( vGBoxOutput );
        hLayoutOutputSize->setSpacing(6);
        hLayoutOutputSize->setObjectName( QStringLiteral("hLayoutOutputSize") );
        hLayoutOutputSize->setContentsMargins( 3, 3, 3, 3 );
        outputLabel = new QLabel( vGBoxOutput );
        outputLabel->setObjectName( QStringLiteral("outputLabel") );
        outputLabel->setLayoutDirection( Qt::LeftToRight );
        outputLabel->setAlignment( Qt::AlignRight|Qt::AlignTrailing
                                   |Qt::AlignVCenter );
        hLayoutOutputSize->addWidget( outputLabel );
        outputSize = new QLabel( vGBoxOutput );
        outputSize->setObjectName( QStringLiteral("outputSize") );
        hLayoutOutputSize->addWidget( outputSize );
        hLayoutOutputSize->setStretch( 0, 1 );
        hLayoutOutputSize->setStretch( 1, 2 );
        vLayoutOutput->addLayout( hLayoutOutputSize );
        hLayoutConf->addWidget( vGBoxOutput );
    } {//..// Buttons
        vLayoutButtons = new QVBoxLayout( kitTab );
        vLayoutButtons->setSpacing(6);
        vLayoutButtons->setObjectName( QStringLiteral("vLayoutButtons") );
        vLayoutButtons->setContentsMargins( 3, 3, 3, 3 );
        configurationButton = new QPushButton( kitTab );
        configurationButton->setObjectName( QStringLiteral("configurationButton") );
        QIcon icon9;
        icon9.addFile( QStringLiteral(":/img/gear_64.png"), QSize(),
                       QIcon::Normal, QIcon::Off );
        configurationButton->setIcon( icon9 );
        vLayoutButtons->addWidget( configurationButton );
        trainingButton = new QPushButton( kitTab );
        trainingButton->setObjectName( QStringLiteral("trainingButton") );
        QIcon icon91;
        icon91.addFile( QStringLiteral(":/img/clipboard_pencil_64.png"), QSize(),
                       QIcon::Normal, QIcon::Off );
        trainingButton->setIcon( icon91 );
        vLayoutButtons->addWidget( trainingButton );
        workButton = new QPushButton( kitTab );
        workButton->setObjectName( QStringLiteral("workButton") );
        QIcon icon92;
        icon92.addFile( QStringLiteral(":/img/statistics2_diagram_64.png"), QSize(),
                       QIcon::Normal, QIcon::Off );
        workButton->setIcon( icon92 );
        vLayoutButtons->addWidget( workButton );
        stopButton = new QPushButton( kitTab );
        stopButton->setObjectName( QStringLiteral("stopButton") );
        QIcon icon93;
        icon93.addFile( QStringLiteral(":/img/stop_64.png"), QSize(),
                       QIcon::Normal, QIcon::Off );
        stopButton->setIcon( icon93 );
        vLayoutButtons->addWidget( stopButton );
        deleteButton = new QPushButton( kitTab );
        deleteButton->setObjectName( QStringLiteral("deleteButton") );
        QIcon icon94;
        icon94.addFile( QStringLiteral(":/img/warning_64.png"), QSize(),
                       QIcon::Normal, QIcon::Off );
        deleteButton->setIcon( icon94 );
        vLayoutButtons->addWidget( deleteButton );
        verticalSpacer = new QSpacerItem( 20, 40, QSizePolicy::Minimum,
                                          QSizePolicy::Expanding );
        vLayoutButtons->addItem( verticalSpacer );
        hLayoutConf->addLayout( vLayoutButtons );
        vLayoutTab->addLayout( hLayoutConf );
    } // Progress Bar
    progressBar = new QProgressBar( kitTab );
    progressBar->setObjectName( QStringLiteral("progressBar") );
    progressBar->setMaximum(100);
    progressBar->setValue(0);
    vLayoutTab->addWidget( progressBar );
    // Console
    consoleTextEdit = new QPlainTextEdit( kitTab );
    consoleTextEdit->setObjectName( QStringLiteral("consoleTextEdit") );
    consoleTextEdit->setReadOnly(true);
    vLayoutTab->addWidget( consoleTextEdit );
    vLayoutTab->setStretch( 2, 2 );
    vLayoutTab->setStretch( 4, 2 );

    // retranslateUi
    nameKitLabel->setText(QApplication::translate("MainWindow", "Kit name :", 0));
    nameKitName->setText(QString());
    serverLabel->setText(QApplication::translate("MainWindow", "Server :", 0));
    serverName->setText(QString());
    pathToMt4Label->setText(QApplication::translate("MainWindow", "Path to MT4 :", 0));
    pathToMt4Name->setText(QString());
    vGBoxInput->setTitle(QApplication::translate("MainWindow",
                                          "Input neural network :", 0));
    inputLabel->setText(QApplication::translate("MainWindow", "History size :", 0));
    inputSize->setText(QString());
    arrowLabel->setText(QString());
    vGBoxOutput->setTitle(QApplication::translate("MainWindow",
                                                  "Output neural network :", 0));
    outputLabel->setText(QApplication::translate("MainWindow",
                                                 "Prediction size :", 0));
    outputSize->setText(QString());
    configurationButton->setText(QApplication::translate("MainWindow",
                                                         "Configuration", 0));
    trainingButton->setText(QApplication::translate("MainWindow", "Train", 0));
    workButton->setText(QApplication::translate("MainWindow", "Run work", 0));
    stopButton->setText(QApplication::translate("MainWindow", "Stop", 0));
    deleteButton->setText(QApplication::translate("MainWindow", "Delete", 0));
    progressBar->setFormat(QApplication::translate("MainWindow", "%p%", 0));
}

MainWindow::KitTabWidget::~KitTabWidget()
{
    delete verticalSpacer;
    delete verticalSpacer_2;
    delete verticalSpacer_3;
    delete kitTab;
}
