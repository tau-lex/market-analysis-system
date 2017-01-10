#ifndef PRESENTER_H
#define PRESENTER_H

#include <QObject>
#include "include/mainwindow.h"
#include "include/settingsform.h"
#include "include/kitconfigform.h"
#include "include/openkitdialog.h"
#include "include/settingsstruct.h"
#include "include/marketassaykit.h"

class Presenter : public QObject
{
    Q_OBJECT
public:
    explicit Presenter(QObject *parent = 0);
    ~Presenter();

private:
    struct Trio {
        ConfigMT4                   *configKit;
        MarketAssayKit              *itemMAKit;
        MainWindow::KitTabWidget    *tabKit;
        Trio(Presenter *parent1 = 0, MainWindow *parent2 = 0, QString name = "");
        ~Trio();
    };
    Settings                *settings;
    QMap<QString, Trio *>   mapKits;
    MainWindow              *mainWindow;
    SettingsForm            *settingsForm;
    KitConfigForm           *kitConfigForm;
    OpenKitDialog           *openKitDialog;
    QString                 currentKit;

public slots:
    void openMainWindow(void);
    void openSettingsForm(void);
    void openKitConfigForm(const QString name);
    void errorMessage(const QString text);
    void setCurrentKit(const QString name);

    void newMAKit(void);
    void openDialog(void);
    void openMAKit(const QString name);
    void closeMAKit(const QString name);
    void renameMAKit(const QString oldName, const QString newName);
    void deleteMAKit(const QString name);
    void runTraining(const QString name);
    void runWork(const QString name);
    void stopWork(const QString name);

private slots:
    void updateTab(const QString name);
    void loadSettings(void);
    void saveSettings(void);
    void loadMAKit(const QString name);
    void saveMAKit(const QString name);
    void updateActionsButtons(const QString name);
    void runTerminal(const QString name);       // ?
    void setConnections(void);
    void setConnections(const QString name);    // ?
    void deleteConnections(const QString name); // ?
    void closeWindow();

signals:
    void updatedKit(QString);
    void trainDone(QString);
    void progress(QString, qint32);
    void writeToConsole(QString, QString);
    void error(QString, QString);
};

#endif // PRESENTER_H
