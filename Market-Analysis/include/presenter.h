#ifndef PRESENTER_H
#define PRESENTER_H

#include <QObject>
#include <QVector>
#include "include/configmas.h"
#include "include/marketassaykit.h"

class Presenter : public QObject
{
    Q_OBJECT
public:
    explicit Presenter(QObject *parent = 0);

private:
    Settings *settings;
    QVector<ConfigMT4 *> configKitList;
    std::map< QString, MarketAssayKit *> arrayOfKits;

signals:
    void updatedKit(QString);
    void trainDone(QString);
    void progress(QString, qint32);
    void writeToConsole(QString, QString);
    void error(QString, QString);

public slots:
    QStringList previousSession();
    Settings *getSettingsPtr();
    ConfigMT4 *getConfigMt4Ptr(QString nameKit);
    void newMAKit(const QString name);
    void openMAKit(const QString name);
    void saveMAKit(const QString name);
    void deleteMAKit(const QString name);
    void closeMAKit(const QString name);
    void renameMAKit(const QString oldName, const QString newName);
    void runTraining(const QString name);
    void runWork(const QString name);
    void stopWork(const QString name);

private slots:
    void setConnections();
};

#endif // PRESENTER_H
