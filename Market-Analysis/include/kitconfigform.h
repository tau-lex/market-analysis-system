#ifndef KITCONFIGFORM_H
#define KITCONFIGFORM_H

#include <QDialog>
#include "include/configmas.h"

namespace Ui {
class KitConfigForm;
}

class KitConfigForm : public QDialog
{
    Q_OBJECT
public:
    explicit KitConfigForm(QWidget *parent = 0);
    ~KitConfigForm();
    void setConfigMt4Ptr(ConfigMT4 *configKit);

private:
    Ui::KitConfigForm *ui;
    ConfigMT4 *configKit;
};

#endif // KITCONFIGFORM_H
