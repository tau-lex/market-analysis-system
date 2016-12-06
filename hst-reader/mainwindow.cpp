#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QLineEdit>
#include "hstreader.h"
#include "csvreader.h"
//#include <QDebug>

// OpenNN includes
#include "../opennn/opennn.h"
using namespace OpenNN;

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

    QString outFile = "D:\\Projects\\MQL5 History\\csvWriter";
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
    for( qint32 i = 0; i < historyReader->getHistorySize(); i++ )
    {
        Forecast *newFLine = new Forecast;
        newFLine->Time =     ( *historyReader->getHistoryVector() )[i]->Time;
        newFLine->High[0] =  ( *historyReader->getHistoryVector() )[i]->High;
        newFLine->Low[0] =   ( *historyReader->getHistoryVector() )[i]->Low;
        newFLine->Close[0] = ( *historyReader->getHistoryVector() )[i]->Close;

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
    ui->textBrowser->insertPlainText( historyReader->getHeaderString() + "\n\n" );

    for(int i = 0; i < historyReader->getHistorySize(); i++)
    {
        ui->textBrowser->insertPlainText( historyReader->getHistoryString( i ) + "\n" );
    }

    QString tempMsg = QString( "\nMW: File readed. History size - %1\n" ).arg( historyReader->getHistorySize() );
    ui->textBrowser->insertPlainText( tempMsg );
}

void MainWindow::on_runOpenNNButton_clicked()
{
    try
    {
        std::cout << "OpenNN. Iris Plant Application." << std::endl;

        srand((unsigned)time(NULL));

        // Data set

        DataSet data_set;

        data_set.set_data_file_name("../data/iris_plant.dat");

        data_set.set_separator("Space");

        data_set.load_data();

        // Variables

        Variables* variables_pointer = data_set.get_variables_pointer();

        variables_pointer->set_name(0, "sepal_length");
        variables_pointer->set_units(0, "centimeters");
        variables_pointer->set_use(0, Variables::Input);

        variables_pointer->set_name(1, "sepal_width");
        variables_pointer->set_units(1, "centimeters");
        variables_pointer->set_use(1, Variables::Input);

        variables_pointer->set_name(2, "petal_length");
        variables_pointer->set_units(2, "centimeters");
        variables_pointer->set_use(2, Variables::Input);

        variables_pointer->set_name(3, "petal_width");
        variables_pointer->set_units(3, "centimeters");
        variables_pointer->set_use(3, Variables::Input);

        variables_pointer->set_name(4, "iris_setosa");
        variables_pointer->set_use(4, Variables::Target);

        variables_pointer->set_name(5, "iris_versicolour");
        variables_pointer->set_use(5, Variables::Target);

        variables_pointer->set_name(6, "iris_virginica");
        variables_pointer->set_use(6, Variables::Target);

        const Matrix<std::string> inputs_information = variables_pointer->arrange_inputs_information();
        const Matrix<std::string> targets_information = variables_pointer->arrange_targets_information();

        // Instances

        Instances* instances_pointer = data_set.get_instances_pointer();

        instances_pointer->split_random_indices();

        const Vector< Statistics<double> > inputs_statistics = data_set.scale_inputs_minimum_maximum();

        // Neural network

        NeuralNetwork neural_network(4, 6, 3);

        Inputs* inputs_pointer = neural_network.get_inputs_pointer();

        inputs_pointer->set_information(inputs_information);

        Outputs* outputs_pointer = neural_network.get_outputs_pointer();

        outputs_pointer->set_information(targets_information);

        neural_network.construct_scaling_layer();

        ScalingLayer* scaling_layer_pointer = neural_network.get_scaling_layer_pointer();

        scaling_layer_pointer->set_statistics(inputs_statistics);

        scaling_layer_pointer->set_scaling_method(ScalingLayer::NoScaling);

        neural_network.construct_probabilistic_layer();

        ProbabilisticLayer* probabilistic_layer_pointer = neural_network.get_probabilistic_layer_pointer();

        probabilistic_layer_pointer->set_probabilistic_method(ProbabilisticLayer::Softmax);

        // Performance functional

        PerformanceFunctional performance_functional(&neural_network, &data_set);

        // Training strategy

        TrainingStrategy training_strategy(&performance_functional);

        training_strategy.set_main_type(TrainingStrategy::QUASI_NEWTON_METHOD);

        QuasiNewtonMethod* quasi_Newton_method_pointer = training_strategy.get_quasi_Newton_method_pointer();

        quasi_Newton_method_pointer->set_minimum_performance_increase(1.0e-6);

        quasi_Newton_method_pointer->set_display(false);

        // Model selection

        ModelSelection model_selection(&training_strategy);

        model_selection.set_order_selection_type(ModelSelection::GOLDEN_SECTION);

        GoldenSectionOrder* golden_section_order_pointer = model_selection.get_golden_section_order_pointer();

        golden_section_order_pointer->set_tolerance(1.0e-7);

        ModelSelection::ModelSelectionResults model_selection_results;

        model_selection_results = model_selection.perform_order_selection();

        // Testing analysis

        TestingAnalysis testing_analysis(&neural_network, &data_set);

        const Matrix<size_t> confusion = testing_analysis.calculate_confusion();

        // Save results

        scaling_layer_pointer->set_scaling_method(ScalingLayer::MinimumMaximum);

        data_set.save("../data/data_set.xml");

        neural_network.save("../data/neural_network.xml");
        neural_network.save_expression("../data/expression.txt");

        training_strategy.save("../data/training_strategy.xml");

        model_selection.save("../data/model_selection.xml");
        model_selection_results.save("../data/model_selection_results.dat");

        confusion.save("../data/confusion.dat");

        //return(0);
    }
    catch(std::exception& e)
    {
        ui->textBrowser->insertPlainText( e.what() );

        //return(1);
    }
}
