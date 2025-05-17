#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "network_manager.hpp"
#include "storage_monitor.hpp"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    NetworkManager networkManager;
    StorageMonitor storageMonitor(&networkManager);

    QQmlApplicationEngine engine;
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreationFailed, &app, []() { QCoreApplication::exit(-1); }, Qt::QueuedConnection);

    engine.rootContext()->setContextProperty("networkManager", &networkManager);
    engine.rootContext()->setContextProperty("storageMonitor", &storageMonitor);
    engine.loadFromModule("qt_app", "Main");

    return app.exec();
}
