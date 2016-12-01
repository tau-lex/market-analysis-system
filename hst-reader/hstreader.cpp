#include "hstreader.h"
#include <QFile>
#include <QDateTime>
#include <QString>
#include <QDataStream>
#include <QDebug>

//+---------------------------------------------------------------------------+
QDataStream& operator>>( QDataStream &out, HeaderBytes &header )
{
    char buffer64[64];

    out >> header.Version;
    out.readRawData(buffer64, 64);
    for(int i = 0; i < 64; i++) header.Copyright[i] = (QChar)buffer64[i];
    out.readRawData(buffer64, 12);
    for(int i = 0; i < 12; i++) header.Symbol[i] = (QChar)buffer64[i];
    out >> header.Period;
    out >> header.Digits;
    out >> header.TimeSign;
    out >> header.LastSync;
    //out.readRawData(buffer64, 52);
    //for(int i = 0; i < 52; i++) header.Unused[i] = (QChar)buffer64[i];
    out.skipRawData(13 * 4);        // HeaderBytes.Unused

    return out;
}
QDataStream& operator>>( QDataStream &out, HistoryBytes &history )
{
    out.setFloatingPointPrecision( QDataStream::DoublePrecision );

    out >> history.Time;
    //out.skipRawData(4);             // Skip 4 bite for int32 Time
    out >> history.Open;
    out >> history.High;
    out >> history.Low;
    out >> history.Close;
    out >> history.Volume;
    out >> history.Spread;
    out >> history.RealVolume;

    return out;
}
QDataStream& operator>>( QDataStream &out, HistoryBytes400 &history )
{
    out.setFloatingPointPrecision( QDataStream::DoublePrecision );

    out >> history.Time;
    out >> history.Open;
    out >> history.Low;
    out >> history.High;
    out >> history.Close;
    out >> history.Volume;

    return out;
}

//+---------------------------------------------------------------------------+
HstReader::HstReader(QObject *parent) : QObject(parent), historySize(0)
{ }

HstReader::HstReader(QString fName) : fileName(fName), historySize(0)
{ }

HstReader::~HstReader()
{
    if( !historyVector.empty() )
        for(int i = 0; i < historySize; i++)
            delete historyVector[i];
    if( !historyVector400.empty() )
        for(int i = 0; i < historySize; i++)
            delete historyVector400[i];
}

void HstReader::setFileName(QString fName)
{
    fileName = fName;
}

QString HstReader::getFileName() const
{
    return fileName;
}

int HstReader::getHistorySize() const
{
    return historySize;
}

int HstReader::getHistoryVersion() const
{
    return historyVersion;
}

bool HstReader::readFromFile()
{
    QFile file(fileName, this);

    if(file.open(QIODevice::ReadOnly))
    {
        fileExists = true;

        QDataStream input(&file);
        input.setByteOrder(QDataStream::LittleEndian);

        input >> header;
        historyVersion = header.Version;

        //input.setByteOrder(QDataStream::BigEndian);
        while (!file.atEnd())
        {
            if( historyVersion == 401 )
            {
                HistoryBytes *historyLine = new HistoryBytes;
                input >> *historyLine;
                historyVector.push_back(historyLine);
            }
            else if( historyVersion == 400 )
            {
                HistoryBytes400 *historyLine = new HistoryBytes400;
                input >> *historyLine;
                historyVector400.push_back(historyLine);
            }
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

HeaderBytes *HstReader::getHeaderStruct()
{
    return &header;
}

QString HstReader::getHeaderString() const
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
                //.arg( QString(header.Unused) );
    return "File not exists.";
}

std::vector<HistoryBytes*> *HstReader::getHistoryVector()
{
    return &historyVector;
}

QString HstReader::getHistoryString(int numberPosition) const
{
    if(fileExists)
        return QString("%1, %2, %3, %4, %5, %6")
                .arg( QDateTime::fromTime_t( historyVector[numberPosition]->Time )
                      .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( historyVector[numberPosition]->Open , header.Digits, 'f' )
                .arg( historyVector[numberPosition]->High , header.Digits, 'f' )
                .arg( historyVector[numberPosition]->Low  , header.Digits, 'f' )
                .arg( historyVector[numberPosition]->Close, header.Digits, 'f' )
                .arg( historyVector[numberPosition]->Volume );
                //.arg( historyVector[numberPosition]->Spread )
                //.arg( historyVector[numberPosition]->RealVolume );
    return "File not exists.";
}
