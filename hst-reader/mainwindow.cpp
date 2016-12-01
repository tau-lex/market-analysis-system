#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
    //if(historyReader != NULL)
    //    delete historyReader;
}

void MainWindow::on_findFileButton_clicked()
{
    filePath = QFileDialog::getOpenFileName( this, tr("Open file:"), "D:\\Projects\\MQL5 History", tr("History file (*.hst *.csv)") );
    ui->filePathEdit->setText( filePath );
    ui->textBrowser->insertPlainText( filePath + "\n\n" );
}

void MainWindow::on_pushButton_clicked()
{
    if( filePath.contains(".hst") )
        readHistory();
    else if( filePath.contains(".csv") )
        readNewHistory();
    else
        ui->textBrowser->insertPlainText("Sorry, file not found!\n\n");
}

void MainWindow::on_action_triggered()
{
    ui->textBrowser->clear();
}

void MainWindow::readHistory()
{
    historyReader = new HstReader( filePath );
    historyReader->readFromFile();
    ui->textBrowser->insertPlainText( historyReader->getHeaderString() + "\n\n" );

    for(int i = 0; i < historyReader->getHistorySize(); i++)
    {
        ui->textBrowser->insertPlainText( historyReader->getHistoryString( i ) + "\n" );
    }

    QString tempMsg = QString( "\nMW: File readed. History size - %1\n" ).arg( historyReader->getHistorySize() );
    ui->textBrowser->insertPlainText( tempMsg );
    //qDebug() << tempMsg;

    delete historyReader;
}

void MainWindow::readNewHistory()
{
    historyCReader = new CsvReader( filePath );
    historyCReader->readFromFile();
    ui->textBrowser->insertPlainText( historyCReader->getHeaderString() + "\n\n" );

    for(int i = 0; i < historyCReader->getHistorySize(); i++)
    {
        ui->textBrowser->insertPlainText( historyCReader->getHistoryString( i ) + "\n" );
    }

    QString tempMsg = QString( "\nMW: File readed. History size - %1\n" ).arg( historyCReader->getHistorySize() );
    ui->textBrowser->insertPlainText( tempMsg );
    //qDebug() << tempMsg;

    delete historyCReader;
}
