#include <QApplication>
#include <QDir>
#include "include/presenter.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QApplication::setOrganizationName("Terentew Aleksey");
    QApplication::setOrganizationDomain("https://www.mql5.com/ru/users/terentjew23");
    QApplication::setApplicationName("Market Analysis System");
    QApplication::setApplicationVersion("1.1");

    QString mDir = a.applicationDirPath();
    mDir += "/Market Kits";
    if( !QDir().exists(mDir) )
        QDir().mkdir(mDir);

    Presenter p;
    p.openMainWindow();

    return a.exec();
}
