#ifndef MARKETASSAYKIT_H
#define MARKETASSAYKIT_H

#include <QObject>
#include <QDateTime>
#include "include/configmas.h"

class MarketAssayKit : public QObject
{
    Q_OBJECT
public:
    //explicit MarketAssayKit(QObject *parent = 0);
    explicit MarketAssayKit(QString name = "default", QObject *parent = 0);
    ~MarketAssayKit();

private:
    struct MT_Tool {
        QString nameTool;
        qint32 period;
    };
    const QString configFile = "\\MQL4\\Files\\mas_mt4.conf";
    const QString newHistoryPath = "\\MQL4\\Files\\MAS_MarketData\\";
    const QString predictionPath = "\\MQL4\\Files\\MAS_Prediction\\";
    QString nameKit;
    QString pathMt4;
    QString server;
    QString historyPath; // "\\history\\_SERVER_\\"
    std::list<MT_Tool> input;
    std::list<MT_Tool> output;
    qint32 depthHistory;
    qint32 depthPrediction = 5;
    QDateTime lastTraining;
    bool isTrained;
    bool isRun;
    //list inputLayer
    //list outputLayer

signals:
    void trained();

public slots:
    void setName(const QString newName);
    QString getName() const;
    void setPathForMt4(const QString path);
    QString getPathForMt4() const;

    //void saveConf() const;
};

#endif // MARKETASSAYKIT_H
