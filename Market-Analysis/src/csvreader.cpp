#include "include/csvreader.h"
#include <QDateTime>
#include <QString>
#include <QByteArray>
#include <QList>

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
    header->TimeSign =
            QDateTime::fromString( buffer.section( ';', 5, 5 ),
                                   "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;
    header->LastSync =
            QDateTime::fromString( buffer.section( ';', 6, 6 ),
                                   "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;
    return header;
}

std::vector<double> CsvReader::readHistoryLine(QFile &f)
{
    QString buffer = f.readLine().data();
    std::vector<double> newRow;
    if( buffer == "" )
        return newRow;
    double time = static_cast<double>( QDateTime::fromString( buffer.section( ';', 0, 0 ),
                                         "yyyy.MM.dd hh:mm:ss" ).toTime_t() );
    newRow.push_back( time );
    newRow.push_back( buffer.section( ';', 1, 1 ).toDouble() );
    newRow.push_back( buffer.section( ';', 2, 2 ).toDouble() );
    newRow.push_back( buffer.section( ';', 3, 3 ).toDouble() );
    newRow.push_back( buffer.section( ';', 4, 4 ).toDouble() );
    if( header->Version == 401 ) {
        qint64 volume = buffer.section( ';', 5, 5 ).toInt();
        newRow.push_back( static_cast<double>( volume ) );
    }
    else if( header->Version == 400 ) {
        newRow.push_back( buffer.section( ';', 5, 5 ).toDouble() );
    }
    return newRow;
}

bool CsvReader::readFile()
{
    QFile file(fileName, this);
    if(file.open(QIODevice::ReadOnly)) {
        fileExists = true;
        header = readHeader( file );
        std::vector<double> newRow = readHistoryLine( file );
        while( newRow.size() != 0 ) {
            history->append( newRow );
            newRow = readHistoryLine( file );
        }
        file.close();
        return fileExists;
    } else {
        fileExists = false;
        return fileExists;
    }
}
