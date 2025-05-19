#include "storage_monitor.hpp"
#include <QJsonDocument>
#include <QJsonObject>

StorageMonitor::StorageMonitor(NetworkManager* netManager, QObject* parent):
  QObject(parent),
  networkManager_(netManager),
  timer_(new QTimer(this)),
  data_()
{
  connect(timer_, &QTimer::timeout, this, &StorageMonitor::fetchStorageData);
  connect(networkManager_, &NetworkManager::responseChanged, this, &StorageMonitor::handleResponse);
  connect(networkManager_, &NetworkManager::errorOccurred, this, &StorageMonitor::errorOccurred);
  timer_->start(5000);
  fetchStorageData();
}

QJsonArray StorageMonitor::storageData() const
{
  return data_;
}

void StorageMonitor::fetchStorageData()
{
  networkManager_->getRequest("/storage");
}

void StorageMonitor::handleResponse(const QString& response)
{
  parseResponse(response);
}

void StorageMonitor::parseResponse(const QString& response)
{
  QJsonDocument doc = QJsonDocument::fromJson(response.toUtf8());

  if (doc.isArray())
  {
    data_ = doc.array();
    emit dataUpdated();
  }
  else if (doc.isObject())
  {
    QJsonObject obj = doc.object();
    if (obj.contains("storage") && obj["storage"].isArray())
    {
      data_ = obj["storage"].toArray();
      emit dataUpdated();
    }
    else
    {
      emit errorOccurred("Invalid data format");
    }
  }
  else
  {
    emit errorOccurred("Invalid response format");
  }
}
