#include "include/neuralnetworkanalysis.h"
#include "include/hstreader.h"
#include "include/csvreader.h"
#include "include/csvwriter.h"

#include <QDateTime>
#include <QApplication>

#include <QDebug>
#include <QThread>

NeuralNetworkAnalysis::NeuralNetworkAnalysis(QObject *parent) : QObject(parent),
    matrixDS(nullptr),
    dataSet(nullptr),
    neuralNetwork(nullptr),
    performanceFunc(nullptr)
{
    srand((unsigned)time(NULL));
}

NeuralNetworkAnalysis::~NeuralNetworkAnalysis()
{
    if( performanceFunc )
        delete performanceFunc;
    if( neuralNetwork )
        delete neuralNetwork;
    if( dataSet )
        delete dataSet;
    if( matrixDS )
        delete matrixDS;
}

void NeuralNetworkAnalysis::runTraining()
{
    qDebug()<<"From nn thread: "<<QThread::currentThreadId();
    try {
        prepareDataSet();
        prepareVariablesInfo();
        prepareInstances();
        prepareNeuralNetwork();
        preparePerformanceFunc();


        trained( config->nameKit );
    } catch(int e) {
        message( config->nameKit, tr("Error prepare Data Set - %1").arg(e) );
    }
}

void NeuralNetworkAnalysis::runPrediction()
{
    qDebug()<<"From nn thread: "<<QThread::currentThreadId();
}

void NeuralNetworkAnalysis::stop()
{
    qDebug()<<"From nn thread: "<<QThread::currentThreadId();
}

void NeuralNetworkAnalysis::setConfigKit(ConfigMT4 *cfg)
{
    config = cfg;
}

void NeuralNetworkAnalysis::setLoaded(bool isLoaded)
{
    this->isLoaded = isLoaded;
}

void NeuralNetworkAnalysis::prepareDataSet()
{
    message( config->nameKit, tr("Start prepare Data Set.") );
    QMap<QString, IMt4Reader *> readers;
    QMap<QString, qint32> iters;
    matrixDS = new Matrix<double>;
    //==========================
    foreach( QString symbol, config->input ) {
        iters[symbol] = 0;
        if( checkSymbolIsTime(symbol) ) {
            columnsDS += 1;
            continue; // is Time
        } else {
            columnsDS += 4;
            if( config->volumeIn )
                columnsDS += 1;
        }
        readers[symbol] = new HstReader( QString("%1%2%3.hst").arg( config->mt4Path )
                                         .arg( config->historyPath )
                                         .arg( symbol ) );
        if( readers[symbol]->readFromFile() ) {
            message( config->nameKit, tr("History file \"%1\" succeful loaded.")
                     .arg( readers[symbol]->getFileName() ) );
        } else {
            message( config->nameKit, tr("History file \"%1\" cannot be loaded.")
                     .arg( readers[symbol]->getFileName() ) );
            throw 20;
        }
    }
    foreach( QString symbol, config->output ) {
        if( checkSymbolIsTime(symbol) )
            columnsDS += 1;
        else
            columnsDS += 3;
    }
    qint64 timeCurrentIter, lastEntryTime;
    getFirstEntryTime( readers, timeCurrentIter, lastEntryTime );
    message( config->nameKit, tr("The data set belongs to the interval of time:\n\t%1 (%2 sec.) - %3 (%4 sec.)")
                              .arg( QDateTime::fromTime_t( timeCurrentIter )
                                    .toString("yyyy.MM.dd hh:mm:ss") )
                              .arg( timeCurrentIter )
                              .arg( QDateTime::fromTime_t( lastEntryTime )
                                    .toString("yyyy.MM.dd hh:mm:ss") )
                              .arg( lastEntryTime ));
    rowsDS = ( lastEntryTime - timeCurrentIter ) / ( 60 * config->period );
    //=========================== copy data to matrix
    matrixDS->set( rowsDS, columnsDS );
    bool nextIteration = true;
    while( nextIteration ) {
        Vector<double> newRow;
        foreach( QString symbol, config->input ) {
            if( readers.contains(symbol) ) { //timeseries
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]]->Open );
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]]->High );
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]]->Low );
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]]->Close );
                if( (*readers[symbol]->getHistoryVector())[iters[symbol]]->Time <= timeCurrentIter )
                    iters[symbol]++;
            } else { //time
                if( symbol == "YEAR")
                    newRow.push_back( static_cast<double>(QDateTime::fromTime_t( timeCurrentIter ).date().year()) );
                else if( symbol == "MONTH")
                    newRow.push_back( static_cast<double>(QDateTime::fromTime_t( timeCurrentIter ).date().month()) );
                else if( symbol == "DAY")
                    newRow.push_back( static_cast<double>(QDateTime::fromTime_t( timeCurrentIter ).date().day()) );
                else if( symbol == "HOUR")
                    newRow.push_back( static_cast<double>(QDateTime::fromTime_t( timeCurrentIter ).time().hour()) );
                else if( symbol == "MINUTE")
                    newRow.push_back( static_cast<double>(QDateTime::fromTime_t( timeCurrentIter ).time().minute()) );
                else if( symbol == "WEEKDAY")
                    newRow.push_back( static_cast<double>(QDateTime::fromTime_t( timeCurrentIter ).date().dayOfWeek()) );
            }
        }
        foreach( QString symbol, config->output ) {
            if( readers.contains(symbol) ) { //timeseries
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]+1]->High );
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]+1]->Low );
                newRow.push_back( (*readers[symbol]->getHistoryVector())[iters[symbol]+1]->Close );
                if( (iters[symbol] + 2) >= readers[symbol]->getHistorySize() )
                    nextIteration = false;
            }
        }
        matrixDS->append_row( newRow );
        timeCurrentIter += ( 60 * config->period ); // + 1 bar
        config->progress = lastEntryTime / 100 * timeCurrentIter;
        progress( config->nameKit, config->progress );
    }
    //========================== clean readers and save dataset
    dataSet = new DataSet( matrixDS->get_rows_number(), matrixDS->get_columns_number() );
    dataSet->set_data( *matrixDS );
    config->progress = 100;
    progress( config->nameKit, config->progress );
    // clean history readers
    QMapIterator<QString, IMt4Reader *> i(readers);
    while( i.hasNext() ) {
        i.next();
        delete i.value();
    }
    message( config->nameKit, tr("Prepare Data Set done.") );
}

