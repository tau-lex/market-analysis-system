#include "include/csvpredictionwriter.h"
#include <QFile>
#include <QDir>
#include <QTextStream>
#include <QString>
#include <QDateTime>

CsvPredictionWriter::CsvPredictionWriter(QObject *parent) : CsvWriter(parent),
                                                            header(nullptr),
                                                            dataPrediction(nullptr)
{}

CsvPredictionWriter::CsvPredictionWriter(QString fName) : CsvWriter(fName),
                                                          header(nullptr),
                                                          dataPrediction(nullptr)
{}

CsvPredictionWriter::~CsvPredictionWriter()
{
    if( header )
        delete header;
    if( dataPrediction ) {
        for( qint32 i = 0; i < dataPrediction->size(); i++ )
            delete (*dataPrediction)[i];
        delete dataPrediction;
    }
}

PHeader *CsvPredictionWriter::getHeader()
{
    if( header == nullptr )
        header = new PHeader;
    return header;
}

QList<Forecast *> *CsvPredictionWriter::getDataPredictionPtr()
{
    if( dataPrediction == nullptr )
        dataPrediction = new QList<Forecast *>;
    return dataPrediction;
}

void CsvPredictionWriter::writeFile(void)
{
    if( fileName == "" )
        return;
    if( !fileName.contains(".csv") )
        fileName += ".csv";
    QFile file( fileName, this );
    if( file.open(QIODevice::WriteOnly) ) {
        QTextStream output( &file );
        // Write header
        QString headerStr = QString("%1;%2;%3;%4;%5;%6;%7;%8\n")
                .arg( header->Version )
                .arg( header->Copyright )
                .arg( header->Symbol )
                .arg( header->Period )
                .arg( header->Digits )
                .arg( QDateTime::fromTime_t( header->TimeSign )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( QDateTime::fromTime_t( header->LastSync )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( header->Depth );
        output << headerStr;
        // Write prediction
        QString buffer;
        for( qint32 idx = 0; idx < dataPrediction->size(); idx++ ) {
            buffer = QDateTime::fromTime_t( (*dataPrediction)[idx]->Time )
                     .toString("yyyy.MM.dd hh:mm:ss");
            for( qint32 j = 0; j < header->Depth; j++ ) {
                buffer += ';';
                buffer += QString::number( (*dataPrediction)[idx]->High[j],
                                           'f', header->Digits );
            }
            buffer += '\n';
            output << buffer;
            buffer = QDateTime::fromTime_t( (*dataPrediction)[idx]->Time )
                     .toString("yyyy.MM.dd hh:mm:ss");
            for( qint32 j = 0; j < header->Depth; j++ ) {
                buffer += ';';
                buffer += QString::number( (*dataPrediction)[idx]->Low[j],
                                           'f', header->Digits );
            }
            buffer += '\n';
            output << buffer;
            buffer = QDateTime::fromTime_t( (*dataPrediction)[idx]->Time )
                     .toString("yyyy.MM.dd hh:mm:ss");
            for( qint32 j = 0; j < header->Depth; j++ ) {
                buffer += ';';
                buffer += QString::number( (*dataPrediction)[idx]->Close[j],
                                           'f', header->Digits );
            }
            buffer += '\n';
            output << buffer;
        }
        file.close();
    }
}

void CsvPredictionWriter::writeFile(const QString fName)
{
    setFileName( fName );
    CsvPredictionWriter::writeFile();
}
