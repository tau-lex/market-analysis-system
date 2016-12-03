#include "csvwriter.h"
#include <QFile>
#include <QTextStream>
#include <QDateTime>
#include <QDebug>

CsvWriter::CsvWriter(QObject *parent) : QObject(parent),
                                        fileName(""),
                                        forecastSize(0),
                                        forecastDepth(0)
{
    header = new HeaderWr;
    forecastVector = new std::vector<Forecast *>;
}

CsvWriter::CsvWriter(QString fName) : fileName(fName),
                                        forecastSize(0),
                                        forecastDepth(0)
{
    header = new HeaderWr;
    forecastVector = new std::vector<Forecast *>;
}

CsvWriter::~CsvWriter()
{
    if( header )
        delete header;
    if( forecastVector )
    {
        for( qint32 i = 0; i < forecastSize; i++ )
            delete (*forecastVector)[i];
        delete forecastVector;
    }
}

void CsvWriter::setFileName(QString fName)
{
    fileName = fName;
}

QString CsvWriter::getFileName() const
{
    return fileName;
}

void CsvWriter::setSize(qint32 size)
{
    forecastSize = size;
}

qint32 CsvWriter::getSize() const
{
    return forecastSize;
}

void CsvWriter::setDepth(qint32 depth)
{
    forecastDepth = depth;
}

qint32 CsvWriter::getDepth() const
{
    return forecastDepth;
}

HeaderWr *CsvWriter::getHeader()
{
    return header;
}

std::vector<Forecast *> *CsvWriter::getForecastVector()
{
    return forecastVector;
}

void CsvWriter::writeFile()
{
    QFile file(fileName, this);

    if( file.open(QIODevice::WriteOnly) )
    {
        QTextStream output(&file);

        QString headerStr = QString("%1;%2;%3;%4;%5;%6;%7;%8\n").arg( header->Version )
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

        QString buffer;
        for( qint32 i = 0; i < forecastSize; i++ )
        {
            buffer = QString("%1;%2\n").arg( QDateTime::fromTime_t( (*forecastVector)[i]->Time )
                                                .toString("yyyy.MM.dd hh:mm:ss") )
                                        .arg( (*forecastVector)[i]->High[0] );
            output << buffer;
            buffer = QString("%1;%2\n").arg( QDateTime::fromTime_t( (*forecastVector)[i]->Time )
                                                .toString("yyyy.MM.dd hh:mm:ss") )
                                        .arg( (*forecastVector)[i]->Low[0] );
            output << buffer;
            buffer = QString("%1;%2\n").arg( QDateTime::fromTime_t( (*forecastVector)[i]->Time )
                                                .toString("yyyy.MM.dd hh:mm:ss") )
                                        .arg( (*forecastVector)[i]->Close[0] );
            output << buffer;
        }
        file.close();
    }
    else
    {
        qDebug() << "File not open.";
    }
}

void CsvWriter::writeFile(QString fName)
{
    fileName = fName;
    writeFile();
}
