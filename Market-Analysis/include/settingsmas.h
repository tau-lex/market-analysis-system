#ifndef CONFIGMAS_H
#define CONFIGMAS_H

#include <QObject>

#include "include/settingsstruct.h"

class SettingsMAS : public QObject
{
    Q_OBJECT
public:
    static SettingsMAS &Instance();
private:
    explicit SettingsMAS(QObject *parent = 0);

    //QSettings settings;

signals:
    void saved(QString);
    void loaded(QString);
    void changed(QString);

public slots:
    void load(Settings *settings);
    void save(const Settings *settings);
    //void autosave();
    void load(ConfigMT4 *configKit);
    void save(const ConfigMT4 *configKit);
    //void load(QVector<ConfigMT4 *> &configKitList);
    //void save(const QVector<ConfigMT4 *> &configKitList);

    void deleteMAKit(const QString &kit);
    void renameMAKit(const QString &oldName, const QString &newName);
};

#endif // CONFIGMAS_H
