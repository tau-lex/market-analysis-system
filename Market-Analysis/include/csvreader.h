#ifndef CSVREADER_H
#define CSVREADER_H

#include <QObject>
#include <QFile>
#include "include/imt4reader.h"

class CsvReader : public IMt4Reader
{
public:
    CsvReader(QString fName);

private:
    Header* readHeader(QFile &f);
    std::vector<double> readHistoryLine(QFile &f);

public:
    bool readFile();
};

#endif // CSVREADER_H
