import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Effects

Item {
    id: manualMode
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
        id: manualmodeHeader
        height: manualmodeHeaderLoader.height
        width: manualmodeHeaderLoader.width

        Loader {
            id: manualmodeHeaderLoader
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
        text: translate("manual mode")
        anchors.centerIn: manualmodeHeader
        wrapMode: Text.WordWrap
        width: 200
        font.bold: true
        font.family: "Onest"
        font.pointSize: root.height / 25
        horizontalAlignment: Text.AlignHCenter
    }

    Grid {
        anchors.top: manualmodeHeader.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: menuFooterLoader.top
        anchors.topMargin: root.height / 13
        anchors.bottomMargin: root.height / 13
        anchors.leftMargin: 50
        anchors.rightMargin: 50
        columns: 3
        rows: 3
        spacing: 20

        Repeater {
            model: storageMonitor.storageData
            delegate: Button {
                height: root.height / 7
                width: root.height / 7
                background: Rectangle {
                    anchors.fill: parent
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

                onClicked: networkManager.postRequest("/process" + "/" + (modelData.row + 1) + "/" + (modelData.col + 1), "")
            }
        }
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
