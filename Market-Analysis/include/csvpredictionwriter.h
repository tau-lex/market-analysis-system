#ifndef CSVPREDICTIONWRITER_H
#define CSVPREDICTIONWRITER_H

#include <QObject>
#include "include/csvwriter.h"

//+----------------TimeSeries Structures--------------------------------------+
typedef struct PHeader
{
    qint32      Version = 411;
    QString     Copyright = {"Copyright 2016, Terentew Aleksey"};
    QString     Symbol;
    qint32      Period;
    qint32      Digits = 4;
    qint32      TimeSign;
    qint32      LastSync;
    qint32      Depth = 1;      // forecast timeseries length [1 - 11]
} PHeader;
typedef struct Forecast
{
    qint32      Time;       // open time of first bar in forecast [0]
    double      High[11];
    double      Low[11];
    double      Close[11];
} Forecast;

//+----------------Class CsvWriter--------------------------------------------+
class CsvPredictionWriter : public CsvWriter
{
    Q_OBJECT
public:
    explicit CsvPredictionWriter(QObject *parent = 0);
    CsvPredictionWriter(QString fName);
    ~CsvPredictionWriter();

private:
    PHeader                 *header;
    QList<Forecast *>       *dataPrediction;

public:
    PHeader *getHeader(void);
    QList<Forecast *> *getDataPredictionPtr(void);
    void writeFile(void);
    void writeFile(const QString fName);
};

#endif // CSVPREDICTIONWRITER_H
