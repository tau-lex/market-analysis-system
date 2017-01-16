#ifndef HSTREADER_H
#define HSTREADER_H

#include <QObject>
#include "include/imt4reader.h"

class HstReader : public IMt4Reader
{
public:
    HstReader(QString fName);
    bool readFile();
};

#endif // HSTREADER_H
