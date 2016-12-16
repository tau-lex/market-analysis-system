#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QLineEdit>
#include "hstreader.h"
#include "csvreader.h"
//#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
    if( historyReader )
        delete historyReader;
    if( forecastWriter )
        delete forecastWriter;
}

void MainWindow::on_findFileButton_clicked()
{
    filePath = QFileDialog::getOpenFileName( this, tr("Open file:"), "D:\\Projects\\MQL5 History", tr("History file (*.hst *.csv)") );
    ui->filePathEdit->setText( filePath );
    ui->textBrowser->insertPlainText( filePath + "\n\n" );
    ui->textBrowser->setUpdatesEnabled(true);
}

void MainWindow::on_pushButton_clicked()
{
    if( filePath.contains(".hst") )
        readHistory( FileType::HST );
    else if( filePath.contains(".csv") )
        readHistory( FileType::CSV );
    else
        ui->textBrowser->insertPlainText("Sorry, file not found!\n\n");
}

void MainWindow::on_saveCsvButton_clicked()
{
    if( forecastWriter )
        delete forecastWriter;
    if( !historyReader )
        ui->textBrowser->insertPlainText("Not find open file.\n");

    QString outFile = "D:\\Projects\\MQL5 History\\newPrediction";
    outFile = QString("%1-%2%3.csv").arg( outFile )
                                .arg( QString(historyReader->getHeader()->Symbol) )
                                .arg( historyReader->getHeader()->Period );
    forecastWriter = new CsvWriter( outFile );

    HeaderWr *header = forecastWriter->getHeader();
    header->Symbol = QString(historyReader->getHeader()->Symbol);
    header->Period = historyReader->getHeader()->Period;
    header->Digits = historyReader->getHeader()->Digits;
    header->Depth = 1;

    std::vector<Forecast*> *forecast = forecastWriter->getForecastVector();
    for( qint32 i = 0; i < historyReader->getHistorySize() - 1; i++ )
    {
        Forecast *newFLine = getNewForecast( (*historyReader->getHistoryVector())[i],
                                             (*historyReader->getHistoryVector())[i + 1]->Time );
        //newFLine->Time =     ( *historyReader->getHistoryVector() )[i]->Time;
        //newFLine->High[0] =  ( *historyReader->getHistoryVector() )[i]->High;
        //newFLine->Low[0] =   ( *historyReader->getHistoryVector() )[i]->Low;
        //newFLine->Close[0] = ( *historyReader->getHistoryVector() )[i]->Close;

        forecast->push_back( newFLine );
        forecastWriter->setSize(i);
    }

    forecastWriter->writeFile();

    ui->textBrowser->insertPlainText("Save csv file - Done!\n");
}

void MainWindow::on_action_triggered()
{
    ui->textBrowser->clear();
}

void MainWindow::readHistory(FileType type)
{
    if( historyReader )
        delete historyReader;

    if( type == FileType::HST )
        historyReader = new HstReader( filePath );
    else
        historyReader = new CsvReader( filePath );

    historyReader->readFromFile();
    ui->textBrowser->insertPlainText( historyReader->getHeaderString() + "\n" );

    ///*
    for(int i = 0; i < historyReader->getHistorySize(); i++)
    {
        ui->textBrowser->insertPlainText( historyReader->getHistoryString( i ) + "\n" );
    }//*/

    QString tempMsg = QString( "MW: File readed. History size - %1\n\n" ).arg( historyReader->getHistorySize() );
    ui->textBrowser->insertPlainText( tempMsg );
}

