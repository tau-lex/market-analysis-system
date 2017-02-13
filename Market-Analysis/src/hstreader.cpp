#include "include/hstreader.h"
#include <QFile>
#include <QString>
#include <QDataStream>

//+---------------------------------------------------------------------------+
QDataStream& operator>>( QDataStream &out, Header &header )
{
    char buffer64[64];
    out >> header.Version;
    out.readRawData( buffer64, 64 );
    for(int i = 0; i < 64; i++)
        header.Copyright[i] = (QChar)buffer64[i];
    out.readRawData( buffer64, 12 );
    for(int i = 0; i < 12; i++)
        header.Symbol[i] = (QChar)buffer64[i];
    out >> header.Period;
    out >> header.Digits;
    out >> header.TimeSign;
    out >> header.LastSync;
    out.skipRawData( 13 * 4 );      // HeaderBytes.Unused
    return out;
}
QDataStream& operator>>( QDataStream &out, History &history )
{
    out >> history.Time;
    out >> history.Open;
    out >> history.High;
    out >> history.Low;
    out >> history.Close;
    out >> history.Volume;
    out.skipRawData(12);
    //out >> history.Spread;
    //out >> history.RealVolume;
    return out;
}
QDataStream& operator>>( QDataStream &out, History400 &history )
{
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

bool HstReader::readFile()
{
    QFile file( fileName, this );
    if( file.open(QIODevice::ReadOnly) ) {
        fileExists = true;
        QDataStream input( &file );
        input.setByteOrder( QDataStream::LittleEndian );
        input.setFloatingPointPrecision( QDataStream::DoublePrecision );
        input >> *header;
        bool h401 = header->Version == 401;
        quint32 i32; qint64 i64; double dbl;
        while( !file.atEnd() ) {
            std::vector<double> newRow;
            if( h401 ) {            // time
                input >> i64;
                newRow.push_back( static_cast<double>(i64) );
            } else {
                input >> i32;
                newRow.push_back( static_cast<double>(i32) );
            }
            input >> dbl;           // open
            newRow.push_back( dbl );
            input >> dbl;           // high
            newRow.push_back( dbl );
            input >> dbl;           // low
            newRow.push_back( dbl );
            input >> dbl;           // close
            newRow.push_back( dbl );
            if( h401 ) {            // volume
                input >> i64;
                newRow.push_back( static_cast<double>(i64) );
            } else {
                input >> dbl;
                newRow.push_back( dbl );
            }
            if( h401 )                      // spread + realVolume
                input.skipRawData( 12 );
            history->append( newRow );
        }
        file.close();
        return fileExists;
    } else {
        fileExists = false;
        return fileExists;
    }
}
