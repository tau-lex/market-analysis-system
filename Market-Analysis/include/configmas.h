#ifndef CONFIGMAS_H
#define CONFIGMAS_H

#include <QObject>

class ConfigMAS : public QObject
{
    Q_OBJECT
public:
    explicit ConfigMAS(QObject *parent = 0);

signals:

public slots:
};

#endif // CONFIGMAS_H