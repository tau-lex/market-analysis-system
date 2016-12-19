#include "include/presenter.h"
#include "ui_mainwindow.h"

Presenter::Presenter(QObject *parent) : QObject(parent)
{ }

void Presenter::loadListOfKits()
{
    listOfKits = ConfigMAS::Instance().getListOfKits();
    for( qint32 i = 0; i < listOfKits.size(); i++ )
        arrayOfKits[ listOfKits[i] ] = 0;
}

void Presenter::openDefaultTabKit()
{
    if( listOfKits.size() == 0 )
        this->loadListOfKits();
    if( listOfKits.size() == 0 ) {
        defaultKit = "default";
    } else {
        defaultKit = ConfigMAS::Instance().getDefaultKit();
    }
    this->openTabKit( defaultKit );
}

void Presenter::openTabKit(const QString kit)
{
    arrayOfKits[ kit ] = new MarketAssayKit( kit, this );
    emit setUiNameTab( kit );
}

void Presenter::setupCurrentMAKitUi()
{

}
