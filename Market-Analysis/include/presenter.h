#ifndef PRESENTER_H
#define PRESENTER_H

#include <QObject>
#include <QMap>
#include "include/settingsstruct.h"
#include "include/marketassaykit.h"

class Presenter : public QObject
{
    Q_OBJECT
public:
    explicit Presenter(QObject *parent = 0);
    ~Presenter();

private:
    struct Pair {
        ConfigMT4 *configKit;
        MarketAssayKit *itemKit;
    };
    Settings *settings;
    QMap<QString, Pair *> mapKits;

signals:
    void updatedKit(QString);
    void trainDone(QString);
    void progress(QString, qint32);
    void writeToConsole(QString, QString);
    void error(QString, QString);

public slots:
    QStringList previousSession() const;
    Settings *getSettingsPtr() const;
    ConfigMT4 *getConfigMt4Ptr(const QString nameKit);

    void newMAKit(const QString name);
    void openMAKit(const QString name);
    void saveMAKit(const QString name);
    void loadMAKit(const QString name);
    void deleteMAKit(const QString name);
    void closeMAKit(const QString name);
    void renameMAKit(const QString oldName, const QString newName);
    void runTraining(const QString name);
    void runWork(const QString name);
    void stopWork(const QString name);

private slots:
    void loadKits(const QStringList list);
    void saveKits(const QStringList list);
    void setConnections(const QString name);
    void deleteConnections(const QString name);
};

#endif // PRESENTER_H
