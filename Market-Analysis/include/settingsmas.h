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
    QSettings *kitConfigFile = 0;

private:
    struct SettingsKeys {
        const QString   globalGr = "Global/";
        const QString   savedKit = globalGr + "Saved_Kits_";
        const QString   savedSize = savedKit + "Size";
        const QString   lastKit = globalGr + "Last_Session_";
        const QString   lastSize = lastKit + "Size";
        const QString   windowGr = "Window/";
        const QString   maxTabs = windowGr + "Max_Tabs";
        const QString   posX = windowGr + "Pos_X";
        const QString   posY = windowGr + "Pos_Y";
        const QString   sizeX = windowGr + "Size_X";
        const QString   sizeY = windowGr + "Size_Y";
    };
    struct KitKeys {
        const QString   mainKitGr;
        const QString   nnKitGr;
        const QString   mt4KitGr;
    };
    SettingsKeys        sKeys;
    KitKeys             kKeys;

public slots:
    void load(Settings *settings);
    void save(const Settings *settings);
    void load(ConfigMT4 *configKit);
    void save(const ConfigMT4 *configKit);
    void deleteMAKit(ConfigMT4 *configKit);

private slots:
    void loadDefault(ConfigMT4 *configKit);

signals:
    void saved(QString);
    void loaded(QString);
    void changed(QString);
};

#endif // CONFIGMAS_H
