#include "include/mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    presenter(new Presenter(this))
{
    ui->setupUi(this);

    setConnections();

    this->openTab( 0 );
    currentTab = 0;
    countTabs = 1;
}

MainWindow::~MainWindow()
{
    delete ui;
    delete presenter;
}

void MainWindow::openKit()
{
    this->openTab(countTabs);
    currentTab = countTabs;
    countTabs++;
}

void MainWindow::openTab(qint32 idx)
{
    if( idx > MAX_TAB ) {
        ui->statusBar->setStatusTip( tr("The Maximum number of Open kits - %1")
                                     .arg( MAX_TAB) );
        return;
    }
    this->addTabToUi( idx );
    this->addTabConnections( idx );
    emit opened( idx );
}

void MainWindow::closeTab(qint32 idx)
{

}

void MainWindow::selectTab(qint32 idx)
{

}

void MainWindow::setConnections()
{
    connect( ui->actionNew_Kit, &QAction::triggered, this, &MainWindow::newKit );
    connect( ui->actionOpen_Kit, &QAction::triggered, this, &MainWindow::openKit );
    connect( ui->actionSave_Kit, &QAction::triggered, this, &MainWindow::saveKit );
    connect( ui->actionClose_Kit, &QAction::triggered, this, &MainWindow::closeKit );
    connect( ui->actionSettings, &QAction::triggered, this, &MainWindow::openSettings );
    connect( ui->actionKit_Configuration, &QAction::triggered,
             this, &MainWindow::openKitConfig );
    connect( ui->actionTrain_NN, &QAction::triggered, this, &MainWindow::runTraining );
    connect( ui->actionStart_forecasting, &QAction::triggered,
             this, &MainWindow::runWork );
    connect( ui->actionStop, &QAction::triggered, this, &MainWindow::stopWork );
    connect( ui->actionDelete_Kit, &QAction::triggered, this, &MainWindow::deleteKit );
    connect( ui->actionHelp, &QAction::triggered, this, &MainWindow::openHelp );
    connect( ui->actionAbout, &QAction::triggered, this, &MainWindow::openAbout );
    connect( ui->actionExit, &QAction::triggered, this, &MainWindow::close );
}

