#ifndef PAINTSERVICE_H
#define PAINTSERVICE_H
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <stdio.h>
#include <QImage>
#include <QDebug>
#include <QThread>
#include <QTimer>
#include <QPainter>
#include <math.h>
#include <iostream>

#include "baseservice.h"


using namespace cv;
using namespace std;

class PaintService : public QThread, public BaseService
{
    Q_OBJECT
public:
    PaintService();
    void DrawImage();
    void SendInstruction();
    void run();
    bool useSimulator = false;

public slots:
    void SetContours(QVector<QVector<QPoint>> points);

signals:
    void SendToUI(QImage image);
    void SendContours(QPoint);
    void SendInstuctionToUI(QPoint);

private:
    QVector<QVector<QPoint>> contours;
    int m_timerId;
    int m_times;
    bool canStart;

    void timerEvent(QTimerEvent *event);
};

#endif // PAINTSERVICE_H
