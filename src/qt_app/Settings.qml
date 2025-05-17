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
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.topMargin: 10
        }
    }

    Text {
        text: translate("settings")
        anchors.centerIn: settingsHeader
        wrapMode: Text.WordWrap
        width: 200
        font.bold: true
        font.family: "Onest"
        font.pointSize: root.height / 25
        horizontalAlignment: Text.AlignHCenter
    }

    TextArea {
        id: httpArea
        background: Rectangle {
            anchors.fill: parent
            color: "white"
        }

        text: networkManager.url

        anchors.top: settingsHeader.bottom
        height: 100
        anchors.right: parent.right
        anchors.left: parent.left
        placeholderText: "Enter HTTP address"
    }

    Button {
        id: saveButton
        anchors.bottom: menuFooterLoader.top
        anchors.bottomMargin: root.height / 25
        anchors.horizontalCenter: parent.horizontalCenter

        background: Rectangle {
            implicitHeight: root.height / 12
            implicitWidth: root.width / 1.5
            color: "#e3e3e3"
            radius: 30
            border.color: "black"
            border.width: 2

            Text {
                text: translate("save")
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
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
