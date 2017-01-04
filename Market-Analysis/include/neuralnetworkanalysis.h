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

private:
    ConfigMT4                       *config;
    QString                         nameKit;
    qint32                          rowsDS = 1;
    qint32                          columnsDS = 0;
    qint64                          firstEntryTime;
    qint64                          lastEntryTime;
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
    void loadTrainedModel();
    void prepareDataSet(FileType historyType);
    void prepareVariablesInfo();
    void prepareInstances();
    void prepareNeuralNetwork();
    void preparePerformanceFunc();
    void runTrainingNeuralNetwork();
    void runWorkingProcess();

    inline bool checkSymbolIsTime(QString &symbol);
    void getFirstEntryTime(QMap<QString, IMt4Reader *> &readers, qint64 &first, qint64 &last);
    //void parseNNExeption();
};

#endif // NEURALNETWORKANALYSIS_H
