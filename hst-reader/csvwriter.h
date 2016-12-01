#ifndef CSVWRITER_H
#define CSVWRITER_H

#include <QObject>
#include <QDateTime>
#include "imt4reader.h"

//+----------------TimeSeries Structures--------------------------------------+
typedef struct HeaderWr
{
    qint32      Version = 411;
    QString     Copyright[64] = {"Copyright 2016, Terentew Aleksey"};
    QString     Symbol[12];
    qint32      Period;
    qint32      Digits;
    qint32      ForecastTimeSign;
    qint32      ForecastLastSync;
    qint32      Depth;      // forecast timeseries length [0 - 10]
} HeaderWr;
typedef struct Forecast
{
    qint32      Time;       // open time of first bar in forecast [0]
    double      High[11];   // forecast highest price
    double      Low[11];    // forecast lowest price
    double      Close[11];  // forecast close price
} Forecast;

//+----------------Class CsvWriter--------------------------------------------+
class CsvWriter : public QObject
{
    Q_OBJECT
public:
    explicit CsvWriter(QObject *parent = 0);
    CsvWriter(QString fName);
    ~CsvWriter();

private:
    QString fileName;
    qint32 forcastSize;
    qint32 forcastDepth; // trancelate?

    HeaderWr *header;
    std::vector<Forecast*> *forecast;

public slots:
    void setFileName(QString fName);
    QString getFileName() const;
    qint32 getForecastSize() const;
    void setDepth(qint32 n); // trancelate?
    qint32 getForecastDepth() const; // trancelate?

    HeaderWr *getHeader;
    std::vector<Forecast*> *getForcastVector();
    void writeFile();
    void writeFile(QString fName);
};

#endif // CSVWRITER_H
