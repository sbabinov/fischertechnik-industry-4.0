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
            font.pointSize: 30
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignJustify
            text: "Продолжаю перевод книги John Torjo «Boost.Asio C++ Network Programming». Вторая глава получилась большая, поэтому разобью ее на две части. В этой части мы поговорим именно про основы Boost.Asio, а во второй части речь пойдет про асинхронное программирование."
        }
    }
}
