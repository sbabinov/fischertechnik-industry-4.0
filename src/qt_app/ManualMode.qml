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
            source: "images/wallpaper1.jpg"
            anchors {
                fill: parent
                bottomMargin: root.height / 10.67
            }
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
            anchors {
                top: parent.top
                right: parent.right
                rightMargin: root.width / 48
                topMargin: root.height / 80
            }
        }
    }

    Text {
        text: translate("manual mode")
        anchors.centerIn: manualmodeHeader
        font {
            bold: true
            family: "Onest"
            pointSize: root.height / 25
        }
        wrapMode: Text.WordWrap
        width: root.width / 2.4
        horizontalAlignment: Text.AlignHCenter
    }

    Grid {
        anchors {
            top: manualmodeHeader.bottom
            left: parent.left
            right: parent.right
            bottom: menuFooterLoader.top
            topMargin: root.height / 13
            bottomMargin: root.height / 13
            leftMargin: root.width / 9.6
            rightMargin: root.width / 9.6
        }
        columns: 3
        rows: 3
        spacing: root.height / 40

        Repeater {
            model: storageMonitor.storageData
            delegate: Button {
                height: root.height / 7
                width: root.width / 4.21
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
                    radius: root.height / 27
                    border {
                        color: "black"
                        width: root.height / 400
                    }

                    Text {
                        text: index + 1
                        anchors.centerIn: parent
                        font {
                            bold: true
                            family: "Onest"
                            pointSize: root.height / 30
                        }
                    }
                }

                onClicked: networkManager.postRequest("/process" + "/" + (modelData.row) + "/" + (modelData.col), "")
            }
        }
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
