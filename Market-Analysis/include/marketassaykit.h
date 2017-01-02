#ifndef MARKETASSAYKIT_H
#define MARKETASSAYKIT_H

#include <QObject>
#include <QThread>
//#include <QDateTime>
#include "include/settingsstruct.h"
#include "include/neuralnetworkanalysis.h"

class MarketAssayKit : public QObject
{
    Q_OBJECT
public:
    explicit MarketAssayKit(QObject *parent = 0);
    ~MarketAssayKit();

private:
    ConfigMT4 *config;
    QThread maThread;
    NeuralNetworkAnalysis ma_nnWorker;
    //QDateTime lastTraining;

signals:
    // to MA_NN
    void runTraining();
    void runPrediction();
    void stop();
    // from MA_NN
    void trained(QString);
    void progress(QString, qint32);
    void message(QString, QString);

public slots:
    void setKitPtr(ConfigMT4 *cfg);

private slots:
    void setConnections();
};

#endif // MARKETASSAYKIT_H
