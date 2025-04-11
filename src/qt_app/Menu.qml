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
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }

            onClicked: {
                pageId = 2
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
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
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
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }
        }
    }
}
