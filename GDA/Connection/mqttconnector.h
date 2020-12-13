#ifndef MQTTCONNECTOR_H
#define MQTTCONNECTOR_H
#include <QtMqtt/qmqttclient.h>
#include <QJsonObject>
#include <QJsonDocument>
class MqttConnector: public QObject
{
    Q_OBJECT
public:
    MqttConnector();
    QMqttClient* m_client;

public slots:
    void onConnected();
    void publishContor(QPoint);

signals:
    void SendHumToUI(QString);
    void SendTempToUI(QString);
    void SendPressureToUI(QString);

private:
    QJsonObject stringToJson(QString jsonString);
};

#endif // MQTTCONNECTOR_H
