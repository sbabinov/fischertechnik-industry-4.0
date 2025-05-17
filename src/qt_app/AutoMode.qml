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

    Grid {
        anchors.top: automodeHeader.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: startButton.top
        anchors.topMargin: root.height / 20
        anchors.bottomMargin: 20
        anchors.leftMargin: 50
        anchors.rightMargin: 50
        columns: 3
        rows: 3
        spacing: 20

        Repeater {
            model: storageMonitor.storageData
            delegate: Rectangle {
                height: root.height / 7
                width: root.height / 7
                color: {
                    if (modelData.cargo === 1) return "#ffffff";
                    if (modelData.cargo === 2) return "#0038a5";
                    if (modelData.cargo === 3) return "#D52B1E";
                    if (modelData.cargo === 4) return "#b6b6b6";
                    if (modelData.cargo === 5) return "#474747";
                    return "yellow";
                }

                radius: 30
                border.color: "black"
                border.width: 2

                Text {
                    text: index + 1
                    font.bold: true
                    font.family: "Onest"
                    font.pointSize: root.height / 30
                    anchors.centerIn: parent
                }
            }
        }
    }

    Button {
        id: startButton
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
                text: translate("start")
                font.bold: true
                font.family: "Onest"
                font.pointSize: root.height / 35
                anchors.centerIn: parent
            }
        }

        onClicked: networkManager.postRequest("http://127.0.0.1:8000/sort", "")
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
