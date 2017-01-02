#include "include/kitconfigform.h"
#include "ui_kitconfigform.h"
#include <QFile>
#include <QFileDialog>

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

void KitConfigForm::setSettingsPtr(Settings *sett)
{
    settings = sett;
}

void KitConfigForm::setConfigMt4Ptr(ConfigMT4 *config)
{
    configKit = config;
}

void KitConfigForm::show()
{
    updateUi();
    QDialog::show();
}

void KitConfigForm::updateUi()
{
    ui->nameKitEdit->setText( configKit->nameKit );
    ui->mt4PathEdit->setText( configKit->mt4Path );
    checkTerminalPath();
    ui->inputListWidget->addItems( configKit->input );
    ui->outputListWidget->addItems( configKit->output );
    ui->inputCountLEdit->setText( tr("%1 * %2 = %3")
                                  .arg( configKit->input.size() )
                                  .arg( configKit->depthHistory )
                                  .arg( configKit->input.size() *
                                        configKit->depthHistory ) );
    ui->layerCountLEdit->setText( QString("%1").arg( configKit->layersCount ) );
    ui->layersSizeLEdit->setText( tr("%1, %2, %3")
                                  .arg( configKit->layersSize[0] )
                                  .arg( configKit->layersSize[1] )
                                  .arg( configKit->layersSize[2] ) );
    ui->outputCountLEdit->setText( tr("%1 * %2 = %3")
                                   .arg( configKit->output.size() )
                                   .arg( configKit->depthPrediction )
                                   .arg( configKit->output.size() *
                                         configKit->depthPrediction ) );
}

void KitConfigForm::checkTerminalPath()
{
    QDir path( configKit->mt4Path );
    QStringList nameFilter;
    nameFilter << "*.exe";
    QStringList files = path.entryList( nameFilter, QDir::Files );
    QPalette pal = ui->mt4PathEdit->palette();
    if( files.contains( "terminal.exe" ) )
        pal.setColor( QPalette::Text, Qt::darkGreen );
    else
        pal.setColor( QPalette::Text, Qt::darkRed );
    ui->mt4PathEdit->setPalette( pal );
}

void KitConfigForm::on_mt4PathButton_clicked()
{
    configKit->mt4Path = QFileDialog::getExistingDirectory( this,
                                      tr("Open the folder containing the Meta Trader 4:"),
                                      configKit->mt4Path );
    ui->mt4PathEdit->setText( configKit->mt4Path );
    checkTerminalPath();
}

void KitConfigForm::on_addSymbolButton_clicked()
{

}

void KitConfigForm::on_deleteButton_clicked()
{

}

void KitConfigForm::on_upButton_clicked()
{

}

void KitConfigForm::on_downButton_clicked()
{

}

void KitConfigForm::on_buttonBox_clicked(QAbstractButton *button)
{

}
