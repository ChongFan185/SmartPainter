#include "cameraservice.h"

/******************
 * Author： ChongFan
 *
 * 1.Get rtsp stream.
 * 2.Send the stream to MainUI
 *****************/

CameraService::CameraService()
{
    cap.open(0);
    //cap.open("rtsp://192.168.1.19:554/1/h264major");
    // check if we succeeded
    if (!cap.isOpened()) {
        std::cerr << "ERROR! Unable to open stream\n";
    }
}

CameraService::~CameraService()
{
    delete &cap;
}

void CameraService::run(){
    while(true){
        cap.read(frame);
        this->Image = QImage((const unsigned char*)(frame.data), frame.cols, frame.rows, frame.step, QImage::Format_RGB888);
        emit SendToUI(this->Image);
        //qDebug()<<"CameraService sent a image!";
        //QThread::sleep(1);
    }
}
