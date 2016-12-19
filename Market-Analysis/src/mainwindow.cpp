#include "include/mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    presenter(new Presenter(this))
{
    ui->setupUi(this);

    setConnections();

    presenter->openDefaultTabKit();
}

MainWindow::~MainWindow()
{
    delete ui;
    delete presenter;
}

void MainWindow::openTab()
{

}

void MainWindow::closeTab()
{

}

void MainWindow::setNameTab(QString name)
{
    //ui->nameTab->setText( name );
}

void MainWindow::setConnections()
{
    connect( presenter, SIGNAL(setUiNameTab(QString)), this, SLOT(setNameTab(QString)) );
}

