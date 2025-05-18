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
        anchors {
            top: menuHeaderLoader.bottom
            left: parent.left
            right: parent.right
            bottom: menuFooterLoader.top
            topMargin: root.height / 20
            bottomMargin: root.height / 4
        }
        spacing: root.height / 27

        Button {
            id: button1
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: root.height / 27
            }

            Text {
                id: buttonText1
                text: translate("automatic mode")
                anchors.centerIn: parent
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
            }

            onClicked: mainLoader.source = "AutoMode.qml"
        }

        Button {
            id: button2
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: root.height / 27
            }

            Text {
                id: buttonText2
                text: translate("manual mode")
                anchors.centerIn: parent
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
            }

            onClicked: mainLoader.source = "ManualMode.qml"
        }

        Button {
            id: button3
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: root.height / 27
            }

            Text {
                id: buttonText3
                text: translate("settings")
                anchors.centerIn: parent
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
            }

            onClicked: mainLoader.source = "Settings.qml"
        }

        Button {
            id: button4
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 9
                implicitWidth: root.width / 1.2
                color: "#e3e3e3"
                radius: root.height / 27
            }

            Text {
                id: buttonText4
                text: translate("about us")
                anchors.centerIn: parent
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
            }

            onClicked: mainLoader.source = "About.qml"
        }
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
