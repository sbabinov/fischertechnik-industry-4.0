#ifndef PYTHONMANAGER_H
#define PYTHONMANAGER_H

#include <QObject>

class PythonManager : public QObject
{
    Q_OBJECT
public:
    explicit PythonManager(QObject *parent = nullptr);

signals:
};

#endif // PYTHONMANAGER_H
