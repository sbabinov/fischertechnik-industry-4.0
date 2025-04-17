#include "pythonmanager.h"

PythonManager::PythonManager(QObject* parent) : QObject(parent)
{
    connect(&m_process, &QProcess::readyReadStandardOutput, this, &PythonManager::onPythonOutput);
    connect(&m_process, &QProcess::readyReadStandardError, this, &PythonManager::onPythonError);
    connect(&m_process, QOverload< int, QProcess::ExitStatus >::of(&QProcess::finished), this, &PythonManager::onPythonFinished);
}

void PythonManager::startPythonScript(const QString& scriptPath)
{
    if (m_process.state() == QProcess::NotRunning)
    {
        m_process.start("python", QStringList() << scriptPath);
    }
}

void PythonManager::stopPythonScript()
{
    if (m_process.state() != QProcess::NotRunning)
    {
        m_process.terminate();
    }
}

void PythonManager::sendCommand(const QString& command)
{
    if (m_process.state() == QProcess::Running)
    {
        m_process.write((command + "\n").toUtf8());
    }
}

void PythonManager::onPythonOutput()
{
    QString output = m_process.readAllStandardOutput();
    emit pythonOutputReceived(output);
}

void PythonManager::onPythonError()
{
    QString error = m_process.readAllStandardError();
    emit pythonErrorReceived(error);
}

void PythonManager::onPythonFinished()
{
    emit pythonFinished();
}
