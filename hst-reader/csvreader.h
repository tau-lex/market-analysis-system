#ifndef CSVREADER_H
#define CSVREADER_H

#include <QObject>
#include "imt4reader.h"
#include <QFile>

class CsvReader : public IMt4Reader
{
public:
    CsvReader(QString fName);

private:
    Header* readHeader(QFile &f);
    History* readHistory(QFile &f);

public slots:
    bool readFromFile();
};

#endif // CSVREADER_H
