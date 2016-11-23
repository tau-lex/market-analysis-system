#-------------------------------------------------
#
# Project created by QtCreator 2016-10-25T19:08:04
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = hst-reader
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    hstreader.cpp \
    csvreader.cpp

HEADERS  += mainwindow.h \
    hstreader.h \
    csvreader.h

FORMS    += mainwindow.ui
