#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <stdio.h>
#include <QMainWindow>
#include <QDebug>

#include "Service/cameraservice.h"
#include "Service/processservice.h"
#include "Service/paintservice.h"

#include "Connection/mqttconnector.h"
#include "Connection/httpconnector.h"
#include "System/systemutil.h"

#include "Data/redisconnector.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    void initImageTopLeft(QImage image);
    void initImageTopRight(QImage image);
    void initImageBotLeft(QImage image);
    void initImageBotRight(QImage image);

    void updateCpu(double);
    void updateMem(double,double);
    void updateInstuction(QPoint);

    void updateTemp(QString);
    void updateHum(QString);
    void updatePressure(QString);

private slots:
    void on_startButton_clicked();
    void on_stopButton_clicked();

private:
    Ui::MainWindow *ui;
    QImage TopLeft;
    QImage TopRight;
    QImage BotLeft;
    QImage BotRight;

    CameraService *cs;
    ProcessService *ps;
    PaintService *pas;

    MqttConnector *mqtt;
    HttpConnector *http;
    RedisConnector *redis;

    SystemUtil *msys;

    void initImageWidget();
    void initDataManager();
};
#endif // MAINWINDOW_H
