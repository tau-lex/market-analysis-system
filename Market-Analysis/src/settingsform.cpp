#include "include/settingsform.h"
#include "ui_settingsform.h"

SettingsForm::SettingsForm(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::SettingsForm)
{
    ui->setupUi(this);
    this->setWindowTitle( tr("Program settings") );
}

SettingsForm::~SettingsForm()
{
    delete ui;
}

void SettingsForm::setSettingsPtr(Settings *sett)
{
    settings = sett;
}
