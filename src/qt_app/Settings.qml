import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: settings
    anchors.fill: parent

    property var myArray: [1, 1, 1, 1, 1, 1, 1, 1, 1]

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

    Flickable
    {
        anchors {
            top: settingsHeader.bottom
            left: parent.left
            right: parent.right
            bottom: saveButton.top
            bottomMargin: root.height / 40
        }
        contentWidth: parent.width
        contentHeight: settingsSection.height
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        boundsMovement: Flickable.StopAtBounds

        Column
        {
            id: settingsSection
            spacing: parent.height * 0.025
            width: parent.width

            Text {
                id: httpAddress
                text: translate("http address")
                anchors.horizontalCenter: parent.horizontalCenter
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 30
                }
            }

            TextArea {
                id: httpArea
                text: networkManager.url
                anchors {
                    topMargin: root.height / 80
                    right: parent.right
                    left: parent.left
                }
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 35
                }
                background: Rectangle {
                    anchors.fill: parent
                    color: "white"
                }
                height: root.height / 8
                wrapMode: Text.WordWrap
                placeholderText: translate("http placeholder")
            }

            Text {
                id: storageState
                text: translate("storage state")
                anchors.horizontalCenter: parent.horizontalCenter
                font {
                    bold: true
                    family: "Onest"
                    pointSize: root.height / 30
                }
            }

            Grid {
                anchors {
                    left: parent.left
                    right: parent.right
                    leftMargin: root.width / 9.6
                    rightMargin: root.width / 9.6
                }
                columns: 3
                rows: 3
                spacing: root.height / 40

                Repeater {
                    id: writeMatrix
                    model: myArray
                    delegate: Button {
                        height: root.height / 7
                        width: root.width / 4.21
                        background: Rectangle {
                            anchors.fill: parent
                            color: {
                                if (modelData === 1) return "#ffffff";
                                if (modelData === 2) return "#0038a5";
                                if (modelData === 3) return "#D52B1E";
                                if (modelData === 4) return "#b6b6b6";
                                if (modelData === 5) return "#474747";
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

                        onClicked: {
                            if (myArray[index] !== 5) {
                                var newArray = myArray;
                                ++newArray[index];
                                myArray = newArray;
                            }
                            else {
                                var newArray = myArray;
                                newArray[index] = 1;
                                myArray = newArray;
                            }
                        }
                    }
                }
            }
        }
    }

    Button {
        id: saveButton
        anchors {
            bottom: menuFooterLoader.top
            bottomMargin: root.height / 50
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

        onClicked: {
            networkManager.setUrl(httpArea.text);
            const array = myArray
            const matrix = [];
            const size = 3;
            for (let i = 0; i < array.length; i += size) {
                matrix.push(array.slice(i, i + size));
            }
            const result = `[${matrix.map(row => `[${row.join(',')}]`).join(',')}]`;
            networkManager.postRequest("/write" + "/" + result, "")
        }
    }

    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
