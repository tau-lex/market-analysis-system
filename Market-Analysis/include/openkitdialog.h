#ifndef OPENKITDIALOG_H
#define OPENKITDIALOG_H

#include <QDialog>

namespace Ui {
class OpenKitDialog;
}

class OpenKitDialog : public QDialog
{
    Q_OBJECT

public:
    explicit OpenKitDialog(QWidget *parent = 0);
    ~OpenKitDialog();

    void show(QStringList &list);

signals:
    void openKit(QString);

private slots:
    void on_buttonBox_accepted();

    void on_buttonBox_rejected();

private:
    Ui::OpenKitDialog *ui;
};

#endif // OPENKITDIALOG_H
