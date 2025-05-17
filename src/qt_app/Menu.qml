import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Effects

Item {
    id: menu

    Loader {
        id: menuHeaderLoader
        source: "Header.qml"
        anchors.top: parent.top
    }

    Image {
        source: "images/logo.png"
        anchors.centerIn: menuHeaderLoader
        sourceSize.width: root.width / 1.07
    }

    ColumnLayout {
        anchors.top: menuHeaderLoader.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: menuFooterLoader.top
        anchors.topMargin: root.height / 20
        anchors.bottomMargin: root.height / 4
        spacing: 30

        Button {
            id: button1
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 30
            }

            Text {
                id: buttonText1
                text: translate("automatic mode")
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }

            onClicked: {
                mainLoader.source = "AutoMode.qml"
            }
        }

        Button {
            id: button2
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 30
            }

            Text {
                id: buttonText2
                text: translate("manual mode")
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }

            onClicked: {
                mainLoader.source = "ManualMode.qml"
            }
        }

        Button {
            id: button3
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 25
            }

            Text {
                id: buttonText3
                text: translate("settings")
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }

            onClicked: {
                mainLoader.source = "Settings.qml"
            }
        }

        Button {
            id: button4
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 25
            }

            Text {
                id: buttonText4
                text: translate("about us")
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }

            onClicked: {
                mainLoader.source = "About.qml"
            }
        }
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
