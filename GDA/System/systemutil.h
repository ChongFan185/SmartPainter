#ifndef SYSTEMUTIL_H
#define SYSTEMUTIL_H

#include <QThread>
//#include "mysysinfo.h"

class SystemUtil : public QThread
{
    Q_OBJECT
public:
    SystemUtil();
    void run() override;

signals:
    void SendCpuToUI(double);
    void SendMemToUI(double,double);

private:
    //MySysInfo* info;
};

#endif // SYSTEMUTIL_H
