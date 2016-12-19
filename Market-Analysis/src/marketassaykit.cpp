#include "include/marketassaykit.h"

//MarketAssayKit::MarketAssayKit(QObject *parent) : QObject(parent)
//{ }

MarketAssayKit::MarketAssayKit(QString name, QObject *parent) : nameKit(name),
                                                                QObject(parent)
{ }

MarketAssayKit::~MarketAssayKit()
{

}

void MarketAssayKit::setId(const qint32 id)
{
    idKit = id;
}

qint32 MarketAssayKit::getId() const
{
    return idKit;
}

void MarketAssayKit::setName(const QString newName)
{
    nameKit = newName;
}

QString MarketAssayKit::getName() const
{
    return nameKit;
}

void MarketAssayKit::setPathForMt4(const QString path)
{
    // add checking
    pathMt4 = path;
}

QString MarketAssayKit::getPathForMt4() const
{
    return pathMt4;
}
