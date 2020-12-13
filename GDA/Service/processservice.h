#ifndef PROCESSSERVICE_H
#define PROCESSSERVICE_H
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <stdio.h>
#include <QImage>
#include <QDebug>
#include <math.h>
#include <iostream>
#include "baseservice.h"
//using namespace cv;
using namespace std;
class ProcessService : public QObject , public BaseService
{
    Q_OBJECT
public:
    ProcessService();
    void setImage(QImage image);
    void ProcessImage();
    vector<vector<cv::Point>> contours;
    QVector<QVector<QPoint>> qContours;

signals:
    void SendToUI(QImage image);
    void SendContours(QVector<QVector<QPoint>>);

private:
    QImage Image;
    cv::Mat source;
    cv::Mat result;
};

#endif // PROCESSSERVICE_H
