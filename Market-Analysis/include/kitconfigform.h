#ifndef KITCONFIGFORM_H
#define KITCONFIGFORM_H

#include <QDialog>

namespace Ui {
class KitConfigForm;
}

class KitConfigForm : public QDialog
{
    Q_OBJECT

public:
    explicit KitConfigForm(QWidget *parent = 0);
    ~KitConfigForm();

private:
    Ui::KitConfigForm *ui;
};

#endif // KITCONFIGFORM_H
