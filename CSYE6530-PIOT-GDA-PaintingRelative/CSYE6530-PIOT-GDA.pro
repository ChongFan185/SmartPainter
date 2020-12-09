QT       += core gui network mqtt
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    Connection/httpconnector.cpp \
    Connection/mqttconnector.cpp \
    Service/baseservice.cpp \
    Service/cameraservice.cpp \
    Service/paintservice.cpp \
    Service/processservice.cpp \
    System/systemutil.cpp \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    Connection/httpconnector.h \
    Connection/mqttconnector.h \
    Service/baseservice.h \
    Service/cameraservice.h \
    Service/paintservice.h \
    Service/processservice.h \
    System/systemutil.h \
    mainwindow.h

FORMS += \
    mainwindow.ui

INCLUDEPATH+= "D:/OpenCV/opencv/build/include"
CONFIG(debug, debug|release): {
    LIBS += -LD:/OpenCV/opencv/build/x64/vc15/lib -lopencv_world440d
} else:CONFIG(release, debug|release): {
    LIBS += -LD:/OpenCV/opencv/build/x64/vc15/lib -lopencv_world440
}

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    resource.qrc
