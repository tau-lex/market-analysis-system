#include "include/mainwindow.h"
#include <QApplication>
#include <QDir>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QApplication::setOrganizationName("Terentew Aleksey");
    QApplication::setOrganizationDomain("https://www.mql5.com/ru/users/terentjew23");
    QApplication::setApplicationName("Market Analysis System");

    QString mDir = a.applicationDirPath();
    mDir += "/Market Kits";
    if(!QDir().exists(mDir))
        QDir().mkdir(mDir);

    MainWindow w;
    w.show();

    return a.exec();
}
