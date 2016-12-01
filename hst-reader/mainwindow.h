#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QLineEdit>
#include "hstreader.h"
#include "csvreader.h"

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
    void on_action_triggered();

    void readHistory();
    void readNewHistory();

private:
    Ui::MainWindow *ui;
    HstReader *historyReader;
    CsvReader *historyCReader;

    QString filePath;
};

#endif // MAINWINDOW_H
