#include "include/kitconfigform.h"
#include "ui_kitconfigform.h"
#include <QFile>
#include <QFileDialog>

KitConfigForm::KitConfigForm(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::KitConfigForm)
{
    ui->setupUi(this);
    setUpComboBoxes();
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

void KitConfigForm::show(void)
{
    tempLastChange = configKit->lastChange;
    updateUi();
    QDialog::show();
}

void KitConfigForm::setUpComboBoxes(void)
{
    ui->periodCBox->addItem( "1 min", QString("1") );
    ui->periodCBox->addItem( "5 min", QString("5") );
    ui->periodCBox->addItem( "15 min", QString("15") );
    ui->periodCBox->addItem( "30 min", QString("30") );
    ui->periodCBox->addItem( "1 Hour", QString("60") );
    ui->periodCBox->addItem( "4 Hours", QString("240") );
    ui->periodCBox->addItem( "1 Day", QString("1440") );
    ui->periodCBox->addItem( "1 Week", QString("10080") );
    ui->periodCBox->addItem( "1 Month", QString("43200") );
    ui->periodCBox->setCurrentText( "1 Day" );
}

void KitConfigForm::setUpDinamicComboBoxes(void)
{
    ui->trainingStrategyCBox->clear();
    foreach( QString method, configKit->trainingMethods )
        ui->trainingStrategyCBox->addItem( method, method );
    ui->trainingStrategyCBox->setCurrentText( configKit->trainingMethod );
    ui->symbolCBox->clear();
    foreach( QString symbol, configKit->symbolsOfTime )
        ui->symbolCBox->addItem( QString("time:%1").arg(symbol), symbol );
    foreach( QString symbol, configKit->symbols ) {
        if( symbol.contains(".OQ") || symbol.contains(".N") )
            ui->symbolCBox->addItem( QString("uidx:%1").arg(symbol), symbol );
        else if( symbol.contains(".DE") )
            ui->symbolCBox->addItem( QString("eidx:%1").arg(symbol), symbol );
        else if( symbol.contains("XAU") || symbol.contains("XAG") )
            ui->symbolCBox->addItem( QString("mtls:%1").arg(symbol), symbol );
        else
            ui->symbolCBox->addItem( QString("forx:%1").arg(symbol), symbol );
    }
    if( configKit->symbols.size() )
        ui->symbolCBox->setCurrentText( configKit->symbols[0] );
    else
        ui->symbolCBox->setCurrentText( configKit->symbolsOfTime[0] );
    ui->serverCBox->clear();
    foreach( QString server, configKit->servers )
        ui->serverCBox->addItem( server, server );
    ui->serverCBox->setCurrentText( configKit->server );
}

void KitConfigForm::updateUi(void)
{
    this->setWindowTitle( tr("%1 configuration").arg( configKit->nameKit ) );
    ui->nameKitEdit->setText( configKit->nameKit );
    ui->mt4PathEdit->setText( configKit->mt4Path );
    checkTerminalPath();
    setUpDinamicComboBoxes();
    ui->dataAllocationLEdit->setText( QString("%1%, %2%, %3%")
                                      .arg( configKit->divideInstances[0] )
                                      .arg( configKit->divideInstances[1] )
                                      .arg( configKit->divideInstances[2] ) );
    ui->layerCountLEdit->setText( QString("%1").arg( configKit->layersCount ) );
    ui->layersSizeLEdit->setText( tr("%1,%2,%3,%4,%5,%6,%7,%8,%9,%10")
                                  .arg( configKit->layersSize.at(0) )
                                  .arg( configKit->layersSize.at(1) )
                                  .arg( configKit->layersSize.at(2) )
                                  .arg( configKit->layersSize.at(3) )
                                  .arg( configKit->layersSize.at(4) )
                                  .arg( configKit->layersSize.at(5) )
                                  .arg( configKit->layersSize.at(6) )
                                  .arg( configKit->layersSize.at(7) )
                                  .arg( configKit->layersSize.at(8) )
                                  .arg( configKit->layersSize.at(9) ) );
    tempPeriods = configKit->periods;
    ui->inputListWidget->clear();
    ui->inputListWidget->addItems( configKit->input );
    ui->outputListWidget->clear();
    ui->outputListWidget->addItems( configKit->output );
    ui->recurrentNNChBox->setChecked( configKit->recurrentModel );
    ui->readVolumeChBox->setChecked( configKit->readVolume );
    ui->depthInLEdit->setText( QString("%1").arg( configKit->depthHistory ) );
    ui->inputCountLEdit->setText( QString("%1").arg( configKit->sumInput() ) );
    ui->depthOutLEdit->setText( QString("%1").arg( configKit->depthPrediction ) );
    ui->outputCountLEdit->setText( QString("%1").arg( configKit->sumOutput() ) );
}

void KitConfigForm::checkTerminalPath(void)
{
    QDir path( configKit->mt4Path );
    QStringList nameFilter;
    nameFilter << "*.exe";
    QStringList files = path.entryList( nameFilter, QDir::Files );
    QPalette pal = ui->mt4PathEdit->palette();
    if( files.contains( "terminal.exe" ) && files.contains( "metaeditor.exe" ) ) {
        pal.setColor( QPalette::Text, Qt::darkGreen );
        configKit->updateServerParameters();
        if( configKit->symbols.size() == 0 )
            emit updateSymbols( configKit );
        if( configKit->mt4Account > 0 )
            ui->runTerminalButton->setEnabled( true );
        setUpDinamicComboBoxes();
        copyMqlScripts( configKit->mt4Path );
    } else {
        pal.setColor( QPalette::Text, Qt::darkRed );
        ui->runTerminalButton->setEnabled( false );
    }
    ui->mt4PathEdit->setPalette( pal );
}

void KitConfigForm::copyMqlScripts(QString path)
{
    QFile assist( QString("%1/MQL4/Indicators/MAS_Assistant.ex4").arg( path ) );
    if( !assist.exists() ) {
        QFile::copy( ":/mql/MAS_Assistant.ex4",
                     QString("%1/MQL4/Indicators/MAS_Assistant.ex4").arg( path ) );
        QFile::copy( ":/mql/MAS_Template.tpl",
                     QString("%1/templates/MAS_Template.tpl").arg( path ) );
    }
//    QFile::copy( ":/mql/MAS_Assistant.mq4",
//                 QString("%1/MQL4/Indicators/MAS_Assistant.mq4").arg( path ) );
//    QFile::copy( ":/mql/MAS_Autotrading.mq4",
//                 QString("%1/MQL4/Experts/MAS_Autotrading.mq4").arg( path ) );
//    QFile::copy( ":/mql/MAS_MasterWindows.mqh",
//                 QString("%1/MQL4/Include/MAS_MasterWindows.mqh").arg( path ) );
//    QFile::copy( ":/mql/MAS_Template.tpl",
//                 QString("%1/templates/MAS_Template.tpl").arg( path ) );
}

void KitConfigForm::on_mt4PathButton_clicked()
{
    QString str = "";
    str = QFileDialog::getExistingDirectory( this,
                                             tr("Open the folder containing the Meta Trader 4:"),
                                             configKit->mt4Path );
    if( str != "" ) {
        if( str != configKit->mt4Path )
            tempLastChange = QDateTime::currentDateTime();
        configKit->mt4Path = str;
    }
    ui->mt4PathEdit->setText( configKit->mt4Path );
    checkTerminalPath();
}

void KitConfigForm::on_runTerminalButton_clicked()
{
    emit runTerminalBtn( configKit->nameKit );
}

void KitConfigForm::on_addSymbolButton_clicked()
{
    QString newSymbol;
    newSymbol = ui->symbolCBox->currentData().toString();
    if( !configKit->isTimeSymbol( newSymbol ) )
        newSymbol += ui->periodCBox->currentData().toString();
    if( ui->inputRButton->isChecked() ) {
        ui->inputListWidget->addItem( newSymbol );
    } else if( ui->outputRButton->isChecked() ) {
        ui->outputListWidget->addItem( newSymbol );
    }
    if( !tempPeriods.contains( ui->periodCBox->currentData().toString().toInt() ) )
        tempPeriods.append( ui->periodCBox->currentData().toString().toInt() );
    tempLastChange = QDateTime::currentDateTime();
}

void KitConfigForm::on_deleteButton_clicked()
{
    QListWidget *widget = 0;
    if( ui->inputListWidget->hasFocus() ) {
        widget = ui->inputListWidget;
    } else if( ui->outputListWidget->hasFocus() ) {
        widget = ui->outputListWidget;
    }
    if( widget ) {
        QListWidgetItem* item = widget->currentItem();
        if( item ) {
            delete item;
            tempLastChange = QDateTime::currentDateTime();
        }
    }
    if( ui->inputListWidget->count() == 0 && ui->outputListWidget->count() == 0 )
        tempPeriods.clear();
}

void KitConfigForm::on_upButton_clicked()
{
    QListWidget *widget = 0;
    if( ui->inputListWidget->hasFocus() ) {
        widget = ui->inputListWidget;
    } else if( ui->outputListWidget->hasFocus() ) {
        widget = ui->outputListWidget;
    }
    if( widget ) {
        QListWidgetItem *item = widget->currentItem();
        if( item ) {
            widget->insertItem( (widget->currentRow() - 1), item->text() );
            widget->setCurrentRow( widget->currentRow() - 2 );
            delete item;
            tempLastChange = QDateTime::currentDateTime();
        }
    }
}

void KitConfigForm::on_downButton_clicked()
{
    QListWidget *widget = 0;
    if( ui->inputListWidget->hasFocus() ) {
        widget = ui->inputListWidget;
    } else if( ui->outputListWidget->hasFocus() ) {
        widget = ui->outputListWidget;
    }
    if( widget ) {
        QListWidgetItem *item = widget->currentItem();
        if( item ) {
            widget->insertItem( (widget->currentRow() + 2), item->text() );
            widget->setCurrentRow( widget->currentRow() + 2 );
            delete item;
            tempLastChange = QDateTime::currentDateTime();
        }
    }
}

void KitConfigForm::on_buttonBox_clicked(QAbstractButton *button)
{
    if( QDialogButtonBox::Ok == ui->buttonBox->standardButton(button) ) {
        save();
        this->close();
    }
    if( QDialogButtonBox::Save == ui->buttonBox->standardButton(button) ) {
        save();
        updateUi();
    }
    if( QDialogButtonBox::Cancel == ui->buttonBox->standardButton(button) ) {
    }
}

void KitConfigForm::save(void)
{
    QString oldName = "";
    if( configKit->nameKit != ui->nameKitEdit->text() )
        oldName = configKit->nameKit;
    configKit->rename( ui->nameKitEdit->text() );
    configKit->mt4Path = ui->mt4PathEdit->text();
    if( configKit->server != ui->serverCBox->currentText() ) {
        configKit->server = ui->serverCBox->currentText();
        tempLastChange = QDateTime::currentDateTime();
    }
    configKit->historyPath = QString("/history/%1/").arg( configKit->server );
    configKit->trainingMethod = ui->trainingStrategyCBox->currentText();
    configKit->divideInstances[0] = ui->dataAllocationLEdit->text().mid(0, 2).toInt();
    configKit->divideInstances[1] = ui->dataAllocationLEdit->text().mid(5, 2).toInt();
    configKit->divideInstances[2] = ui->dataAllocationLEdit->text().mid(10, 2).toInt();
    if( configKit->layersCount = ui->layerCountLEdit->text().toInt() ) {
        configKit->layersCount = ui->layerCountLEdit->text().toInt();
        tempLastChange = QDateTime::currentDateTime();
    }
    for( auto i = 0; i < configKit->layersCount; i++ )
        configKit->layersSize[i] = ui->layersSizeLEdit->text().section( ",", i, i).toInt();
    configKit->periods = tempPeriods;
    configKit->input.clear();
    for( qint32 i = 0; i < ui->inputListWidget->count(); i++ )
        configKit->input.append( ui->inputListWidget->item( i )->text() );
    configKit->output.clear();
    for( qint32 i = 0; i < ui->outputListWidget->count(); i++ )
        configKit->output.append( ui->outputListWidget->item( i )->text() );
    configKit->recurrentModel = ui->recurrentNNChBox->isChecked();
    configKit->readVolume = ui->readVolumeChBox->isChecked();
    if( configKit->depthHistory = ui->depthInLEdit->text().toInt() ) {
        configKit->depthHistory = ui->depthInLEdit->text().toInt();
        tempLastChange = QDateTime::currentDateTime();
    }
    if( configKit->depthPrediction = ui->depthOutLEdit->text().toInt() ) {
        configKit->depthPrediction = ui->depthOutLEdit->text().toInt();
        tempLastChange = QDateTime::currentDateTime();
    }
    configKit->lastChange = tempLastChange;
    if( configKit->lastChange > configKit->lastTraining )
        configKit->isTrained = false;
    configKit->isReady = isReady();
    if( oldName == "" ) {
        emit savedUpd( configKit->nameKit );
        emit saved( configKit->nameKit );
    } else {
        emit savedUpd( oldName );
        emit saved( configKit->nameKit );
    }
}

bool KitConfigForm::isReady(void)
{
    if( configKit->mt4Path.size() > 5 &&
            configKit->historyPath.size() > 10 &&
            configKit->historyPath.contains( configKit->server ) &&
            configKit->input.size() > 0 &&
            configKit->output.size() > 0 &&
            configKit->depthHistory > 0 &&
            configKit->depthPrediction > 0 )
        return true;
    return false;
}

void KitConfigForm::accept()
{

}
