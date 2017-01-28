#include "include/csvwriter.h"
#include <QFile>
#include <QTextStream>
#include <QString>
#include <QDateTime>

CsvWriter::CsvWriter(QObject *parent) : QObject(parent),
                                        fileName(""),
                                        data(nullptr)
{}

CsvWriter::CsvWriter(QString fName) : fileName(fName),
                                      data(nullptr)
{}

CsvWriter::~CsvWriter()
{
    if( data )
        delete data;
}

void CsvWriter::setFileName(const QString fName)
{
    fileName = fName;
}

QString CsvWriter::getFileName() const
{
    return fileName;
}

qint32 CsvWriter::getSize() const
{
    return data->size();
}

void CsvWriter::setZeroColumnIsTime(const bool isTime)
{
    zeroColumnIsTime = isTime;
}

bool CsvWriter::getZeroColumnIsTime() const
{
    return zeroColumnIsTime;
}

void CsvWriter::setPrecision(const qint32 prec)
{
    precision = prec;
}

qint32 CsvWriter::getPrecision() const
{
    return precision;
}

QList<std::vector<double> > *CsvWriter::getDataPtr(void)
{
    if( data == nullptr )
        data = new QList<std::vector<double> >;
    return data;
}

void CsvWriter::writeFile(void)
{
    if( fileName == "" )
        return;
    if( !fileName.contains(".csv") )
        fileName += ".csv";
    QFile file(fileName, this);
    if( file.open(QIODevice::WriteOnly) ) {
        QTextStream output( &file );
        QString buffer = "";
        for( qint32 idx = 0; idx < data->size(); idx++ ) {
            if( zeroColumnIsTime )
                buffer = QDateTime::fromTime_t( static_cast<qint32>((*data)[idx][0]) )
                         .toString("yyyy.MM.dd hh:mm:ss");
            else
                buffer = QString("%1").arg( static_cast<qint32>((*data)[idx][0]) );
            buffer += QString(",%1").arg( (*data)[idx][1], 0, 'f', precision );
            buffer += QString(",%1").arg( (*data)[idx][2], 0, 'f', precision );
            buffer += QString(",%1").arg( (*data)[idx][3], 0, 'f', precision );
            buffer += QString(",%1").arg( (*data)[idx][4], 0, 'f', precision );
            buffer += QString(",%1\n").arg( static_cast<qint32>((*data)[idx][5]) );
            output << buffer;
        }
        file.close();
    }
}

void CsvWriter::writeFile(const QString fName)
{
    fileName = fName;
    writeFile();
}
