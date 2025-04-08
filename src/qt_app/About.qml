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
            leftPadding: 20
            font.family: "Arial"
            font.pointSize: 15
            textFormat: Text.RichText
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignJustify
            text: "<b>Fischerтех</b> - небольшое приложение для удаленного управления макетом завода Fischertechnik industry 4.0. Макет функционирует благодаря программе на Python - сервера с основной логикой сортировки - и данному приложению, разработанному с помощью фреймворка Qt6 для C++."
        }

        Image {
            source: "images/command.jpeg"
            anchors.top: aboutText.bottom
            anchors.left: parent.left
            anchors.topMargin: 20
            anchors.leftMargin: 20
            sourceSize.width: parent.width - 40
        }
    }
}
