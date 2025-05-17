#include "network_manager.hpp"

NetworkManager::NetworkManager(QObject *parent):
  QObject(parent)
{
  manager_ = new QNetworkAccessManager(this);
  connect(manager_, &QNetworkAccessManager::finished, this, &NetworkManager::onReplyFinished);
  url_ = "http://127.0.0.1:8000";
}

QString NetworkManager::response() const
{
  return response_;
}

QString NetworkManager::url() const
{
  return url_;
}

void NetworkManager::setUrl(const QString &url)
{
  if (url_ != url)
  {
    url_ = url;
    emit urlChanged(url_);
  }
}

void NetworkManager::getRequest(const QString &url)
{
  QNetworkRequest request(url_ + url);
  manager_->get(request);
}

void NetworkManager::postRequest(const QString &url, const QString &jsonData)
{
  QNetworkRequest request(url_ + url);
  request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
  manager_->post(request, jsonData.toUtf8());
}

void NetworkManager::onReplyFinished(QNetworkReply *reply)
{
  if (reply->error() == QNetworkReply::NoError)
  {
    response_ = QString::fromUtf8(reply->readAll());
    emit responseChanged(response_);
  }
  else
  {
    emit errorOccurred(reply->errorString());
  }
  reply->deleteLater();
}
