#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QVBoxLayout>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    struct KitTabWidget {
        KitTabWidget(QTabWidget *parent = 0, QString name = "");
        ~KitTabWidget();
        QTabWidget      *parent;
        QString         name;
        QWidget         *kitTab;
        QLabel          *nameKitName;
        QLabel          *serverName;
        QLabel          *pathToMt4Name;
        QListWidget     *inputListView;
        QListWidget     *outputListView;
        QLabel          *inputSize;
        QLabel          *outputSize;
        QPushButton     *configurationButton;
        QPushButton     *trainingButton;
        QPushButton     *workButton;
        QPushButton     *stopButton;
        QPushButton     *deleteButton;
        QProgressBar    *progressBar;
        QPlainTextEdit  *consoleTextEdit;
        QVBoxLayout     *vLayoutTab;
        QGroupBox       *hGBoxKitName;
        QHBoxLayout     *hLayoutName;
        QLabel          *nameKitLabel;
        QGroupBox       *hGBoxPathMt4;
        QHBoxLayout     *hLayoutPath;
        QLabel          *serverLabel;
        QLabel          *pathToMt4Label;
        QHBoxLayout     *hLayoutConf;
        QGroupBox       *vGBoxInput;
        QVBoxLayout     *vLayoutInput;
        QHBoxLayout     *hLayoutInputSize;
        QLabel          *inputLabel;
        QVBoxLayout     *vLayoutSymbol;
        QSpacerItem     *verticalSpacer_2;
        QLabel          *arrowLabel;
        QSpacerItem     *verticalSpacer_3;
        QGroupBox       *vGBoxOutput;
        QVBoxLayout     *vLayoutOutput;
        QHBoxLayout     *hLayoutOutputSize;
        QLabel          *outputLabel;
        QVBoxLayout     *vLayoutButtons;
        QSpacerItem     *verticalSpacer;
        //=======Functions=======
        void rename(const QString newName);
    };

private:
    Ui::MainWindow      *ui;
    qint32              currentTabId = 0;
    qint32              countTabs = 0;

public slots:
    QTabWidget *getTabWidget();
    void updateActions(bool kitActions[5]);
    void addNewTab(const QString name, const KitTabWidget *tab);
    void newTabConnections(const KitTabWidget *tab);
    void deleteTabConnections(const KitTabWidget *tab);

private slots:
    void addNew();
    void open();
    void save();
    void closeTab();
    void openSettings();
    void openKitConfig();
    void runTraining();
    void runWork();
    void stopWork();
    void delete_Kit();
    void openHelp();    // make simple help
    void openAbout();

    void closeTab(const qint32 idx);
    void setCurrentTab(const qint32 idx);
    void setConnections();
    void closeEvent(QCloseEvent *event);

signals:
    void settings();
    void kitConfigs(QString);
    void currentTab(QString);
    void addNewKit();
    void openKit();
    void saveKit(QString);
    void closedKit(QString);
    void renamedKit(QString, QString);
    void deleteKit(QString);
    void runTrainingKit(QString);
    void runWorkKit(QString);
    void stopWorkKit(QString);
    void closeWindow(void);
};

#endif // MAINWINDOW_H
