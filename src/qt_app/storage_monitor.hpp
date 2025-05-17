#ifndef STORAGE_MONITOR_HPP
#define STORAGE_MONITOR_HPP

#include <QObject>
#include <QTimer>
#include <QJsonArray>
#include "network_manager.hpp"

class StorageMonitor : public QObject
{
  Q_OBJECT
  Q_PROPERTY(QJsonArray storageData READ storageData NOTIFY dataUpdated)

public:
  explicit StorageMonitor(NetworkManager* netManager, QObject* parent = nullptr);
  QJsonArray storageData() const;

public slots:
  void fetchStorageData();

signals:
  void dataUpdated();
  void errorOccurred(const QString &message);

private slots:
  void handleResponse(const QString &response);

private:
  NetworkManager* networkManager_;
  QTimer* timer_;
  QJsonArray data_;
  void parseResponse(const QString &response);
};

#endif
