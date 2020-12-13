#include "paintservice.h"

PaintService::PaintService():canStart(false)
{
    m_timerId=startTimer(1000);
    m_times=0;
}

void PaintService::SetContours(QVector<QVector<QPoint>> points){
    qDebug()<<"Receive contours："<<points.size();
    this->contours.clear();
    this->contours = points;
    this->canStart = true;
}

void PaintService::DrawImage(){
    QPixmap *pix = new QPixmap(280, 280);
    pix->fill(qRgb(0, 0, 0));
    QPainter painter(pix);
    QPen pen(Qt::SolidLine);
    pen.setColor(QColor(255,255,255));
    painter.setPen(pen);
    qDebug()<<"DrawImage";
    for(int i = 0;i<contours.size();i++){
        QPoint last(0,0);
        QPoint sendlast(0,0);
        for(int j=0;j<contours[i].size();j++){
            if(last.x()!=0||last.y()!=0){
                painter.drawLine(last,contours[i][j]);
                if(qAbs(contours[i][j].x()-sendlast.x())+qAbs(contours[i][j].y()-sendlast.y())>5){
                    emit SendContours(contours[i][j]);
                    emit SendInstuctionToUI(contours[i][j]);
                    sendlast.setX(contours[i][j].x());
                    sendlast.setY(contours[i][j].y());
                    if(useSimulator){
                        QThread::sleep(1);
                    }else{
                        QThread::sleep(1);
                    }
                }
                emit SendToUI(pix->toImage());
                //qDebug()<<"PaintService-("<<contours[i][j].x()<<","<<contours[i][j].y()<<") to ("<<last.x()<<","<<last.y()<<")";
            }
            last.setX(contours[i][j].x());
            last.setY(contours[i][j].y());
        }
    }
    this->canStart=false;
}

void PaintService::SendInstruction(){

}

void PaintService::run(){
    while(true){
        //qDebug()<<"Canstart:"<<canStart;
        if(canStart){
            DrawImage();
        }
    }
}

void PaintService::timerEvent(QTimerEvent *event)
{
//    this->image=this->pix.toImage();
//    emit SendToUI(this->image);
}
