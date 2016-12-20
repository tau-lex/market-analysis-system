#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "include/presenter.h"

#include <QtWidgets/QGroupBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QListView>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QVBoxLayout>

#define MAX_TAB 5

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

    qint32 currentTab;
    qint32 countTabs;

signals:
    void addNewKit(QString);
    void deleteKit(QString);
    void opened(qint32);

private slots:
    void newKit();
    void openKit();
    void saveKit();
    void closeKit();
    void openSettings();
    void openKitConfig();
    void runTraining();
    void runWork();
    void stopWork();
    void deleteKit();
    void openHelp();
    void openAbout();

    void openTab(qint32 idx);
    void closeTab(qint32 idx);
    void selectTab(qint32 idx);
    void setConnections();

    void addTabToUi(qint32 idx);
    void addTabConnections(qint32 idx);
    void closeEvent(QCloseEvent *event);

private: // tab widgets
    QList< QWidget* >       kitTab;
    QList< QVBoxLayout* >   vLayoutTab;
    QList< QGroupBox* >     hGBoxKitName;
    QList< QHBoxLayout* >   hLayoutName;
    QList< QLabel* >        nameKitLabel;
    QList< QLabel* >        nameKitName;
    QList< QGroupBox* >     hGBoxPathMt4;
    QList< QHBoxLayout* >   hLayoutPath;
    QList< QLabel* >        serverLabel;
    QList< QLabel* >        serverName;
    QList< QLabel* >        pathToMt4Label;
    QList< QLabel* >        pathToMt4Name;
    QList< QHBoxLayout* >   hLayoutConf;
    QList< QGroupBox* >     vGBoxInput;
    QList< QVBoxLayout* >   vLayoutInput;
    QList< QListView* >     inputListView;
    QList< QHBoxLayout* >   hLayoutInputSize;
    QList< QLabel* >        inputLabel;
    QList< QLabel* >        inputSize;
    QList< QVBoxLayout* >   vLayoutSymbol;
    QList< QSpacerItem* >   verticalSpacer_2;
    QList< QLabel* >        arrowLabel;
    QList< QSpacerItem* >   verticalSpacer_3;
    QList< QGroupBox* >     vGBoxOutput;
    QList< QVBoxLayout* >   vLayoutOutput;
    QList< QListView* >     outputListView;
    QList< QHBoxLayout* >   hLayoutOutputSize;
    QList< QLabel* >        outputLabel;
    QList< QLabel* >        outputSize;
    QList< QVBoxLayout* >   vLayoutButtons;
    QList< QPushButton* >   configurationButton;
    QList< QSpacerItem* >   verticalSpacer;
    QList< QProgressBar* >  progressBar;
    QList< QPlainTextEdit* > consoleTextEdit;
    // tab widgets
};

#endif // MAINWINDOW_H
