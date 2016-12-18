#ifndef CONFIGMAS_H
#define CONFIGMAS_H

#include <QObject>
#include <QSettings>

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
    void load();
    void save();
    void autosave();
    qint32 addKit(const QString &kit);
    void deleteKit(const QString &kit);
    void renameKit(const QString &oldName, const QString &newName);
    void setDefaultKit(const QString &kit);
    const QString getDefaultKit() const;
    const qint32 getCountOfKits();
    const QStringList getListOfKits();
};

#endif // CONFIGMAS_H
