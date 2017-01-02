#include "include/marketassaykit.h"

#include <QDebug>

MarketAssayKit::MarketAssayKit(QObject *parent) : QObject(parent)
{
    setConnections();
    ma_nnWorker.moveToThread(&maThread);
    maThread.start();
    qDebug()<<"From main thread: "<<QThread::currentThreadId();
}

MarketAssayKit::~MarketAssayKit()
{ }

void MarketAssayKit::setKitPtr(ConfigMT4 *cfg)
{
    config = cfg;
    ma_nnWorker.setConfigKit( cfg );
}

void MarketAssayKit::setConnections()
{
    connect( this, SIGNAL( runTraining() ), &ma_nnWorker, SLOT( runTraining() ) );
    connect( this, SIGNAL( runPrediction() ), &ma_nnWorker, SLOT( runPrediction() ) );
    connect( this, SIGNAL( stop() ), &ma_nnWorker, SLOT( stop() ) );
    connect( &ma_nnWorker, SIGNAL( trained(QString) ), this, SIGNAL( trained(QString) ) );
    connect( &ma_nnWorker, SIGNAL( progress(QString, qint32) ),
             this, SIGNAL( progress(QString, qint32) ) );
    connect( &ma_nnWorker, SIGNAL( message(QString, QString) ),
             this, SIGNAL( message(QString, QString) ) );
}
