#ifndef CONFIGMAS_H
#define CONFIGMAS_H

#include <QObject>
#include <QSettings>
#include "include/settingsstruct.h"

class SettingsMAS : public QObject
{
    Q_OBJECT
public:
    static SettingsMAS &Instance();
private:
    explicit SettingsMAS(QObject *parent = 0);
    ~SettingsMAS();
    QSettings *global = 0;
    QSettings *kitFile = 0;

public slots:
    void load(Settings *settings);
    void save(const Settings *settings);
    bool load(ConfigMT4 *configKit);
    void save(const ConfigMT4 *configKit);
    void loadMt4Conf(ConfigMT4 *configKit);
    void saveMt4Conf(const ConfigMT4 *configKit);
    void deleteMAKit(ConfigMT4 *configKit);

private slots:
    void readArray(const QString &arrayName, const QString &valueName,
                   QSettings *setups, QStringList &list);
    void readArray(const QString &arrayName, const QString &valueName,
                   QSettings *setups, QList<qint32> &list);
    void writeArray(const QString &arrayName, const QString &valueName,
                    QSettings *setups, const QStringList &list);
    void writeArray(const QString &arrayName, const QString &valueName,
                    QSettings *setups, const QList<qint32> &list);
    void loadDefault(ConfigMT4 *configKit);
    void clear(void);

signals:
    void saved(QString);
    void loaded(QString);
    void changed(QString);
};

#endif // CONFIGMAS_H
