#ifndef HTTPCONNECTOR_H
#define HTTPCONNECTOR_H
#include <QObject>
#include <QNetworkAccessManager>
#include <QEventLoop>
#include <QNetworkReply>

class HttpConnector: public QObject
{
    Q_OBJECT
public:
    HttpConnector();
    void SendToCloud(QString name, QString value);

};

#endif // HTTPCONNECTOR_H
