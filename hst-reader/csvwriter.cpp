#include "csvwriter.h"
#include <QFile>
#include <QTextStream>
#include <QString>
#include <QDateTime>

CsvWriter::CsvWriter(QObject *parent) : QObject(parent),
                                        fileName(""),
                                        forecastSize(0)
{
    header = new HeaderWr;
    forecastVector = new std::vector<Forecast *>;
}

CsvWriter::CsvWriter(QString fName) : fileName(fName),
                                        forecastSize(0)
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

qint32 CsvWriter::getDepth() const
{
    return header->Depth;
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
        // Write header
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
        // Write prediction
        QString buffer;
        for( qint32 i = 0; i < forecastSize; i++ )
        {
            {
                buffer = QDateTime::fromTime_t( (*forecastVector)[i]->Time ).toString("yyyy.MM.dd hh:mm:ss");
                for( qint32 j = 0; j < header->Depth; j++ )
                {
                    buffer += ';';
                    buffer += QString::number( (*forecastVector)[i]->High[j], 'f', header->Digits );
                }
                buffer += '\n';
                output << buffer;
            }
            {
                buffer = QDateTime::fromTime_t( (*forecastVector)[i]->Time ).toString("yyyy.MM.dd hh:mm:ss");
                for( qint32 j = 0; j < header->Depth; j++ )
                {
                    buffer += ';';
                    buffer += QString::number( (*forecastVector)[i]->Low[j], 'f', header->Digits );
                }
                buffer += '\n';
                output << buffer;
            }
            {
                buffer = QDateTime::fromTime_t( (*forecastVector)[i]->Time ).toString("yyyy.MM.dd hh:mm:ss");
                for( qint32 j = 0; j < header->Depth; j++ )
                {
                    buffer += ';';
                    buffer += QString::number( (*forecastVector)[i]->Close[j], 'f', header->Digits );
                }
                buffer += '\n';
                output << buffer;
            }
        }
        file.close();
    }
}

void CsvWriter::writeFile(QString fName)
{
    fileName = fName;
    writeFile();
}
