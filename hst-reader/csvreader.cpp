#include "csvreader.h"
#include <QDateTime>
#include <QString>
#include <QByteArray>

//+---------------------------------------------------------------------------+
CsvReader::CsvReader(QString fName) : IMt4Reader(fName)
{ }

Header *CsvReader::readHeader(QFile &f)
{
    QByteArray byteArr = f.readLine();
    QString buffer = byteArr.data();
    if( buffer == "" )
        return nullptr;

    Header *header = new Header;
    header->Version = buffer.section( ';', 0, 0 ).toInt();
    for(int i = 0; i < buffer.section( ';', 1, 1 ).size(); i++)
        header->Copyright[i] = (QChar)buffer.section( ';', 1, 1 )[i];
    for(int i = 0; i < buffer.section( ';', 2, 2 ).size(); i++)
        header->Symbol[i] = (QChar)buffer.section( ';', 2, 2 )[i];
    header->Period = buffer.section( ';', 3, 3 ).toInt();
    header->Digits = buffer.section( ';', 4, 4 ).toInt();
    header->TimeSign = QDateTime::fromString( buffer.section( ';', 5, 5 ), "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;
    header->LastSync = QDateTime::fromString( buffer.section( ';', 6, 6 ), "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;

    return header;
}

History *CsvReader::readHistory(QFile &f)
{
    QByteArray byteArr = f.readLine();
    QString buffer = byteArr.data();
    if( buffer == "" )
        return nullptr;

    History *history = new History;
    history->Time = QDateTime::fromString( buffer.section( ';', 0, 0 ), "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;
    history->Open =  buffer.section( ';', 1, 1 ).toDouble();
    history->High =  buffer.section( ';', 2, 2 ).toDouble();
    history->Low =   buffer.section( ';', 3, 3 ).toDouble();
    history->Close = buffer.section( ';', 4, 4 ).toDouble();
    history->Volume = buffer.section( ';', 5, 5 ).toInt();

    return history;
}

bool CsvReader::readFromFile()
{
    QFile file(fileName, this);

    if(file.open(QIODevice::ReadOnly))
    {
        fileExists = true;

        header = readHeader( file );
        historyVersion = header->Version;

        History *historyLine = readHistory( file );
        while( historyLine != nullptr )
        {
            historyVector->push_back( historyLine );
            historySize++;
            historyLine = readHistory( file );
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
