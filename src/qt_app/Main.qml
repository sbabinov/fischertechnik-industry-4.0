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
}
