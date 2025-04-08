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
        contentHeight: aboutSection.height
        clip: true

        Column
        {
            id: aboutSection
            spacing: 20
            width: parent.width
            Text {
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
                width: about.width
                horizontalAlignment: Text.AlignHCenter
                text: "Наша команда:"
                font.family: "Arial"
                font.pointSize: 20
                font.bold: true
            }

            Image {
                source: "images/command.jpeg"
                anchors.left: parent.left
                anchors.leftMargin: 20
                sourceSize.width: parent.width - 40
            }
        }


    }
}
