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
            source: "images/wallpaper1.jpg"
            anchors {
                fill: parent
                bottomMargin: root.height / 10.67
            }
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
            anchors {
                top: parent.top
                right: parent.right
                rightMargin: root.width / 48
                topMargin: root.height / 80
            }
        }
    }

    Text {
        text: translate("automatic mode")
        anchors.centerIn: automodeHeader
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
            top: automodeHeader.bottom
            left: parent.left
            right: parent.right
            bottom: startButton.top
            topMargin: root.height / 20
            bottomMargin: root.height / 40
            leftMargin: root.width / 9.6
            rightMargin: root.width / 9.6
        }
        columns: 3
        rows: 3
        spacing: root.height / 40

        Repeater {
            model: storageMonitor.storageData
            delegate: Rectangle {
                height: root.height / 7
                width: root.width / 4.21
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
        }
    }

    Button {
        id: startButton
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
                text: translate("start")
                anchors.centerIn: parent
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
            }
        }

        onClicked: networkManager.postRequest("/sort", "")
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
