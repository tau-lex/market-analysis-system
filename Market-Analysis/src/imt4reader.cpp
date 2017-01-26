#include "include/imt4reader.h"
#include <QDateTime>
#include <QString>
#include <QList>

IMt4Reader::IMt4Reader(QObject *parent) : QObject(parent),
                                            fileName("")
{
    header = new Header;
    history = new QList<std::vector<double> >;
}

IMt4Reader::IMt4Reader(QString fName) : fileName(fName)
{
    header = new Header;
    history = new QList<std::vector<double> >;
}

IMt4Reader::~IMt4Reader()
{
    if( header )
        delete header;
    if( history )
        delete history;
}

void IMt4Reader::setFileName(const QString fName)
{
    fileName = fName;
}

QString IMt4Reader::getFileName() const
{
    return fileName;
}

size_t IMt4Reader::getHistorySize() const
{
    return history->size();
}

qint32 IMt4Reader::getHistoryVersion() const
{
    return header->Version;
}

Header *IMt4Reader::getHeader() const
{
    return header;
}

QString IMt4Reader::getHeaderString() const
{
    if( fileExists )
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

QList<std::vector<double> > *IMt4Reader::getHistory() const
{
    return history;
}

std::vector<double> IMt4Reader::getHistory(qint32 position) const
{
    return history->at( position );
}

QString IMt4Reader::getHistoryString(qint32 position) const
{
    if( fileExists ) {
        if( position >= history->size() )
            return "Position not valid.";
        std::vector<double> row = history->at( position );
        QString out = QString("%1, %2, %3, %4, %5, %6")
                .arg( QDateTime::fromTime_t( static_cast<qint64>(row[0]) )
                            .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( row[1], 0, 'f', header->Digits )
                .arg( row[2], 0, 'f', header->Digits )
                .arg( row[3], 0, 'f', header->Digits )
                .arg( row[4], 0, 'f', header->Digits )
                .arg( row[5], 0, 'f', 0 );
        return out;
    }
    return "File not exists.";
}
