#include "mainwindow.h"
#include "ui_mainwindow.h"
/******************
 * Author： ChongFan
 *
 * 1.Set up MainUI.
 * 2.Create app agent.
 * 3.Create Camera/Process/Paint Service (Thread).
 *****************/

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //set Title
    this->setWindowTitle("CSYE6530-PIOT-GDA-ChongFan");
    initImageWidget();
    initDataManager();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::initDataManager(){
    msys = new SystemUtil();
    connect(msys,SIGNAL(SendCpuToUI(double)),this,SLOT(updateCpu(double)));
    connect(msys,SIGNAL(SendMemToUI(double,double)),this,SLOT(updateMem(double,double)));
    msys->start();
}

void MainWindow::initImageWidget(){
    cs = new CameraService();
    connect(cs, SIGNAL(SendToUI(QImage)), this, SLOT(initImageTopLeft(QImage)));
    cs->start();

    ps = new ProcessService();
    connect(ps, SIGNAL(SendToUI(QImage)), this, SLOT(initImageBotLeft(QImage)));

    pas = new PaintService();
    connect(pas, SIGNAL(SendToUI(QImage)), this, SLOT(initImageBotRight(QImage)));
    connect(pas, SIGNAL(SendInstuctionToUI(QPoint)), this, SLOT(updateInstuction(QPoint)));
    pas->start();

    // ProcessService should send contour points to PaintService
    connect(ps, SIGNAL(SendContours(QVector<QVector<QPoint>>)), pas, SLOT(SetContours(QVector<QVector<QPoint>>)));

    //send step motor instructions by mqtt to cda
    mqtt = new MqttConnector();
    connect(pas, SIGNAL(SendContours(QPoint)), mqtt, SLOT(publishContor(QPoint)));
    connect(mqtt,SIGNAL(SendHumToUI(QString)),this,SLOT(updateHum(QString)));
    connect(mqtt,SIGNAL(SendTempToUI(QString)),this,SLOT(updateTemp(QString)));
    connect(mqtt,SIGNAL(SendPressureToUI(QString)),this,SLOT(updatePressure(QString)));

    http = new HttpConnector();
}

void MainWindow::initImageTopLeft(QImage image){
    //qDebug()<<"initImageTopLeft";
    ui->image1->setPixmap(QPixmap::fromImage(image));
    ui->image1->update();
    TopLeft = image.scaled(280, 280, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
}

void MainWindow::initImageTopRight(QImage image){
    ui->image2->setPixmap(QPixmap::fromImage(image));
    ui->image2->update();
}

void MainWindow::initImageBotLeft(QImage image){
    ui->image3->setPixmap(QPixmap::fromImage(image));
    ui->image3->update();
}

void MainWindow::initImageBotRight(QImage image){
    //qDebug()<<"initImageBotRight";
    ui->image4->setPixmap(QPixmap::fromImage(image));
    ui->image4->update();
}

void MainWindow::on_startButton_clicked()
{
    //qDebug()<<"on_startButton_clicked";
    if(!ui->CB_simulator->isChecked()){
        TopRight = TopLeft;
        ps->setImage(TopRight);
        ps->ProcessImage();
        initImageTopRight(TopRight);
    }else{
        qDebug()<<"use simulator";
        TopRight = QImage(":/new/prefix1/Resource/simulator_image.png").scaled(280, 280, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
        ps->setImage(TopRight);
        ps->ProcessImage();
        pas->useSimulator = true;
        initImageTopRight(TopRight);
    }
    ui->startButton->setEnabled(false);
    ui->stopButton->setEnabled(true);
}

void MainWindow::on_stopButton_clicked()
{
    ui->startButton->setEnabled(true);
    ui->stopButton->setEnabled(false);
}

void MainWindow::updateCpu(double cpu){
    ui->label_cpu->setText("Cpu-  "+QString::number(cpu)+"%");
}

void MainWindow::updateMem(double total,double used){
    ui->label_mem->setText("Memory-  "+QString::number(used)+"/"+QString::number(total));
}

void MainWindow::updateInstuction(QPoint p){
    ui->label_stepmotor->setText("MoveTo-  ("+QString::number(p.x())+","+QString::number(p.y())+")");
}

void MainWindow::updateTemp(QString s){
    ui->label_temp->setText("Temperature-  "+s);
    http->SendToCloud("Temperature",s);
}

void MainWindow::updateHum(QString s){
    ui->label_hum->setText("Humidity-  "+s);
    http->SendToCloud("Humidity",s);
}

void MainWindow::updatePressure(QString s){
    ui->label_pressure->setText("Pressure-  "+s);
    http->SendToCloud("Pressure",s);
}
