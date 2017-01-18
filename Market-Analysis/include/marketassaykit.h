#ifndef MARKETASSAYKIT_H
#define MARKETASSAYKIT_H

#include <QObject>
#include <QThread>
#include "include/settingsstruct.h"
#include "include/neuralnetworkanalysis.h"

class MarketAssayKit : public QObject
{
    Q_OBJECT
public:
    explicit MarketAssayKit(QObject *parent = 0, ConfigMT4 *cfg = 0);
    ~MarketAssayKit();

private:
    ConfigMT4 *config;
    QThread maThread;
    NeuralNetworkAnalysis ma_nnWorker;

signals:
    void runTraining();                 // to ma_nnThread
    void runPrediction();
    void stop();
    void trained(QString);              // to presenter
    void progress(QString);
    void message(QString, QString);

private slots:
    void setConnections();
    void trained(void);                 // from ma_nnThread
    void progress(qint32 proc);
    void message(QString text);
    void pause(qint32 msec);
};

#endif // MARKETASSAYKIT_H