void MainWindow::on_runOpenNNButton_clicked()
{
    try
    {
        ui->textBrowser->insertPlainText( "OpenNN. Simple Test Time Series Application.\n\n" );

        srand((unsigned)time(NULL));

        ui->textBrowser->insertPlainText( "DataSet... " );
        // Data set ( Набор данных )
        DataSet data_set;
        data_set.set( historyReader->getHistorySize() - 1, 9 );
        data_set.set_data( *getMatrixFromReader(historyReader) );

        // Variables ( Информация по входным и выходным данным )
        Variables* variables_pointer = data_set.get_variables_pointer();
        Vector< Variables::Item > variables_items(9);

        variables_items[0].name = "Time";
        variables_items[0].units = "Seconds";
        variables_items[0].use = Variables::Input;
        variables_items[1].name = "Open";
        variables_items[1].units = "price";
        variables_items[1].use = Variables::Input;
        variables_items[2].name = "High";
        variables_items[2].units = "price";
        variables_items[2].use = Variables::Input;
        variables_items[3].name = "Low";
        variables_items[3].units = "price";
        variables_items[3].use = Variables::Input;
        variables_items[4].name = "Close";
        variables_items[4].units = "price";
        variables_items[4].use = Variables::Input;
        variables_items[5].name = "Volume";
        variables_items[5].units = "";
        variables_items[5].use = Variables::Input;
        variables_items[6].name = "outHigh";
        variables_items[6].units = "price";
        variables_items[6].use = Variables::Target;
        variables_items[7].name = "outLow";
        variables_items[7].units = "price";
        variables_items[7].use = Variables::Target;
        variables_items[8].name = "outClose";
        variables_items[8].units = "price";
        variables_items[8].use = Variables::Target;

        variables_pointer->set_items(variables_items);

        ui->textBrowser->insertPlainText( "Done!\n" );

        const Matrix<std::string> inputs_information = variables_pointer->arrange_inputs_information();
        const Matrix<std::string> targets_information = variables_pointer->arrange_targets_information();

        // Instances ( Разбиение на обучающие, обобщающие и тестовые данные )
        Instances* instances_pointer = data_set.get_instances_pointer();
        instances_pointer->split_random_indices(); // training = 0.6, generalization = 0.2, testing = 0.2

        const Vector< Statistics<double> > inputs_statistics = data_set.scale_inputs_mean_standard_deviation();
        const Vector< Statistics<double> > outputs_statistics = data_set.scale_targets_mean_standard_deviation();

        ui->textBrowser->insertPlainText( "Neural Network... " );
        // Neural network ( Создание нейро сети )
        NeuralNetwork neural_network(6, 6, 3);

        Inputs* inputs_pointer = neural_network.get_inputs_pointer();
        inputs_pointer->set_information(inputs_information);

        Outputs* outputs_pointer = neural_network.get_outputs_pointer();
        outputs_pointer->set_information(targets_information);
            // Scaling ( Масштабирование (нормирование) данных )
        neural_network.construct_scaling_layer();
        ScalingLayer* scaling_layer_pointer = neural_network.get_scaling_layer_pointer();
        scaling_layer_pointer->set_statistics(inputs_statistics);
        scaling_layer_pointer->set_scaling_method(ScalingLayer::NoScaling); // MeanStandardDeviation?
            // Unscaling ( Демасштабирование данных )
        neural_network.construct_unscaling_layer();
        UnscalingLayer* unscaling_layer_pointer = neural_network.get_unscaling_layer_pointer();
        unscaling_layer_pointer->set_statistics(outputs_statistics);
        unscaling_layer_pointer->set_unscaling_method(UnscalingLayer::NoUnscaling); // MeanStandardDeviation?

        ui->textBrowser->insertPlainText( "Done!\n" );

        ui->textBrowser->insertPlainText( "Performance functional... " );
        // Performance functional
        PerformanceFunctional performance_functional(&neural_network, &data_set);
        performance_functional.set_regularization_type(PerformanceFunctional::NEURAL_PARAMETERS_NORM); //need?

        ui->textBrowser->insertPlainText( "Done!\n" );

        ui->textBrowser->insertPlainText( "Training strategy... " );
        // Training strategy
        TrainingStrategy training_strategy(&performance_functional);

        QuasiNewtonMethod* quasi_Newton_method_pointer = training_strategy.get_quasi_Newton_method_pointer();
        quasi_Newton_method_pointer->set_maximum_iterations_number(1000);
        quasi_Newton_method_pointer->set_display_period(10);
        quasi_Newton_method_pointer->set_minimum_performance_increase(1.0e-6);
        quasi_Newton_method_pointer->set_reserve_performance_history(true);

        TrainingStrategy::Results training_strategy_results = training_strategy.perform_training();

        ui->textBrowser->insertPlainText( "Done!\n" );

        ui->textBrowser->insertPlainText( "Testing analysis... " );
        // Testing analysis
        TestingAnalysis testing_analysis(&neural_network, &data_set);
        TestingAnalysis::LinearRegressionResults linear_regression_results = testing_analysis.perform_linear_regression_analysis();

        ui->textBrowser->insertPlainText( "Done!\n" );

        ui->textBrowser->insertPlainText( "Save results... " );
        // Save results
        scaling_layer_pointer->set_scaling_method(ScalingLayer::MeanStandardDeviation);
        unscaling_layer_pointer->set_unscaling_method(UnscalingLayer::MeanStandardDeviation);

        data_set.save("D:/Projects/data/data_set.xml");

        neural_network.save("D:/Projects/data/neural_network.xml");
        neural_network.save_expression("D:/Projects/data/expression.txt");

        performance_functional.save("D:/Projects/data/performance_functional.xml");

        training_strategy.save("D:/Projects/data/training_strategy.xml");
        training_strategy_results.save("D:/Projects/data/training_strategy_results.dat");

        linear_regression_results.save("D:/Projects/data/linear_regression_analysis_results.dat");

        ui->textBrowser->insertPlainText( "Done!\n" );
        //return(0);
    }
    catch(std::exception& e)
    {
        ui->textBrowser->insertPlainText( e.what() );

        //return(1);
    }
}

