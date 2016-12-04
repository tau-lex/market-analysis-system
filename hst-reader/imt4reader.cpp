#include "imt4reader.h"
#include <QDateTime>
#include <QString>

/*IMt4Reader::IMt4Reader(QObject *parent) : QObject(parent)
{
    header = new Header;
    historyVector = new std::vector<History*>;
}*/

IMt4Reader::IMt4Reader(QObject *parent) : QObject(parent), fileName(""), historySize(0)
{
    header = new Header;
    historyVector = new std::vector<History*>;
}

IMt4Reader::IMt4Reader(QString fName) : fileName(fName), historySize(0)
{
    header = new Header;
    historyVector = new std::vector<History*>;
}

IMt4Reader::~IMt4Reader()
{
    if( header )
        delete header;
    if( historyVector )
    {
        for(int i = 0; i < historySize; i++)
            delete (*historyVector)[i];
        delete historyVector;
    }
}

void IMt4Reader::setFileName(QString fName)
{
    fileName = fName;
}

QString IMt4Reader::getFileName() const
{
    return fileName;
}

qint32 IMt4Reader::getHistorySize() const
{
    return historySize;
}

qint32 IMt4Reader::getHistoryVersion() const
{
    return historyVersion;
}

Header *IMt4Reader::getHeader()
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

std::vector<History *> *IMt4Reader::getHistoryVector()
{
    return historyVector;
}

QString IMt4Reader::getHistoryString(qint32 position) const
{
    if( fileExists )
        return QString("%1, %2, %3, %4, %5, %6")
                .arg( QDateTime::fromTime_t( (*historyVector)[position]->Time )
                        .toString("yyyy.MM.dd hh:mm:ss") )
                .arg( (*historyVector)[position]->Open , 0, 'f', header->Digits )
                .arg( (*historyVector)[position]->High , 0, 'f', header->Digits )
                .arg( (*historyVector)[position]->Low  , 0, 'f', header->Digits )
                .arg( (*historyVector)[position]->Close, 0, 'f', header->Digits )
                .arg( (*historyVector)[position]->Volume );
    return "File not exists.";
}
