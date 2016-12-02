#include "hstreader.h"
#include <QFile>
#include <QString>
#include <QDataStream>

//+---------------------------------------------------------------------------+
QDataStream& operator>>( QDataStream &out, Header &header )
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
    out.skipRawData(13 * 4);        // HeaderBytes.Unused

    return out;
}
QDataStream& operator>>( QDataStream &out, History &history )
{
    out.setFloatingPointPrecision( QDataStream::DoublePrecision );

    out >> history.Time;
    out >> history.Open;
    out >> history.High;
    out >> history.Low;
    out >> history.Close;
    out >> history.Volume;
    //out >> history.Spread;
    //out >> history.RealVolume;
    out.skipRawData(12);        // Skip 12 bytes struct History

    return out;
}
QDataStream& operator>>( QDataStream &out, History400 &history )
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
HstReader::HstReader(QString fName) : IMt4Reader(fName)
{ }

bool HstReader::readFromFile()
{
    QFile file(fileName, this);

    if( file.open(QIODevice::ReadOnly) )
    {
        fileExists = true;

        QDataStream input(&file);
        input.setByteOrder(QDataStream::LittleEndian);

        input >> *header;
        historyVersion = header->Version;

        while( !file.atEnd() )
        {
            if( historyVersion == 401 )
            {
                History *historyLine = new History;
                input >> *historyLine;
                historyVector->push_back( historyLine );
            }
            else if( historyVersion == 400 )
            {
                History400 *historyLine = new History400;
                input >> *historyLine;
                historyVector400->push_back( historyLine );
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
