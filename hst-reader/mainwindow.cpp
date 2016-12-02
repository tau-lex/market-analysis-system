#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "hstreader.h"
#include "csvreader.h"
//#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
    if( historyReader )
        delete historyReader;
}

void MainWindow::on_findFileButton_clicked()
{
    filePath = QFileDialog::getOpenFileName( this, tr("Open file:"), "D:\\Projects\\MQL5 History", tr("History file (*.hst *.csv)") );
    ui->filePathEdit->setText( filePath );
    ui->textBrowser->insertPlainText( filePath + "\n\n" );
    ui->textBrowser->setUpdatesEnabled(true);
}

void MainWindow::on_pushButton_clicked()
{
    if( filePath.contains(".hst") )
        readHistory( FileType::HST );
    else if( filePath.contains(".csv") )
        readHistory( FileType::CSV );
    else
        ui->textBrowser->insertPlainText("Sorry, file not found!\n\n");
}

void MainWindow::on_saveCsvButton_clicked()
{

    ui->textBrowser->insertPlainText("Done!\n");
}

void MainWindow::on_action_triggered()
{
    ui->textBrowser->clear();
}

void MainWindow::readHistory(FileType type)
{
    if( historyReader )
        delete historyReader;

    if( type == FileType::HST )
        historyReader = new HstReader( filePath );
    else
        historyReader = new CsvReader( filePath );

    historyReader->readFromFile();
    ui->textBrowser->insertPlainText( historyReader->getHeaderString() + "\n\n" );

    for(int i = 0; i < historyReader->getHistorySize(); i++)
    {
        ui->textBrowser->insertPlainText( historyReader->getHistoryString( i ) + "\n" );
    }

    QString tempMsg = QString( "\nMW: File readed. History size - %1\n" ).arg( historyReader->getHistorySize() );
    ui->textBrowser->insertPlainText( tempMsg );
}
