#ifndef CAMERASERVICE_H
#define CAMERASERVICE_H
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <stdio.h>
#include <QThread>
#include <QImage>
#include <QDebug>

#include "baseservice.h"

class CameraService : public QThread, public BaseService
{
    Q_OBJECT
public:
    CameraService();
    ~CameraService();
    void run();
signals:
    void SendToUI(QImage image);
private:
    QImage Image;
    cv::Mat frame;
    cv::VideoCapture cap;
};

#endif // CAMERASERVICE_H
