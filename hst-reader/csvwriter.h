#ifndef CSVWRITER_H
#define CSVWRITER_H

#include <QObject>

//+----------------TimeSeries Structures--------------------------------------+
typedef struct HeaderWr
{
    qint32      Version = 411;
    QString     Copyright = {"Copyright 2016, Terentew Aleksey"};
    QString     Symbol;
    qint32      Period;
    qint32      Digits;
    qint32      TimeSign;
    qint32      LastSync;
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
    qint32 forecastSize;

    HeaderWr *header;
    std::vector<Forecast *> *forecastVector;

public slots:
    void setFileName(QString fName);
    QString getFileName() const;
    void setSize(qint32 size);
    qint32 getSize() const;
    qint32 getDepth() const;

    HeaderWr *getHeader();
    std::vector<Forecast *> *getForecastVector();
    void writeFile();
    void writeFile(QString fName);
};

#endif // CSVWRITER_H
