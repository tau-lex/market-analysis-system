#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPointer>
#include "imt4reader.h"
#include "csvwriter.h"

// OpenNN includes
#include "../opennn/opennn.h"
using namespace OpenNN;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_findFileButton_clicked();
    void on_pushButton_clicked();
    void on_saveCsvButton_clicked();
    void on_action_triggered();

    void readHistory(FileType type);

    void on_runOpenNNButton_clicked();

    Matrix<double> *getMatrixFromReader(IMt4Reader *reader);
    Forecast *getNewForecast(const History *hist, qint32 forcastTime);

private:
    Ui::MainWindow *ui;
    QPointer<IMt4Reader> historyReader;
    QPointer<CsvWriter> forecastWriter;

    QString filePath;
};

#endif // MAINWINDOW_H
