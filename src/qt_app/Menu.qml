import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Effects

Item {
    id: menu

    ColumnLayout {
        anchors.fill: parent
        anchors.topMargin: root.height / 20
        anchors.bottomMargin: root.height / 4
        spacing: 30

        Button {
            id: button1
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 7
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 30
            }

            Text {
                id: buttonText1
                text: translate("automatic mode")
                anchors.centerIn: parent
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
            }
        }

        Button {
            id: button2
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 7
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 25
            }

            Text {
                id: buttonText2
                text: translate("settings")
                anchors.centerIn: parent
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
            }
        }

        Button {
            id: button3
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 7
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: 25
            }

            Text {
                id: buttonText3
                text: translate("about us")
                anchors.centerIn: parent
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
            }
        }
    }
}