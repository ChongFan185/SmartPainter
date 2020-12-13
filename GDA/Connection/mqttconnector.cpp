#include <QDebug>
#include <QVector>
#include <QByteArray>
#include <QtMqtt/qmqtttopicname.h>
#include <QThread>
#include "mqttconnector.h"

MqttConnector::MqttConnector()
{
    QString topic("ProgrammingIoT/ConstrainedDevice/SensorMsg");
    m_client = new QMqttClient();
    m_client->setHostname("192.168.1.158");
    m_client->setPort(1883);
    m_client->setClientId("Csye");
    connect(m_client, &QMqttClient::connected, this, &MqttConnector::onConnected);
    connect(m_client, &QMqttClient::stateChanged, this, [this](QMqttClient::ClientState state){qDebug()<<state;});
    connect(m_client, &QMqttClient::messageReceived, this, [this](const QByteArray &message, const QMqttTopicName &topic) {
        QString s(message);
        //qDebug()<<s;
        QJsonObject tmp = stringToJson(s);
        //qDebug()<<tmp.keys()<<","<<tmp.value("value")<<","<<tmp.value("name");
        if(tmp.value("name").toString().contains("Temp", Qt::CaseInsensitive)){
            emit SendTempToUI(QString::number(tmp.value("value").toDouble()));
        }else if(tmp.value("name").toString().contains("Humidity", Qt::CaseInsensitive)){
            emit SendHumToUI(QString::number(tmp.value("value").toDouble()));
        }else if(tmp.value("name").toString().contains("Pressure", Qt::CaseInsensitive)){
            emit SendPressureToUI(QString::number(tmp.value("value").toDouble()));
        }else{
            qDebug()<<"no data";
        }
    });
    connect(m_client, &QMqttClient::pingResponseReceived, this, [this]() {
        const QString content = QDateTime::currentDateTime().toString()
                    + QLatin1String(" PingResponse")
                    + QLatin1Char('\n');
    });
    m_client->connectToHost();
}

QJsonObject MqttConnector::stringToJson(QString jsonString)
{
    QJsonDocument jsonDocument = QJsonDocument::fromJson(jsonString.toLocal8Bit().data());
    if(jsonDocument.isNull())
    {
        qDebug()<< "String NULL"<< jsonString.toLocal8Bit().data();
    }
    QJsonObject jsonObject = jsonDocument.object();
    return jsonObject;
}

void MqttConnector::onConnected(){
    QString topic("ProgrammingIoT/ConstrainedDevice/SensorMsg");
    auto subscription = m_client->subscribe(topic);
    if (!subscription) {
            qDebug()<<"Could not subscribe. Is there a valid connection?";
    }
}

void MqttConnector::publishContor(QPoint p){
    //qDebug()<<"publishcontor"<<p.x()<<","<<p.y();
    QString topic("ProgrammingIoT/StepMotor/Instruction");
    QString x = QString::number(p.x());
    QString y = QString::number(p.y());
    QString message = x.append(",").append(y);
    m_client->publish(topic, message.toUtf8());
}
