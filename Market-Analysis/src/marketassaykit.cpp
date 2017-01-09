#include "include/marketassaykit.h"

MarketAssayKit::MarketAssayKit(QObject *parent, ConfigMT4 *cfg) :
    QObject(parent),
    config(cfg)
{
    setConnections();
    ma_nnWorker.setConfigKit( cfg );
    ma_nnWorker.moveToThread(&maThread);
    maThread.start();
}

MarketAssayKit::~MarketAssayKit()
{
    maThread.exit();
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
