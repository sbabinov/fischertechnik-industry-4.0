#ifndef NETWORK_MANAGER_HPP
#define NETWORK_MANAGER_HPP

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>

class NetworkManager : public QObject
{
  Q_OBJECT
  Q_PROPERTY(QString response READ response NOTIFY responseChanged)

public:
  explicit NetworkManager(QObject* parent = nullptr);
  QString response() const;

  Q_INVOKABLE void getRequest(const QString &url);
  Q_INVOKABLE void postRequest(const QString &url, const QString &jsonData);

signals:
  void responseChanged(const QString &response);
  void errorOccurred(const QString &error);

private slots:
  void onReplyFinished(QNetworkReply *reply);
private:
  QNetworkAccessManager *manager_;
  QString response_;
};

#endif
