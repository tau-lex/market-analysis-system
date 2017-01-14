#ifndef KITCONFIGFORM_H
#define KITCONFIGFORM_H

#include <QDialog>
#include <QAbstractButton>
#include "include/settingsstruct.h"

namespace Ui {
class KitConfigForm;
}

class KitConfigForm : public QDialog
{
    Q_OBJECT
public:
    explicit KitConfigForm(QWidget *parent = 0);
    ~KitConfigForm();

private:
    Ui::KitConfigForm   *ui;
    Settings            *settings;
    ConfigMT4           *configKit;
    QList<qint32>       tempPeriods;

public slots:
    void setSettingsPtr(Settings *sett);
    void setConfigMt4Ptr(ConfigMT4 *config);
    void show(void);

private slots:
    void setUpComboBoxes(void);
    void setUpDinamicComboBoxes(void);
    void updateUi(void);
    void checkTerminalPath(void);
    void on_mt4PathButton_clicked();
    void on_runTerminalButton_clicked();
    void on_addSymbolButton_clicked();
    void on_deleteButton_clicked();
    void on_upButton_clicked();
    void on_downButton_clicked();
    void on_buttonBox_clicked(QAbstractButton *button);
    void save(void);
    bool isReady(void);             //?
    void accept();

signals:
    void updateSymbols(ConfigMT4 *);
    void runTerminalBtn(QString);
    void savedUpd(QString);
    void saved(QString);
};

#endif // KITCONFIGFORM_H
