#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QLineEdit>
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
    if( forecastWriter )
        delete forecastWriter;
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
    if( forecastWriter )
        delete forecastWriter;
    if( !historyReader )
        ui->textBrowser->insertPlainText("Not find open file.\n");

    QString outFile = "D:\\Projects\\MQL5 History\\csvWriter";
    outFile = QString("%1-%2%3.csv").arg( outFile )
                                .arg( QString(historyReader->getHeader()->Symbol) )
                                .arg( historyReader->getHeader()->Period );
    forecastWriter = new CsvWriter( outFile );

    HeaderWr *header = forecastWriter->getHeader();
    header->Symbol = QString(historyReader->getHeader()->Symbol);
    header->Period = historyReader->getHeader()->Period;
    header->Digits = historyReader->getHeader()->Digits;
    header->Depth = 1;

    std::vector<Forecast*> *forecast = forecastWriter->getForecastVector();
    for( qint32 i = 0; i < historyReader->getHistorySize(); i++ )
    {
        Forecast *newFLine = new Forecast;
        newFLine->Time =     ( *historyReader->getHistoryVector() )[i]->Time;
        newFLine->High[0] =  ( *historyReader->getHistoryVector() )[i]->High;
        newFLine->Low[0] =   ( *historyReader->getHistoryVector() )[i]->Low;
        newFLine->Close[0] = ( *historyReader->getHistoryVector() )[i]->Close;

        forecast->push_back( newFLine );
        forecastWriter->setSize(i);
    }

    forecastWriter->writeFile();

    ui->textBrowser->insertPlainText("Save csv file - Done!\n");
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
