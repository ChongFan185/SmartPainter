#include "systemutil.h"

SystemUtil::SystemUtil(){
    //info = new MySysInfo();
}

void SystemUtil::run(){
    double cpu,mem_use,mem_total;
    while(true){
        //info->GetCpuUsage(cpu);
        //info->GetMemUsage(mem_total,mem_use);
        emit SendCpuToUI(qrand()%10+50);
        double a = double(qrand()%10)/10;
        emit SendMemToUI(15.8, a+3);
        QThread::sleep(1);
    }
}
