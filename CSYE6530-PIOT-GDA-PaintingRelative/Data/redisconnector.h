#ifndef REDISCONNECTOR_H
#define REDISCONNECTOR_H

#include <QObject>
#include "qredis.h"

class RedisConnector:public QObject
{
    Q_OBJECT
public:
    RedisConnector();

    void save(QString, QString);

private:
    QRedis redis;
};

#endif // REDISCONNECTOR_H