Matrix<double> *MainWindow::getMatrixFromReader(IMt4Reader *reader)
{
    qint32 size = reader->getHistorySize();
    std::vector<History *> *history = reader->getHistoryVector();

    Matrix<double> *matrixDS = new Matrix<double>;
    matrixDS->set( size - 1, 9 );

    for( qint32 i = 0; i < size - 1; i++ )
    {
        Vector<double> newRow;
        // Input
        newRow.push_back( (double)(*history)[i]->Time );
        newRow.push_back( (*history)[i]->Open );
        newRow.push_back( (*history)[i]->High );
        newRow.push_back( (*history)[i]->Low );
        newRow.push_back( (*history)[i]->Close );
        newRow.push_back( (double)(*history)[i]->Volume );
        // Output
        newRow.push_back( (*history)[i+1]->High );
        newRow.push_back( (*history)[i+1]->Low );
        newRow.push_back( (*history)[i+1]->Close );

        matrixDS->set_row( i, newRow );
    }

    return matrixDS;
}

Forecast *MainWindow::getNewForecast(const History *hist, qint32 forcastTime)
{
    Forecast *newForecast = new Forecast;
    newForecast->Time = forcastTime;
    double Time = static_cast<double>(forcastTime);
    double Open = hist->Open;
    double High = hist->High;
    double Low = hist->Low;
    double Close = hist->Close;
    double Volume = static_cast<double>(hist->Volume);

    double scaled_Time = ( Time - 1.22607e+09 ) / 1.46901e+08;
    double scaled_Open = ( Open - 1.23565 ) / 0.168808;
    double scaled_High = ( High - 1.24155 ) / 0.169224;
    double scaled_Low = ( Low - 1.22981 ) / 0.16817;
    double scaled_Close = ( Close - 1.23576 ) / 0.16864;
    double scaled_Volume = ( Volume - 55038.5 ) / 61291.1;
    double y_1_1 = tanh( -0.493731 + 1.31289 * scaled_Time +
                         2.15081 *  scaled_Open - 0.89018 * scaled_High -
                         0.381082 * scaled_Low +  0.85078 * scaled_Close +
                         1.07173 *  scaled_Volume );
    double y_1_2 = tanh( -0.388098 + 0.559863 * scaled_Time +
                         0.675013 *  scaled_Open + 0.787622 * scaled_High +
                         0.0367613 * scaled_Low -  0.774004 * scaled_Close +
                         0.241172 *  scaled_Volume );
    double y_1_3 = tanh( -0.53812 + 0.26891 * scaled_Time +
                         0.386367 *  scaled_Open - 0.490414 *  scaled_High -
                         0.746751 *  scaled_Low -  0.0889836 * scaled_Close +
                         0.111324 *  scaled_Volume );
    double y_1_4 = tanh( -1.70943 - 0.305006 * scaled_Time -
                         0.0102027 *  scaled_Open - 0.0670519 * scaled_High +
                         0.820993 *   scaled_Low +  0.423657 *  scaled_Close +
                         0.00298224 * scaled_Volume );
    double y_1_5 = tanh( -0.356751 - 1.03923 * scaled_Time -
                         0.759348 * scaled_Open + 0.190465 * scaled_High -
                         0.409322 * scaled_Low -  1.05359 *  scaled_Close -
                         0.65556 *  scaled_Volume );
    double y_1_6 = tanh( 1.50643 + 0.393741 * scaled_Time +
                         0.369172 *  scaled_Open + 0.817134 * scaled_High +
                         0.0705429 * scaled_Low -  0.469911 * scaled_Close -
                         0.174542 *  scaled_Volume );
    double scaled_outHigh = ( -0.0222355 - 0.0760875 * y_1_1 +
                              0.375507 * y_1_2 - 0.842273 * y_1_3 +
                              0.743765 * y_1_4 - 0.117617 * y_1_5 +
                              0.466218 * y_1_6 );
    double scaled_outLow = ( 0.000287203 - 0.212282 * y_1_1 +
                             0.567827 * y_1_2 - 0.774556 * y_1_3 +
                             0.762309 * y_1_4 - 0.105843 * y_1_5 +
                             0.532234 * y_1_6 );
    double scaled_outClose = ( -0.00141902 - 0.137676 * y_1_1 +
                               0.455118 * y_1_2 - 0.808174 * y_1_3 +
                               0.771652 * y_1_4 - 0.114845 * y_1_5 +
                               0.494899 * y_1_6 );
    newForecast->High[0] = 1.2416 + 0.169133 * scaled_outHigh;
    newForecast->Low[0] = 1.22987 + 0.168074 * scaled_outLow;
    newForecast->Close[0] = 1.23581 + 0.168547 * scaled_outClose;

    return newForecast;
}
