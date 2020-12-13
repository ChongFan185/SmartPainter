#include "redisconnector.h"

RedisConnector::RedisConnector()
{
    redis.connectHost("127.0.0.1");
}

void RedisConnector::save(QString key, QString value){
    redis.set(key,value);
}
