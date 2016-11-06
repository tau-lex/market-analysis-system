#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_findFileButton_clicked()
{
    QString filePath;
    filePath = QFileDialog::getOpenFileName(this, tr("Open .hst file:"), "C:\\", tr("History file (*.hst)"));
    ui->filePathEdit->setText(filePath);
    ui->textBrowser->insertPlainText(filePath);
}
