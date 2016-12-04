#ifndef HSTREADER_H
#define HSTREADER_H

#include <QObject>
#include "imt4reader.h"

class HstReader : public IMt4Reader
{
public:
    HstReader(QString fName);

private:
    std::vector<History400*> *historyVector400; // ?

public slots:
    bool readFromFile();
};

#endif // HSTREADER_H
