#ifndef CONFIGMAS_H
#define CONFIGMAS_H

#include <QObject>
#include <QDateTime>
#include <QSettings>

struct Settings {
    qint32      maxOpenTabs;
    QStringList lastSession;
    QStringList listOfKits;
    QString defaultKit = "default";

};

struct ConfigMT4 {
    QString nameKit;
    QString pathMt4;
    QString historyPath; // "\\history\\_SERVER_\\"
    const QString configFile = "\\MQL4\\Files\\mas_mt4.conf";
    const QString newHistoryPath = "\\MQL4\\Files\\MAS_MarketData\\";
    const QString predictionPath = "\\MQL4\\Files\\MAS_Prediction\\";
    QString server;
    //std::list<MT_Tool> input;
    //std::list<MT_Tool> output;
    qint32 depthHistory;
    qint32 depthPrediction = 5;
    QDateTime lastTraining;
    bool isTrained = false;
    bool isRun = false;
    qint32 progress = 0;
};

class ConfigMAS : public QObject
{
    Q_OBJECT
private:
    explicit ConfigMAS(QObject *parent = 0);
public:
    static ConfigMAS &Instance();

private:
    QSettings settings;

signals:
    void saved();
    void loaded();
    void changed();

public slots:
    void load(const Settings *settings);
    void save(const Settings *settings);
    //void autosave();
    void load(const ConfigMT4 *configKit);
    void save(const ConfigMT4 *configKit);
    void load(QVector<ConfigMT4 *> &configKitList);
    void save(const QVector<ConfigMT4 *> &configKitList);

    qint32 addKit(const QString &kit);
    void deleteKit(const QString &kit);
    void renameKit(const QString &oldName, const QString &newName);
    void setDefaultKit(const QString &kit);
    const QString getDefaultKit() const;
    const qint32 getCountOfKits();
    const QStringList getListOfKits();
};

#endif // CONFIGMAS_H
