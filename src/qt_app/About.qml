import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: about
    anchors.fill: parent
    width: parent.width
    Rectangle {
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        implicitWidth: root.width
        implicitHeight: root.height
        color: "#e3e3e3"
    }

    Flickable
    {
        anchors.fill: parent
        contentWidth: parent.width
        contentHeight: aboutText.height
        clip: true

        Text {
            id: aboutText
            width: about.width - 40
            leftPadding: (about.width - width) / 2
            horizontalAlignment: Text.AlignJustify
            text: "<b>Fischerтех</b> - небольшое приложение для удаленного управления макетом завода Fischertechnik industry 4.0. Макет функционирует благодаря программе на Python - сервера с основной логикой сортировки - и данному приложению, разработанному с помощью фреймворка Qt6 для C++."
            font.family: "Arial"
            font.pointSize: 15
            textFormat: Text.RichText
            wrapMode: Text.Wrap
        }

        Text {
            id: commandHeaderText
            width: about.width
            anchors.top: aboutText.bottom
            anchors.topMargin: 20
            horizontalAlignment: Text.AlignHCenter
            text: "Наша команда:"
            font.family: "Arial"
            font.pointSize: 20
            font.bold: true
        }

        Image {
            source: "images/command.jpeg"
            anchors.top: commandHeaderText.bottom
            anchors.left: parent.left
            anchors.topMargin: 20
            anchors.leftMargin: 20
            sourceSize.width: parent.width - 40
        }
    }
}
