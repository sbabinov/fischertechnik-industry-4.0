#ifndef NETWORK_MANAGER_HPP
#define NETWORK_MANAGER_HPP

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>

class NetworkManager: public QObject
{
  Q_OBJECT
  Q_PROPERTY(QString response READ response NOTIFY responseChanged)
  Q_PROPERTY(QString url READ url WRITE setUrl NOTIFY urlChanged)

public:
  explicit NetworkManager(QObject* parent = nullptr);
  QString response() const;
  QString url() const;

  Q_INVOKABLE void setUrl(const QString &url);
  Q_INVOKABLE void getRequest(const QString& url);
  Q_INVOKABLE void postRequest(const QString& url, const QString& jsonData);

signals:
  void responseChanged(const QString& response);
  void errorOccurred(const QString& error);
  void urlChanged(const QString& url);

private slots:
  void onReplyFinished(QNetworkReply* reply);
private:
  QNetworkAccessManager* manager_;
  QString response_;
  QString url_;
};

#endif
