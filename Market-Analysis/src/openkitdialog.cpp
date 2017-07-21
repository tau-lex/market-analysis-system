#include "include/openkitdialog.h"
#include "ui_openkitdialog.h"

OpenKitDialog::OpenKitDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::OpenKitDialog)
{
    ui->setupUi(this);
    this->setWindowTitle( tr("Open market kit") );
}

OpenKitDialog::~OpenKitDialog()
{
    delete ui;
}

void OpenKitDialog::show(QStringList &list)
{
    ui->savedKitsLWidget->clear();
    ui->savedKitsLWidget->addItems( list );
    QDialog::show();
}

void OpenKitDialog::on_buttonBox_accepted()
{
    if( ui->savedKitsLWidget->count() > 0 )
        emit openKit( ui->savedKitsLWidget->currentItem()->text() );
}

void OpenKitDialog::on_buttonBox_rejected()
{
    QDialog::close();
}
