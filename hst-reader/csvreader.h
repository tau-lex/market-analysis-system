#ifndef CSVREADER_H
#define CSVREADER_H

#include <QObject>
#include <QVector>
#include <QFile>

typedef struct Header       // Total 148 bytes
{
    qint32 Version;         // database version - 400 or 401 = 4 bytes
    QChar Copyright[64];    // copyright info = 64 bytes
    QChar Symbol[12];       // symbol name = 12 bytes
    qint32 Period;          // symbol timeframe	= 4 bytes
    qint32 Digits;          // the amount of digits after decimal point	= 4 bytes
    qint32 TimeSign;        // timesign of the database creation = 4 bytes
    qint32 LastSync;        // the last synchronization time = 4 bytes
} Header;
typedef struct History      // Total 60 bytes (version 401)
{
    qint64 Time;            // bar start time = 8 bytes
    double Open;            // open price = 8 bytes
    double High;            // highest price = 8 bytes
    double Low;             // lowest price = 8 bytes
    double Close;           // close price = 8 bytes
    qint64 Volume;          // tick count = 8 bytes
} History;

class CsvReader : public QObject
{
    Q_OBJECT
public:
    explicit CsvReader(QObject *parent = 0);
    CsvReader(QString fName);
    ~CsvReader();

private:
    Header *header;
    std::vector<History*> *historyVector;

    uint historySize;

    QString fileName;
    bool fileExists;

private:
    Header* readHeader(QFile &f);
    History* readHistory(QFile &f);

public slots:
    void setFileName(QString fName);
    QString getFileName() const;
    uint getHistorySize() const;

    bool readFromFile();

    Header *getHeaderStruct();
    QString getHeaderString() const;

    std::vector<History*> *getHistoryVector();
    QString getHistoryString(uint numberPosition) const;
};

#endif // CSVREADER_H
