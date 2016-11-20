#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QLineEdit>
#include "hstreader.h"

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

private:
    Ui::MainWindow *ui;
    HstReader *historyReader;

    QString filePath;
};

#endif // MAINWINDOW_H
