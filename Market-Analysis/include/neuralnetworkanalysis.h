#ifndef NEURALNETWORKANALYSIS_H
#define NEURALNETWORKANALYSIS_H

#include <QObject>
#include "include/settingsstruct.h"
#include "include/imt4reader.h"

// include nn library
#include "../opennn/opennn.h"
using namespace OpenNN;

class NeuralNetworkAnalysis : public QObject
{
    Q_OBJECT
public:
    explicit NeuralNetworkAnalysis(QObject *parent = 0);
    ~NeuralNetworkAnalysis();

signals:
    void trained(QString);
    void progress(QString, qint32);
    void message(QString, QString);

public slots:
    void runTraining();
    void runPrediction();
    void stop();
    void setConfigKit(ConfigMT4 *cfg);
    void setLoaded(bool isLoaded);

private:
    ConfigMT4                       *config;
    QString                         nameKit;
    bool                            isLoaded;
    qint32                          rowsDS = 1,
                                    columnsDS = 0;
    Matrix<double>                  *matrixDS;
    DataSet                         *dataSet;
    NeuralNetwork                   *neuralNetwork;
    PerformanceFunctional           *performanceFunc;
    TrainingStrategy                *trainingStrategy;
    Matrix<std::string>             inputsInfo;
    Matrix<std::string>             targetsInfo;
    Vector< Statistics<double> >    inputsStatistics;
    Vector< Statistics<double> >    outputsStatistics;

private slots:
    void prepareDataSet();
    void prepareVariablesInfo();
    void prepareInstances();
    void prepareNeuralNetwork();
    void preparePerformanceFunc();

    inline bool checkSymbolIsTime(QString &symbol);
    void getFirstEntryTime(QMap<QString, IMt4Reader *> &readers, qint64 &first, qint64 &last);

};

#endif // NEURALNETWORKANALYSIS_H
