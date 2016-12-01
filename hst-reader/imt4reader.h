#ifndef IMT4READER_H
#define IMT4READER_H

#include <QObject>
#include <QVector>

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
    // Skip 12 bytes
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
/*
typedef struct Murray
{
    qint32 Time;
    double pivot1_8;
    double pivot2_8;
    double pivot3_8;
    double pivot4_8;
    double pivot5_8;
    double pivot6_8;
    double pivot7_8;
    double pivot8_8;
} Murray; */

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
    int historySize;
    int historyVersion;

    Header *header;
    std::vector<History*> *historyVector;

protected:

public slots:
    void setFileName(QString fName);
    QString getFileName() const;
    int getHistorySize() const;
    int getHistoryVersion() const;

    virtual bool readFromFile() = 0;
    Header *getHeaderStruct();
    QString getHeaderString() const;
    std::vector<History *> *getHistoryVector();
    QString getHistoryString(int position) const;
};

#endif // IMT4READER_H
