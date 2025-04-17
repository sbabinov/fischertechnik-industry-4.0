#ifndef PYTHONMANAGER_H
#define PYTHONMANAGER_H

#include <QProcess>
#include <QObject>

class PythonManager : public QObject
{
    Q_OBJECT

public:
    explicit PythonManager(QObject* parent = nullptr);

    Q_INVOKABLE void startPythonScript(const QString& scriptPath);
    Q_INVOKABLE void stopPythonScript();
    Q_INVOKABLE void sendCommand(const QString& command);

signals:
    void pythonOutputReceived(const QString& output);
    void pythonErrorReceived(const QString& error);
    void pythonFinished();

private slots:
    void onPythonOutput();

    void onPythonError();

    void onPythonFinished();
private:
    QProcess m_process;
};

#endif
