import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: settings
    anchors.fill: parent

    Rectangle {
        anchors.fill: parent
        color: "#e3e3e3"
    }

    Item
    {
        id: settingsHeader
        height: settingsHeaderLoader.height
        width: settingsHeaderLoader.width

        Loader {
            id: settingsHeaderLoader
            source: "Header.qml"
            anchors.top: parent.top
        }

        Loader {
            property string previousPage: "Menu.qml"
            source: "BackButton.qml"
            anchors {
                top: parent.top
                right: parent.right
                rightMargin: root.width / 48
                topMargin: root.height / 80
            }
        }
    }

    Text {
        text: translate("settings")
        anchors.centerIn: settingsHeader
        font {
            bold: true
            family: "Onest"
            pointSize: root.height / 25
        }
        wrapMode: Text.WordWrap
        width: root.width / 2.4
        horizontalAlignment: Text.AlignHCenter
    }

    TextArea {
        id: httpArea
        text: networkManager.url
        anchors {
            top: settingsHeader.bottom
            right: parent.right
            left: parent.left
        }
        background: Rectangle {
            anchors.fill: parent
            color: "white"
        }
        height: root.height / 8
        placeholderText: "Enter HTTP address"
    }

    Button {
        id: saveButton
        anchors {
            bottom: menuFooterLoader.top
            bottomMargin: root.height / 25
            horizontalCenter: parent.horizontalCenter
        }

        background: Rectangle {
            implicitHeight: root.height / 12
            implicitWidth: root.width / 1.5
            color: "#e3e3e3"
            radius: root.height / 27
            border {
                color: "black"
                width: root.height / 400
            }

            Text {
                text: translate("save")
                anchors.centerIn: parent
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
            }
        }

        onClicked: networkManager.setUrl(httpArea.text)
    }


    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
