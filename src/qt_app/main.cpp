#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "pythonmanager.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    PythonManager pythonManager;
    pythonManager.startPythonScript("../fischertechnik-industry-4-0/main.py");

    QQmlApplicationEngine engine;
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.rootContext()->setContextProperty("pythonManager", &pythonManager);
    engine.loadFromModule("qt_app", "Main");

    return app.exec();
}