void NeuralNetworkAnalysis::prepareVariablesInfo()
{
    message( config->nameKit, tr("Start prepare Variables Information.") );
    Variables* variablesPtr = dataSet->get_variables_pointer();
    Vector< Variables::Item > varItems( columnsDS );
    qint32 idx = 0;
    foreach( QString symbol, config->input ) {
        if( !checkSymbolIsTime(symbol) ) {
            for( qint32 i = 0; i < 4; i++ ) {
                varItems[idx].name = symbol.toStdString();
                switch( i ) {
                case 0: varItems[idx].units = "Open"; break;
                case 1: varItems[idx].units = "High"; break;
                case 2: varItems[idx].units = "Low"; break;
                case 3: varItems[idx].units = "Close"; break;
                default: ;
                }
                varItems[idx].use = Variables::Input;
                idx += i != 3 ? 1 : 0;
            }
        } else {
            varItems[idx].name = symbol.toStdString();
            varItems[idx].units = "Time";
            varItems[idx].use = Variables::Input;
        }
        idx++;
        if( idx >= columnsDS )
            throw 21;
    }
    foreach( QString symbol, config->output ) {
        if( !checkSymbolIsTime(symbol) ) {
            for( qint32 i = 0; i < 3; i++ ) {
                varItems[idx].name = symbol.toStdString();
                switch( i ) {
                case 0: varItems[idx].units = "High"; break;
                case 1: varItems[idx].units = "Low"; break;
                case 2: varItems[idx].units = "Close"; break;
                default: ;
                }
                varItems[idx].use = Variables::Target;
                idx += i != 2 ? 1 : 0;
            }
        } else {
            varItems[idx].name = symbol.toStdString();
            varItems[idx].units = "_volume";
            varItems[idx].use = Variables::Target;
        }
        idx++;
        if( idx > columnsDS )
            throw 21;
    }
    variablesPtr->set_items( varItems );
    inputsInfo = variablesPtr->arrange_inputs_information();
    targetsInfo = variablesPtr->arrange_targets_information();
}

void NeuralNetworkAnalysis::prepareInstances()
{
    message( config->nameKit, tr("Start prepare Instances.") );
    Instances* instances_pointer = dataSet->get_instances_pointer();
    instances_pointer->split_sequential_indices( config->divideInstances[0] * 0.01,
                                                 config->divideInstances[1] * 0.01,
                                                 config->divideInstances[2] * 0.01 );
    inputsStatistics = dataSet->scale_inputs_mean_standard_deviation();
    outputsStatistics = dataSet->scale_targets_mean_standard_deviation();
}

