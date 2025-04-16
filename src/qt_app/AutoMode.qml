import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Effects

Item {
    id: autoMode
    anchors.fill: parent

    Item {
        anchors.fill: parent
        Image {
            anchors.fill: parent
            anchors.bottomMargin: root.height / 10.67
            source: "images/wallpaper1.jpg"
        }
    }

    Item
    {
        id: automodeHeader
        height: automodeHeaderLoader.height
        width: automodeHeaderLoader.width

        Loader {
            id: automodeHeaderLoader
            source: "Header.qml"
            anchors.top: parent.top
        }

        Loader {
            property string previousPage: "Menu.qml"
            source: "BackButton.qml"
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.topMargin: 10
        }
    }

    Text {
        text: translate("automatic mode")
        anchors.centerIn: automodeHeader
        wrapMode: Text.WordWrap
        width: 200
        font.bold: true
        font.family: "Onest"
        font.pointSize: root.height / 25
        horizontalAlignment: Text.AlignHCenter
    }

    GridLayout {
        anchors.top: automodeHeader.bottom
        anchors.topMargin: root.height / 20
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: menuFooterLoader.top
        anchors.bottomMargin: root.height / 20
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        columns: 3
        rows: 4
        rowSpacing: 5

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#b6b6b6"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "1"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#ffffff"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "2"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#474747"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "3"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#0038a5"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "4"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#b6b6b6"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "5"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#b6b6b6"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "6"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#b6b6b6"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "7"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#D52B1E"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "8"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: root.height / 7
            Layout.preferredWidth: root.height / 7
            color: "#474747"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: "9"
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 30
                anchors.centerIn: parent
            }
        }

        Button {
            Layout.columnSpan: 3
            Layout.alignment: Qt.AlignHCenter

            background: Rectangle {
                implicitHeight: root.height / 12
                implicitWidth: root.width / 1.5
                color: "#e3e3e3"
                radius: 30
                border.color: "black"
                border.width: 2

                Text {
                    text: translate("start")
                    font.bold: true
                    font.family: "Onest"
                    font.pointSize: root.height / 35
                    anchors.centerIn: parent
                }
            }
        }
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
