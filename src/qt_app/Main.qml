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

        Rectangle {
            id: headerShadow
            anchors.top: header.bottom
            width: root.width
            height: root.height / 35
            layer.enabled: true
            layer.smooth: true
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#e3e3e3" }
                GradientStop { position: 0.3; color: "#d9e3e3e3" }
                GradientStop { position: 0.5; color: "#a0e3e3e3" }
                GradientStop { position: 0.7; color: "#60e3e3e3" }
                GradientStop { position: 0.85; color: "#20e3e3e3" }
                GradientStop { position: 0.95; color: "#08e3e3e3" }
                GradientStop { position: 1.0; color: "#00e3e3e3" }
            }
        }
    }

    Rectangle {
        id: footer
        anchors.bottom: parent.bottom
        implicitWidth: root.width
        implicitHeight: root.height / 8
        color: "#e3e3e3"
    }
}
