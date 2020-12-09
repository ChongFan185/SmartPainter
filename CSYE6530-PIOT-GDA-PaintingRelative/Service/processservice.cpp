#include "processservice.h"

/******************
 * Author： ChongFan
 *
 * 1.Receive an image from MainUI.
 * 2.Process the image
 * 3.Send signal to MainUI with result.
 *****************/

ProcessService::ProcessService()
{

}

void ProcessService::setImage(QImage image){
    this->Image = image;
}

void ProcessService::ProcessImage(){

    int threshold_value = 0;
    int threshold_type = 3;
    int const max_value = 255;
    int const max_type = 4;
    int const max_binary_value = 255;

    contours.clear();
    source = cv::Mat(this->Image.height(), this->Image.width(), CV_8UC3, (void*)this->Image.constBits(), this->Image.bytesPerLine());
    //threshold(source, source, threshold_value, max_binary_value,0 );
    result = cv::Mat::zeros(source.rows, source.cols, CV_8UC3);
    source = source >80;
    cvtColor(source, source, cv::COLOR_BGR2GRAY);
    vector<cv::Vec4i> hierarchy;
    findContours( source, contours, hierarchy, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE );
    int idx = 0;
    for( ; idx >= 0; idx = hierarchy[idx][0] )
    {
        //qDebug()<<"idx:"<<idx;
        cv::Scalar color( 255, 255, 255 );
        drawContours( result, contours, idx, color, cv::LINE_4, 0, hierarchy );
    }

    this->Image = QImage((const unsigned char*)(result.data), result.cols, result.rows, result.step, QImage::Format_RGB888);
    emit SendToUI(this->Image);

    qContours.clear();
    for(int i = 0;i<contours.size();i++){
        QVector<QPoint> line;
        for(int j=0;j<contours[i].size();j++){
            qDebug()<<"x:"<<contours[i][j].x<<"y:"<<contours[i][j].y;
            QPoint *tmpP = new QPoint(contours[i][j].x,contours[i][j].y);
            line.append(*tmpP);
        }
        qContours.append(line);
    }
    qDebug()<<"size:"<<qContours.size();
    emit SendContours(this->qContours);
}
