#include "hstreader.h"
#include <QFile>
#include <QString>
#include <QDataStream>
#include <QDebug>

QDataStream& operator >>(QDataStream &out, HeaderBytes &header)
{
    out >> header.Version;
    char data[64];
    out.readRawData(data, 64);
    for(int i = 0; i < 64; i++) header.Copyright[i] = (QChar)data[i];
    out.readRawData(data, 12);
    for(int i = 0; i < 12; i++) header.Symbol[i] = (QChar)data[i];
    out >> header.Period;
    out >> header.Digits;
    out >> header.TimeSign;
    out >> header.LastSync;
    out.skipRawData(13 * 4);

    return out;
}

QDataStream& operator >>(QDataStream &out, HistoryBytes &history)
{
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

HstReader::HstReader(QObject *parent) : QObject(parent)
{

}

HstReader::HstReader(QString fName) : fileName(fName)
{ }

HstReader::~HstReader()
{
    //if(!historyVector.empty())
    //    delete[] historyVector;
}

bool HstReader::readFromFile()
{
    qDebug() << "open file..";
    QFile file(fileName, this);

    if(file.open(QIODevice::ReadOnly))
    {
        QDataStream input(&file);
        input >> header;
        qDebug() << "done";
        qDebug() << this->getHeaderString();

        while (!file.atEnd())
        {
            HistoryBytes hLine;
            input >> hLine;
            historyVector.append(&hLine);

            qDebug() << getHistoryString(historySize);
            historySize++;
        }

        return true;
    }
    else
    {
        qDebug()<< "don't open file";

        return false;
    }
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

HeaderBytes *HstReader::getHeaderStruct()
{
    return &header;
}

QString HstReader::getHeaderString() const
{
    return QString("%1,%2,%3,%4,%5,%6,%7").arg(header.Version)
                                        .arg(QString(header.Copyright))
                                        .arg(QString(header.Symbol))
                                        .arg(header.Period)
                                        .arg(header.Digits)
                                        .arg(header.TimeSign)
                                        .arg(header.LastSync);
}

QVector<HistoryBytes*> HstReader::getHistoryVector() const
{
    return historyVector;
}

QString HstReader::getHistoryString(int numberPosition) const
{
    return QString("%1,%2,%3,%4,%5,%6,%7,%8").arg(historyVector.at(numberPosition)->Time)
                                            .arg(historyVector.at(numberPosition)->Open)
                                            .arg(historyVector.at(numberPosition)->High)
                                            .arg(historyVector.at(numberPosition)->Low)
                                            .arg(historyVector.at(numberPosition)->Close)
                                            .arg(historyVector.at(numberPosition)->Volume)
                                            .arg(historyVector.at(numberPosition)->Spread)
                                            .arg(historyVector.at(numberPosition)->RealVolume);
}
