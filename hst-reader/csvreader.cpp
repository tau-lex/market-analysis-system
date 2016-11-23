#include "csvreader.h"
#include <QFile>
#include <QDateTime>
#include <QString>
#include <QTextStream>
#include <QDebug>

//+---------------------------------------------------------------------------+
QTextStream& operator>>( QTextStream &out, Header &header )
{
    QString buffer = out.readLine();

    header.Version = buffer.section( ',', 0, 0 ).toInt();
    header.Copyright = buffer.section( ',', 1, 1 ).toUtf8();
    header.Symbol = buffer.section( ',', 2, 2 ).toUtf8();
    header.Period = buffer.section( ',', 3, 3 ).toInt();
    header.Digits = buffer.section( ',', 4, 4 ).toInt();
    header.TimeSign = buffer.section( ',', 5, 5 ).toInt();
    header.LastSync = buffer.section( ',', 6, 6 ).toInt();

    return out;
}
QTextStream& operator>>( QTextStream &out, History &history )
{
    QString buffer = out.readLine();

    history.Time = buffer.section( ',', 0, 0 ).toInt();
    history.Open = buffer.section( ',', 1, 1 ).toDouble();
    history.High = buffer.section( ',', 2, 2 ).toDouble();
    history.Low = buffer.section( ',', 3, 3 ).toDouble();
    history.Close = buffer.section( ',', 4, 4 ).toDouble();
    history.Volume = buffer.section( ',', 5, 5 ).toInt();

    return out;
}

//+---------------------------------------------------------------------------+
CsvReader::CsvReader(QObject *parent) : QObject(parent), historySize(0)
{ }

CsvReader::CsvReader(QString fName) : historySize(0), fileName(fName)
{ }

CsvReader::~CsvReader()
{
    if( !historyVector.empty() )
        for(uint i = 0; i < historySize; i++)
            delete historyVector[i];
}

void CsvReader::setFileName(QString fName)
{
    fileName = fName;
}

QString CsvReader::getFileName() const
{
    return fileName;
}

uint CsvReader::getHistorySize() const
{
    return historySize;
}

bool CsvReader::readFromFile()
{
    QFile file(fileName, this);

    if(file.open(QIODevice::ReadOnly))
    {
        fileExists = true;

        QTextStream input( &file );
        input.setAutoDetectUnicode( true );

        input >> header;

        while ( !file.atEnd() )
        {
            History *historyLine = new HistoryBytes;
            input >> *historyLine;
            historyVector.push_back(historyLine);
            historySize++;
        }
        file.close();
        return fileExists;
    }
    else
    {
        fileExists = false;
        return fileExists;
    }
}

Header *CsvReader::getHeaderStruct()
{
    return &header;
}

QString CsvReader::getHeaderString() const
{
    if(fileExists)
        return QString("%1, %2, %3, %4, %5, %6, %7")
                .arg( header.Version )
                .arg( QString(header.Copyright) )
                .arg( QString(header.Symbol) )
                .arg( header.Period )
                .arg( header.Digits )
                .arg( QDateTime::fromTime_t( header.TimeSign )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( QDateTime::fromTime_t( header.LastSync )
                      .toString("yyyy.MM.dd hh:mm:ss") );
    return "File not exists.";
}

std::vector<History*> *CsvReader::getHistoryVector()
{
    return &historyVector;
}

QString CsvReader::getHistoryString(uint numberPosition) const
{
    if(fileExists)
        return QString("%1, %2, %3, %4, %5, %6")
                .arg( QDateTime::fromTime_t( historyVector[numberPosition]->Time )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( historyVector[numberPosition]->Open  /*, header.Digits, 'f'*/ )
                .arg( historyVector[numberPosition]->High  /*, header.Digits, 'f'*/ )
                .arg( historyVector[numberPosition]->Low   /*, header.Digits, 'f'*/ )
                .arg( historyVector[numberPosition]->Close /*, header.Digits, 'f'*/ )
                .arg( historyVector[numberPosition]->Volume );
    return "File not exists.";
}
