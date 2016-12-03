#ifndef IMT4READER_H
#define IMT4READER_H

#include <QObject>

//+----------------TimeSeries Structures--------------------------------------+
typedef struct Header       // Total 148 bytes
{
    qint32  Version;        // database version (400 || 401) = 4 bytes
    QChar   Copyright[64];  // copyright info = 64 bytes
    QChar   Symbol[12];     // symbol name = 12 bytes
    qint32  Period;         // symbol timeframe	= 4 bytes
    qint32  Digits;         // amount of digits after decimal point	= 4 bytes
    qint32  TimeSign;       // timesign of the database creation = 4 bytes
    qint32  LastSync;       // the last synchronization time = 4 bytes
    //QChar Unused[52];     // to be used in future	= 52 bytes
} Header;
typedef struct History      // Total 60 bytes (version 401)
{
    qint64  Time;           // open time bar = 8 bytes
    double  Open;           // open price = 8 bytes
    double  High;           // highest price = 8 bytes
    double  Low;            // lowest price = 8 bytes
    double  Close;          // close price = 8 bytes
    qint64  Volume;         // tick count = 8 bytes
    // Skip 12 bytes (!when reading)
    //qint32 Spread;        // spread = 4 bytes
    //qint64 RealVolume;    // real volume = 8 bytes
} History;
typedef struct History400   // Total 44 bytes (version 400)
{
    qint32 Time;            // bar start time = 4 bytes
    double Open;            // open price = 8 bytes
    double Low;             // lowest price = 8 bytes
    double High;            // highest price = 8 bytes
    double Close;           // close price = 8 bytes
    double Volume;          // tick count = 8 bytes
} History400;

// Enumeration file types
enum FileType {
    HST,
    CSV
};

//+----------------Interface IMt4Reader---------------------------------------+
class IMt4Reader : public QObject
{
    Q_OBJECT
public:
    explicit IMt4Reader(QObject *parent = 0);
    IMt4Reader(QString fName);
    ~IMt4Reader();

protected:
    QString fileName;
    bool fileExists;
    FileType fileType;
    qint32 historySize;
    qint32 historyVersion;

    Header *header = 0;
    std::vector<History *> *historyVector = 0;

protected:

public slots:
    void setFileName(QString fName);
    QString getFileName() const;
    qint32 getHistorySize() const;
    qint32 getHistoryVersion() const;

    virtual bool readFromFile() = 0;
    Header *getHeader();
    QString getHeaderString() const;
    std::vector<History*> *getHistoryVector();
    QString getHistoryString(qint32 position) const;
};

#endif // IMT4READER_H
