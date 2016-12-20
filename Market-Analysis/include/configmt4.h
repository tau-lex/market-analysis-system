#ifndef CONFIGMT4_H
#define CONFIGMT4_H

#include <QObject>
#include <QSettings>

class ConfigMT4 : public QObject
{
    Q_OBJECT
public:
    explicit ConfigMT4(QObject *parent = 0);
    ~ConfigMT4();

public:

signals:

public slots:
};

#endif // CONFIGMT4_H
