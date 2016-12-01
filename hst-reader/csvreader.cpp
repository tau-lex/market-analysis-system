#include "csvreader.h"
#include <QFile>
#include <QDateTime>
#include <QString>
#include <QByteArray>
//#include <QTextStream>

//+---------------------------------------------------------------------------+
/*
QTextStream& operator>>( QTextStream &out, Header &header )
{
    QString buffer = out.readLine();
    qDebug() << buffer;
    header.Version = buffer.section( ';', 0, 0 ).toInt();
    for(int i = 0; i < buffer.section( ';', 1, 1 ).size(); i++)
        header.Copyright[i] = (QChar)buffer.section( ';', 1, 1 )[i];
    for(int i = 0; i < buffer.section( ';', 2, 2 ).size(); i++)
        header.Symbol[i] = (QChar)buffer.section( ';', 2, 2 )[i];
    header.Period = buffer.section( ';', 3, 3 ).toInt();
    header.Digits = buffer.section( ';', 4, 4 ).toInt();
    header.TimeSign = QDateTime::fromString( buffer.section( ';', 5, 5 ), "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;
    header.LastSync = QDateTime::fromString( buffer.section( ';', 6, 6 ), "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;

    return out;
}
QTextStream& operator>>( QTextStream &out, History &history )
{
    QString buffer = out.readLine();
    qDebug() << buffer;
    history.Time = QDateTime::fromString( buffer.section( ';', 0, 0 ), "yyyy.MM.dd hh:mm:ss" ).toMSecsSinceEpoch()/1000;
    history.Open =  buffer.section( ';', 1, 1 ).toDouble();
    history.High =  buffer.section( ';', 2, 2 ).toDouble();
    history.Low =   buffer.section( ';', 3, 3 ).toDouble();
    history.Close = buffer.section( ';', 4, 4 ).toDouble();
    history.Volume = buffer.section( ';', 5, 5 ).toInt();

    return out;
} */

//+---------------------------------------------------------------------------+
CsvReader::CsvReader(QObject *parent) : QObject(parent), historySize(0)
{
    header = new Header;
    historyVector = new std::vector<History*>;
}

CsvReader::CsvReader(QString fName) : fileName(fName), historySize(0)
{
    header = new Header;
    historyVector = new std::vector<History*>;
}

CsvReader::~CsvReader()
{
    if( header != nullptr )
        delete header;
    if( (historyVector != nullptr) && !historyVector->empty() )
    {
        for(int i = 0; i < historySize; i++)
            delete (*historyVector)[i];
        delete historyVector;
    }
}

Header *CsvReader::readHeader(QFile &f)
{
    QByteArray byteArr = f.readLine();
    QString buffer = byteArr.data();
    if( buffer == "")
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
    if( buffer == "")
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

void CsvReader::setFileName(QString fName)
{
    fileName = fName;
}

QString CsvReader::getFileName() const
{
    return fileName;
}

int CsvReader::getHistorySize() const
{
    return historySize;
}

int CsvReader::getHistoryVersion() const
{
    return historyVersion;
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
        /*
        QTextStream input( &file );
        input.setAutoDetectUnicode( true );
        input >> header;
        historyVersion = header->Version;
        while( !file.atEnd() )
        {
            History *historyLine = new History;
            input >> *historyLine;
            historyVector->push_back(historyLine);
            historySize++;
        } */
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
    return header;
}

QString CsvReader::getHeaderString() const
{
    if(fileExists)
        return QString("%1, %2, %3, %4, %5, %6, %7")
                .arg( header->Version )
                .arg( QString(header->Copyright) )
                .arg( QString(header->Symbol) )
                .arg( header->Period )
                .arg( header->Digits )
                .arg( QDateTime::fromTime_t( header->TimeSign )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( QDateTime::fromTime_t( header->LastSync )
                      .toString("yyyy.MM.dd hh:mm:ss") );
    return "File not exists.";
}

std::vector<History*> *CsvReader::getHistoryVector()
{
    return historyVector;
}

QString CsvReader::getHistoryString(int numberPosition) const
{
    if( fileExists )
        return QString("%1, %2, %3, %4, %5, %6")
                .arg( QDateTime::fromTime_t( (*historyVector)[numberPosition]->Time )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( (*historyVector)[numberPosition]->Open  , header->Digits, 'f' )
                .arg( (*historyVector)[numberPosition]->High  , header->Digits, 'f' )
                .arg( (*historyVector)[numberPosition]->Low   , header->Digits, 'f' )
                .arg( (*historyVector)[numberPosition]->Close , header->Digits, 'f' )
                .arg( (*historyVector)[numberPosition]->Volume );
    return "File not exists.";
}
