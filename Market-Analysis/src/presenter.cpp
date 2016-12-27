#include "include/presenter.h"
#include "include/mainwindow.h"

Presenter::Presenter(QObject *parent) : QObject(parent)
{
    ConfigMAS::Instance().load( settings );
    ConfigMAS::Instance().load( configKitList );

    setConnections();
}

QStringList Presenter::previousSession()
{
    QStringList lastSession;
    //lastSession = settings->lastSession;
    lastSession.append( settings->defaultKit );
    return lastSession;
}

Settings *Presenter::getSettingsPtr()
{
    return settings;
}

ConfigMT4 *Presenter::getConfigMt4Ptr(QString nameKit)
{
    return configKitList[0];
}

void Presenter::newMAKit(const QString name)
{

}

void Presenter::openMAKit(const QString name)
{

}

void Presenter::saveMAKit(const QString name)
{

}

void Presenter::deleteMAKit(const QString name)
{

}

void Presenter::closeMAKit(const QString name)
{

}

void Presenter::renameMAKit(const QString oldName, const QString newName)
{

}

void Presenter::runTraining(const QString name)
{

}

void Presenter::runWork(const QString name)
{

}

void Presenter::stopWork(const QString name)
{

}

void Presenter::setConnections()
{
}
