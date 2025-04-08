import QtQuick

Window {
    id: root
    width: 480
    height: 800
    visible: true
    title: "Raspberry Pi"

    Item {
        anchors.fill: parent
        Image {
            anchors.fill: parent
            anchors.bottomMargin: root.height / 10.67
            source: "images/wallpaper.jpg"
        }
    }

    Rectangle {
        id: header
        anchors.top: parent.top
        implicitWidth: root.width
        implicitHeight: root.height / 5
        color: "#e3e3e3"

        Image {
            sourceSize.width: root.width / 1.07
            source: "images/logo.png"
            anchors.centerIn: parent
        }
    }
}