void MainWindow::addTabToUi(qint32 idx)
{
    try {       // setupUi
        kitTab.append( new QWidget( ui->vTabWidget ) );
        kitTab[ idx ]->setObjectName( QString("MAS Kit #").arg( idx + 1 ));
        vLayoutTab.append( new QVBoxLayout( kitTab[ idx ] ) );
        vLayoutTab[ idx ]->setSpacing(6);
        vLayoutTab[ idx ]->setContentsMargins(11, 11, 11, 11);
        vLayoutTab[ idx ]->setObjectName(QStringLiteral("vLayoutTab"));

        hGBoxKitName.append( new QGroupBox( kitTab[ idx ] ) );
        hGBoxKitName[ idx ]->setObjectName(QStringLiteral("hGBoxKitName"));
        hLayoutName.append( new QHBoxLayout( hGBoxKitName[ idx ] ) );
        hLayoutName[ idx ]->setSpacing(6);
        hLayoutName[ idx ]->setContentsMargins(11, 11, 11, 11);
        hLayoutName[ idx ]->setObjectName(QStringLiteral("hLayoutName"));
        hLayoutName[ idx ]->setContentsMargins(3, 3, 3, 3);
        nameKitLabel.append( new QLabel( hGBoxKitName[ idx ] ) );
        nameKitLabel[ idx ]->setObjectName(QStringLiteral("nameKitLabel"));
        nameKitLabel[ idx ]->setMinimumSize(QSize(0, 16));
        nameKitLabel[ idx ]->setBaseSize(QSize(0, 0));
        QFont font;
        font.setPointSize(11);
        nameKitLabel[ idx ]->setFont(font);
        nameKitLabel[ idx ]->setFrameShape(QFrame::NoFrame);
        nameKitLabel[ idx ]->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        hLayoutName[ idx ]->addWidget(nameKitLabel[ idx ]);
        nameKitName.append( new QLabel( hGBoxKitName[ idx ] ) );
        nameKitName[ idx ]->setObjectName(QStringLiteral("nameKitName"));
        nameKitName[ idx ]->setMinimumSize(QSize(0, 16));
        nameKitName[ idx ]->setFont(font);
        hLayoutName[ idx ]->addWidget(nameKitName[ idx ]);
        hLayoutName[ idx ]->setStretch(0, 1);
        hLayoutName[ idx ]->setStretch(1, 5);
        vLayoutTab[ idx ]->addWidget( hGBoxKitName[ idx ] );

        hGBoxPathMt4.append( new QGroupBox( kitTab[ idx ] ) );
        hGBoxPathMt4[ idx ]->setObjectName(QStringLiteral("hGBoxPathMt4"));
        hLayoutPath.append( new QHBoxLayout( hGBoxPathMt4[ idx ] ) );
        hLayoutPath[ idx ]->setSpacing(6);
        hLayoutPath[ idx ]->setContentsMargins(11, 11, 11, 11);
        hLayoutPath[ idx ]->setObjectName(QStringLiteral("hLayoutPath"));
        hLayoutPath[ idx ]->setContentsMargins(3, 3, 3, 3);
        serverLabel.append( new QLabel( hGBoxPathMt4[ idx ] ) );
        serverLabel[ idx ]->setObjectName(QStringLiteral("serverLabel"));
        serverLabel[ idx ]->setMinimumSize(QSize(0, 16));
        QFont font1;
        font1.setPointSize(9);
        serverLabel[ idx ]->setFont(font1);
        serverLabel[ idx ]->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        hLayoutPath[ idx ]->addWidget(serverLabel[ idx ]);
        serverName.append( new QLabel( hGBoxPathMt4[ idx ] ) );
        serverName[ idx ]->setObjectName(QStringLiteral("serverName"));
        serverName[ idx ]->setMinimumSize(QSize(0, 16));
        serverName[ idx ]->setFont(font1);
        hLayoutPath[ idx ]->addWidget(serverName[ idx ]);
        pathToMt4Label.append( new QLabel( hGBoxPathMt4[ idx ] ) );
        pathToMt4Label[ idx ]->setObjectName(QStringLiteral("pathToMt4Label"));
        pathToMt4Label[ idx ]->setMinimumSize(QSize(0, 16));
        pathToMt4Label[ idx ]->setFont(font1);
        pathToMt4Label[ idx ]->setFrameShape(QFrame::NoFrame);
        pathToMt4Label[ idx ]->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        hLayoutPath[ idx ]->addWidget(pathToMt4Label[ idx ]);
        pathToMt4Name.append( new QLabel( hGBoxPathMt4[ idx ] ) );
        pathToMt4Name[ idx ]->setObjectName(QStringLiteral("pathToMt4Name"));
        pathToMt4Name[ idx ]->setMinimumSize(QSize(0, 16));
        pathToMt4Name[ idx ]->setFont(font1);
        pathToMt4Name[ idx ]->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);
        hLayoutPath[ idx ]->addWidget(pathToMt4Name[ idx ]);
        hLayoutPath[ idx ]->setStretch(0, 1);
        hLayoutPath[ idx ]->setStretch(1, 2);
        hLayoutPath[ idx ]->setStretch(2, 1);
        hLayoutPath[ idx ]->setStretch(3, 2);
        vLayoutTab[ idx ]->addWidget( hGBoxPathMt4[ idx ] );

        hLayoutConf.append( new QHBoxLayout( kitTab[ idx ] ) );
        hLayoutConf[ idx ]->setSpacing(6);
        hLayoutConf[ idx ]->setObjectName(QStringLiteral("hLayoutConf"));
        hLayoutConf[ idx ]->setContentsMargins(0, 0, 0, 0);
        vGBoxInput.append( new QGroupBox( kitTab[ idx ] ) );
        vGBoxInput[ idx ]->setObjectName(QStringLiteral("vGBoxInput"));
        vGBoxInput[ idx ]->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);
        vGBoxInput[ idx ]->setFlat(false);
        vLayoutInput.append( new QVBoxLayout( vGBoxInput[ idx ] ) );
        vLayoutInput[ idx ]->setSpacing(6);
        vLayoutInput[ idx ]->setContentsMargins(11, 11, 11, 11);
        vLayoutInput[ idx ]->setObjectName(QStringLiteral("vLayoutInput"));
        vLayoutInput[ idx ]->setContentsMargins(3, 3, 3, 3);
        inputListView.append( new QListView( vGBoxInput[ idx ] ) );
        inputListView[ idx ]->setObjectName(QStringLiteral("inputListView"));
        vLayoutInput[ idx ]->addWidget(inputListView[ idx ]);
        hLayoutInputSize.append( new QHBoxLayout( vGBoxInput[ idx ] ) );
        hLayoutInputSize[ idx ]->setSpacing(6);
        hLayoutInputSize[ idx ]->setObjectName(QStringLiteral("hLayoutInputSize"));
        hLayoutInputSize[ idx ]->setContentsMargins(3, 3, 3, 3);
        inputLabel.append( new QLabel( vGBoxInput[ idx ] ) );
        inputLabel[ idx ]->setObjectName(QStringLiteral("inputLabel"));
        inputLabel[ idx ]->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        hLayoutInputSize[ idx ]->addWidget(inputLabel[ idx ]);
        inputSize.append( new QLabel( vGBoxInput[ idx ] ) );
        inputSize[ idx ]->setObjectName(QStringLiteral("inputSize"));
        hLayoutInputSize[ idx ]->addWidget(inputSize[ idx ]);
        hLayoutInputSize[ idx ]->setStretch(0, 1);
        hLayoutInputSize[ idx ]->setStretch(1, 2);
        vLayoutInput[ idx ]->addLayout(hLayoutInputSize[ idx ]);
        hLayoutConf[ idx ]->addWidget(vGBoxInput[ idx ]);
        vLayoutSymbol.append( new QVBoxLayout( kitTab[ idx ] ) );
        vLayoutSymbol[ idx ]->setSpacing(6);
        vLayoutSymbol[ idx ]->setObjectName(QStringLiteral("vLayoutSymbol"));
        vLayoutSymbol[ idx ]->setContentsMargins(3, 3, 3, 3);
        verticalSpacer_2.append( new QSpacerItem(20, 40, QSizePolicy::Minimum,
                                                 QSizePolicy::Expanding) );
        vLayoutSymbol[ idx ]->addItem(verticalSpacer_2[ idx ]);
        arrowLabel.append( new QLabel( kitTab[ idx ] ) );
        arrowLabel[ idx ]->setObjectName(QStringLiteral("arrowLabel"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(arrowLabel[ idx ]->sizePolicy().hasHeightForWidth());
        arrowLabel[ idx ]->setSizePolicy(sizePolicy);
        arrowLabel[ idx ]->setMinimumSize(QSize(16, 16));
        arrowLabel[ idx ]->setMaximumSize(QSize(64, 64));
        arrowLabel[ idx ]->setAutoFillBackground(false);
        arrowLabel[ idx ]->setFrameShape(QFrame::NoFrame);
        arrowLabel[ idx ]->setFrameShadow(QFrame::Plain);
        arrowLabel[ idx ]->setTextFormat(Qt::AutoText);
        arrowLabel[ idx ]->setPixmap(QPixmap(QString::fromUtf8(":/img/right_64.png")));
        arrowLabel[ idx ]->setScaledContents(true);
        arrowLabel[ idx ]->setTextInteractionFlags(Qt::NoTextInteraction);
        vLayoutSymbol[ idx ]->addWidget(arrowLabel[ idx ]);
        verticalSpacer_3.append( new QSpacerItem(20, 40, QSizePolicy::Minimum,
                                                 QSizePolicy::Expanding) );
        vLayoutSymbol[ idx ]->addItem( verticalSpacer_3[ idx ] );
        vLayoutSymbol[ idx ]->setStretch(0, 2);
        vLayoutSymbol[ idx ]->setStretch(1, 1);
        vLayoutSymbol[ idx ]->setStretch(2, 2);
        hLayoutConf[ idx ]->addLayout( vLayoutSymbol[ idx ] );
        vGBoxOutput.append( new QGroupBox( kitTab[ idx ] ) );
        vGBoxOutput[ idx ]->setObjectName(QStringLiteral("vGBoxOutput"));
        vGBoxOutput[ idx ]->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);
        vGBoxOutput[ idx ]->setFlat(false);
        vLayoutOutput.append( new QVBoxLayout( vGBoxOutput[ idx ] ) );
        vLayoutOutput[ idx ]->setSpacing(6);
        vLayoutOutput[ idx ]->setContentsMargins(11, 11, 11, 11);
        vLayoutOutput[ idx ]->setObjectName(QStringLiteral("vLayoutOutput"));
        vLayoutOutput[ idx ]->setContentsMargins(3, 3, 3, 3);
        outputListView.append( new QListView( vGBoxOutput[ idx ] ) );
        outputListView[ idx ]->setObjectName(QStringLiteral("outputListView"));
        vLayoutOutput[ idx ]->addWidget(outputListView[ idx ]);
        hLayoutOutputSize.append( new QHBoxLayout( vGBoxOutput[ idx ] ) );
        hLayoutOutputSize[ idx ]->setSpacing(6);
        hLayoutOutputSize[ idx ]->setObjectName(QStringLiteral("hLayoutOutputSize"));
        hLayoutOutputSize[ idx ]->setContentsMargins(3, 3, 3, 3);
        outputLabel.append( new QLabel( vGBoxOutput[ idx ] ) );
        outputLabel[ idx ]->setObjectName(QStringLiteral("outputLabel"));
        outputLabel[ idx ]->setLayoutDirection(Qt::LeftToRight);
        outputLabel[ idx ]->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        hLayoutOutputSize[ idx ]->addWidget(outputLabel[ idx ]);
        outputSize.append( new QLabel( vGBoxOutput[ idx ] ) );
        outputSize[ idx ]->setObjectName(QStringLiteral("outputSize"));
        hLayoutOutputSize[ idx ]->addWidget(outputSize[ idx ]);
        hLayoutOutputSize[ idx ]->setStretch(0, 1);
        hLayoutOutputSize[ idx ]->setStretch(1, 2);
        vLayoutOutput[ idx ]->addLayout(hLayoutOutputSize[ idx ]);
        hLayoutConf[ idx ]->addWidget(vGBoxOutput[ idx ]);
        vLayoutButtons.append( new QVBoxLayout( kitTab[ idx ] ) );
        vLayoutButtons[ idx ]->setSpacing(6);
        vLayoutButtons[ idx ]->setObjectName(QStringLiteral("vLayoutButtons"));
        vLayoutButtons[ idx ]->setContentsMargins(3, 3, 3, 3);
        configurationButton.append( new QPushButton( kitTab[ idx ] ) );
        configurationButton[ idx ]->setObjectName(QStringLiteral("configurationButton"));
        QIcon icon9;
        icon9.addFile(QStringLiteral(":/ui/img/gear_64.png"), QSize(),
                      QIcon::Normal, QIcon::Off);
        configurationButton[ idx ]->setIcon(icon9);
        vLayoutButtons[ idx ]->addWidget(configurationButton[ idx ]);
        verticalSpacer.append( new QSpacerItem(20, 40, QSizePolicy::Minimum,
                                               QSizePolicy::Expanding) );
        vLayoutButtons[ idx ]->addItem(verticalSpacer[ idx ]);
        hLayoutConf[ idx ]->addLayout(vLayoutButtons[ idx ]);
        vLayoutTab[ idx ]->addLayout(hLayoutConf[ idx ]);

        progressBar.append( new QProgressBar( kitTab[ idx ] ) );
        progressBar[ idx ]->setObjectName(QStringLiteral("progressBar"));
        progressBar[ idx ]->setMaximum(120);
        progressBar[ idx ]->setValue(24);
        vLayoutTab[ idx ]->addWidget(progressBar[ idx ]);

        consoleTextEdit.append( new QPlainTextEdit( kitTab[ idx ] ) );
        consoleTextEdit[ idx ]->setObjectName(QStringLiteral("consoleTextEdit"));
        vLayoutTab[ idx ]->addWidget(consoleTextEdit[ idx ]);
        vLayoutTab[ idx ]->setStretch(2, 2);
        vLayoutTab[ idx ]->setStretch(4, 2);
        QIcon icon10;
        icon10.addFile(QStringLiteral(":/ui/img/briefcase_64.png"),
                       QSize(), QIcon::Normal, QIcon::Off);
        ui->vTabWidget->addTab( kitTab[ idx ], icon10, QString() );
    } catch(...) {   // setupUi
        ui->statusBar->setStatusTip( tr("Open tab error!") );
        delete kitTab[ idx ];
        delete verticalSpacer[ idx ];
        delete verticalSpacer_2[ idx ];
        delete verticalSpacer_3[ idx ];
    }

    try {       // retranslateUi
        nameKitLabel[ idx ]->setText(QApplication::translate("MainWindow", "Kit name :", 0));
        nameKitName[ idx ]->setText(QApplication::translate("MainWindow", "nameNameName", 0));
        serverLabel[ idx ]->setText(QApplication::translate("MainWindow", "Server :", 0));
        serverName[ idx ]->setText(QApplication::translate("MainWindow", "server.ru/server", 0));
        pathToMt4Label[ idx ]->setText(QApplication::translate("MainWindow", "Path to MT4 :", 0));
        pathToMt4Name[ idx ]->setText(QApplication::translate("MainWindow", "path:pathpath", 0));
        vGBoxInput[ idx ]->setTitle(QApplication::translate("MainWindow",
                                                            "Input neural network :", 0));
        inputLabel[ idx ]->setText(QApplication::translate("MainWindow", "History size :", 0));
        inputSize[ idx ]->setText(QString());
        arrowLabel[ idx ]->setText(QString());
        vGBoxOutput[ idx ]->setTitle(QApplication::translate("MainWindow",
                                                             "Output neural network :", 0));
        outputLabel[ idx ]->setText(QApplication::translate("MainWindow",
                                                            "Prediction size :", 0));
        outputSize[ idx ]->setText(QString());
        configurationButton[ idx ]->setText(QApplication::translate("MainWindow",
                                                                    "Configuration", 0));
        progressBar[ idx ]->setFormat(QApplication::translate("MainWindow", "Progress %p%", 0));
        ui->vTabWidget->setTabText(ui->vTabWidget->indexOf(kitTab[ idx ]),
                                   QApplication::translate("MainWindow", "sampleTabName", 0));
    } catch(...) {   // retranslateUi
        ui->statusBar->setStatusTip( tr("Trancelate error!") );
    }
}

void MainWindow::addTabConnections(qint32 idx)
{
    connect( configurationButton[ idx ], &QPushButton::clicked,
             this, &MainWindow::openKitConfig );
    connect( ui->vTabWidget, SIGNAL(tabCloseRequested(int)),
             this, SLOT(closeTab(qint32)) );
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

