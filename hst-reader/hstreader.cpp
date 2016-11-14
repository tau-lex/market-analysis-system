#include "hstreader.h"
#include <QFile>
#include <QDateTime>
#include <QString>
#include <QDataStream>
#include <QDebug>

QDataStream& operator >>(QDataStream &out, HeaderBytes &header)
{
    out.setByteOrder(QDataStream::LittleEndian);
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

QDataStream& operator >>(QDataStream &out, HistoryBytes &history)
{
    out.setByteOrder(QDataStream::LittleEndian);
    out >> history.Time;
    out >> history.Open;
    out >> history.High;
    out >> history.Low;
    out >> history.Close;
    out >> history.Volume;
    out >> history.Spread;
    out >> history.RealVolume;

    return out;
}

/* // Read struct HistoryBytes400 from Stream object
QDataStream& operator >>(QDataStream &out, HistoryBytes400 &history)
{
    out.setByteOrder(QDataStream::LittleEndian);
    out >> history.Time;
    out >> history.Open;
    out >> history.Low;
    out >> history.High;
    out >> history.Close;
    out >> history.Volume;

    return out;
} */

HstReader::HstReader(QObject *parent) : QObject(parent)
{ }

HstReader::HstReader(QString fName) : fileName(fName)
{ }

HstReader::~HstReader()
{
    //if(!historyVector.empty())
    //    delete[] historyVector;
}

void HstReader::setFileName(QString fName)
{
    fileName = fName;
}

QString HstReader::getFileName() const
{
    return fileName;
}

uint HstReader::getHistorySize() const
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

        input >> header;
        historyVersion = header.Version;

        while (!file.atEnd())
        {
            //if(historyVersion == 401)
                HistoryBytes historyLine;
            //else
            //    HistoryBytes400 historyLine;
            input >> historyLine;
            historyVector.append(&historyLine);
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
        return QString("v%1,%2,%3,%4,%5,%6,%7")
                .arg(header.Version)
                .arg(QString(header.Copyright))
                .arg(QString(header.Symbol))
                .arg(header.Period)
                .arg(header.Digits)
                .arg(header.TimeSign)
                .arg(header.LastSync);
    return "File not exists.";
}

QVector<HistoryBytes*> HstReader::getHistoryVector() const
{
    return historyVector;
}

QString HstReader::getHistoryString(int numberPosition) const
{
    if(fileExists)
        return QString("%1,%2,%3,%4,%5,%6,%7,%8")
                .arg(QDateTime::fromTime_t(historyVector.at(numberPosition)->Time).toString("yyyy.MM.dd hh:mm:ss"))
                .arg(historyVector.at(numberPosition)->Open)
                .arg(historyVector.at(numberPosition)->High)
                .arg(historyVector.at(numberPosition)->Low)
                .arg(historyVector.at(numberPosition)->Close)
                .arg(historyVector.at(numberPosition)->Volume)
                .arg(historyVector.at(numberPosition)->Spread)
                .arg(historyVector.at(numberPosition)->RealVolume);
    return "File not exists.";
}
