#ifndef PRESENTER_H
#define PRESENTER_H

#include <QObject>
//#include <QMainWindow>
//#include "ui_mainwindow.h"
#include "include/configmas.h"
#include "include/marketassaykit.h"

//namespace Ui {
//class MainWindow;
//}

class Presenter : public QObject
{
    Q_OBJECT
public:
    explicit Presenter(QObject *parent = 0);

private:
    QString defaultKit;
    QStringList listOfKits;
    std::map< QString, MarketAssayKit* > arrayOfKits;

signals:
    void setUiNameTab(QString);

public slots:
    void loadListOfKits();
    void openDefaultTabKit();
    void openTabKit(const QString kit);
    void setupCurrentMAKitUi();

};

#endif // PRESENTER_H
