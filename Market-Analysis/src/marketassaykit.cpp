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
    maThread.wait();
}

void MarketAssayKit::setConnections()
{
    connect( this, SIGNAL( runTraining() ), &ma_nnWorker, SLOT( runTraining() ) );
    connect( this, SIGNAL( runPrediction() ), &ma_nnWorker, SLOT( runPrediction() ) );
    connect( this, SIGNAL( stop() ), &ma_nnWorker, SLOT( stop() ) );
    connect( &ma_nnWorker, SIGNAL( trained() ), this, SLOT( trained() ) );
    connect( &ma_nnWorker, SIGNAL( progress(qint32) ), this, SLOT( progress(qint32) ) );
    connect( &ma_nnWorker, SIGNAL( message(QString) ), this, SLOT( message(QString) ) );
    connect( &ma_nnWorker, SIGNAL( pause(qint32) ), this, SLOT( pause(qint32) ) );
}

void MarketAssayKit::trained()
{
    emit trained( config->nameKit );
}

void MarketAssayKit::progress(qint32 proc)
{
    config->progress = proc;
    emit progress( config->nameKit );
}

void MarketAssayKit::message(QString text)
{
    emit message( config->nameKit, text );
}

void MarketAssayKit::pause(qint32 msec)
{
    maThread.wait( msec );
    emit message( config->nameKit, "MAK Pause." );
}
