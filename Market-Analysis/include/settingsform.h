#ifndef SETTINGSFORM_H
#define SETTINGSFORM_H

#include <QDialog>

namespace Ui {
class SettingsForm;
}

class SettingsForm : public QDialog
{
    Q_OBJECT

public:
    explicit SettingsForm(QWidget *parent = 0);
    ~SettingsForm();

private:
    Ui::SettingsForm *ui;
};

#endif // SETTINGSFORM_H
