#include "httpconnector.h"

HttpConnector::HttpConnector()
{

}

void HttpConnector::SendToCloud(QString name, QString value){
    QNetworkAccessManager *m_pHttpMgr = new QNetworkAccessManager();
    QString url = "https://things.ubidots.com/api/v1.6/devices/csye";
    QNetworkRequest requestInfo;
    requestInfo.setUrl(QUrl(url));
    requestInfo.setHeader(QNetworkRequest::ContentTypeHeader,QVariant("application/json"));
    requestInfo.setRawHeader("Content-Type","application/json");
    requestInfo.setRawHeader("X-Auth-Token","BBFF-tGGNXHuKekWlLjjIKkUKCYpS6gm8bO");

    QByteArray qByteHttpData;
    qByteHttpData.append("{\""+name+"\":"+value+"}");
    qDebug()<<qByteHttpData;
    QNetworkReply *reply =  m_pHttpMgr->post(requestInfo, qByteHttpData);
    QEventLoop eventLoop;
    connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();       //block until finish
    QByteArray responseByte = reply->readAll();
    qDebug()<<responseByte;
}
