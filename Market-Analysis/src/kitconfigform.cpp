#include "include/kitconfigform.h"
#include "ui_kitconfigform.h"

KitConfigForm::KitConfigForm(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::KitConfigForm)
{
    ui->setupUi(this);
}

KitConfigForm::~KitConfigForm()
{
    delete ui;
}
