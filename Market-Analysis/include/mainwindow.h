#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "include/presenter.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    Presenter *presenter;

signals:
    void addNewKit(QString);
    void deleteKit(QString);

public slots:
    void openTab();
    void closeTab();
    void setNameTab(QString name);

private slots:
    void setConnections();


};

#endif // MAINWINDOW_H