void NeuralNetworkAnalysis::prepareNeuralNetwork()
{
    message( config->nameKit, tr("Start prepare Neural Network.") );
    Vector<size_t> layers; //( config->layersCount + 2 );
    layers.push_back( 41 );
    layers.push_back( config->layersSize[0] );
    layers.push_back( config->layersSize[1] );
    layers.push_back( config->layersSize[2] );
    layers.push_back( 3 );
    neuralNetwork = new NeuralNetwork( layers );
        // Set in/out info
    Inputs* inputsPtr = neuralNetwork->get_inputs_pointer();
    inputsPtr->set_information( inputsInfo );
    Outputs* outputsPtr = neuralNetwork->get_outputs_pointer();
    outputsPtr->set_information( targetsInfo );
        // Scaling ( Масштабирование (нормирование) данных )
    neuralNetwork->construct_scaling_layer();
    ScalingLayer* scalingLayerPtr = neuralNetwork->get_scaling_layer_pointer();
    scalingLayerPtr->set_statistics( inputsStatistics );
    scalingLayerPtr->set_scaling_method( ScalingLayer::NoScaling ); // MeanStandardDeviation?
        // Unscaling ( Демасштабирование данных )
    neuralNetwork->construct_unscaling_layer();
    UnscalingLayer* unscalingLayerPtr = neuralNetwork->get_unscaling_layer_pointer();
    unscalingLayerPtr->set_statistics( outputsStatistics );
    unscalingLayerPtr->set_unscaling_method( UnscalingLayer::NoUnscaling ); // MeanStandardDeviation?
}

void NeuralNetworkAnalysis::preparePerformanceFunc()
{
    message( config->nameKit, tr("Start prepare Performance Functional.") );
    performanceFunc = new PerformanceFunctional( neuralNetwork, dataSet);
    performanceFunc->set_regularization_type( PerformanceFunctional::NEURAL_PARAMETERS_NORM ); //need?

    // Training strategy
    message( config->nameKit, tr("Start prepare Training strategy.") );
    trainingStrategy = new TrainingStrategy( performanceFunc );

    QuasiNewtonMethod* quasiNewtonMethodPtr = trainingStrategy->get_quasi_Newton_method_pointer();
    quasiNewtonMethodPtr->set_maximum_iterations_number(1000);
    quasiNewtonMethodPtr->set_display_period(10);
    quasiNewtonMethodPtr->set_minimum_performance_increase(1.0e-6);
    quasiNewtonMethodPtr->set_reserve_performance_history(true);

    TrainingStrategy::Results trainingStrategyResults = trainingStrategy->perform_training();

    // Testing analysis
    message( config->nameKit, tr("Start Testing analysis.") );
    TestingAnalysis testingAnalysis( neuralNetwork, dataSet );
    TestingAnalysis::LinearRegressionResults linearRegressionResults = testingAnalysis.perform_linear_regression_analysis();

    // Save results
    message( config->nameKit, tr("Save results.") );
    neuralNetwork->get_scaling_layer_pointer()->set_scaling_method( ScalingLayer::MeanStandardDeviation );
    neuralNetwork->get_unscaling_layer_pointer()->set_unscaling_method( UnscalingLayer::MeanStandardDeviation );

    dataSet->save( QString("%1/dataSet.xml").arg( config->kitPath ).toStdString() );

    neuralNetwork->save( QString("%1/neuralNetwork.xml").arg( config->kitPath ).toStdString() );
    neuralNetwork->save_expression( QString("%1/nnExpression.txt").arg( config->kitPath ).toStdString() );

    performanceFunc->save( QString("%1/performanceFunctional.xml").arg( config->kitPath ).toStdString() );

    trainingStrategy->save( QString("%1/trainingStrategy.xml").arg( config->kitPath ).toStdString() );
    trainingStrategyResults.save( QString("%1/tsResults.dat").arg( config->kitPath ).toStdString() );

    linearRegressionResults.save( QString("%1/linearRegressionResults.dat").arg( config->kitPath ).toStdString() );

}

inline bool NeuralNetworkAnalysis::checkSymbolIsTime(QString &symbol)
{
    if( symbol == "YEAR" || symbol == "MONTH" || symbol == "DAY" ||
            symbol == "HOUR" || symbol == "MINUTE" || symbol == "WEEKDAY")
        return true;
    return false;
}

void NeuralNetworkAnalysis::getFirstEntryTime(QMap<QString, IMt4Reader *> &readers, qint64 &first, qint64 &last)
{
    first = std::numeric_limits<qint64>::max();
    last = 0;
    QMapIterator<QString, IMt4Reader *> i(readers);
    while( i.hasNext() ) {
        i.next();
        if( i.value()->getHistorySize() > 0 ) {
            if( (*i.value()->getHistoryVector())[0]->Time < first )
                first = (*i.value()->getHistoryVector())[0]->Time;
            if( (*i.value()->getHistoryVector())[i.value()->getHistorySize()-1]->Time > last )
                last = (*i.value()->getHistoryVector())[i.value()->getHistorySize()-1]->Time;
        }
    }
}
