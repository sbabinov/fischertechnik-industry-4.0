import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: about
    anchors.fill: parent

    Rectangle {
        anchors.fill: parent
        color: "#e3e3e3"
    }

    Item
    {
        id: aboutHeader
        height: aboutHeaderLoader.height
        width: aboutHeaderLoader.width

        Loader {
            id: aboutHeaderLoader
            source: "Header.qml"
            anchors.top: parent.top
        }

        Loader {
            property string previousPage: "Menu.qml"
            source: "BackButton.qml"
            anchors {
                top: parent.top
                right: parent.right
                rightMargin: 10
                topMargin: 10
            }
        }
    }

    Text {
        text: translate("about us")
        anchors.centerIn: aboutHeader
        font {
            bold: true
            family: "Onest"
            pointSize: root.height / 25
        }
        wrapMode: Text.WordWrap
        width: 200
        horizontalAlignment: Text.AlignHCenter
    }

    Flickable
    {
        anchors {
            top: aboutHeader.bottom
            left: parent.left
            right: parent.right
            bottom: menuFooterLoader.top
        }
        contentWidth: parent.width
        contentHeight: aboutSection.height
        clip: true

        Column
        {
            id: aboutSection
            spacing: parent.height * 0.05
            width: parent.width

            Text {
                text: "<b>Fischerтех</b> - небольшое приложение для удаленного управления макетом завода Fischertechnik industry 4.0. Макет функционирует благодаря программе на Python - сервера с основной логикой сортировки - и данному приложению, разработанному с помощью фреймворка Qt6 для C++."
                font {
                    family: "Arial"
                    pixelSize: parent.width * 0.04
                }
                width: parent.width
                leftPadding: parent.width * 0.15 / 2
                rightPadding: parent.width * 0.15 / 2
                horizontalAlignment: Text.AlignJustify
                textFormat: Text.RichText
                wrapMode: Text.Wrap
            }

            Text {
                text: "Наша команда:"
                font {
                    family: "Arial"
                    pixelSize: parent.width * 0.05
                    bold: true
                }
                width: about.width
                horizontalAlignment: Text.AlignHCenter
            }

            Image {
                source: "images/command.jpeg"
                anchors {
                    left: parent.left
                    leftMargin: (parent.width - sourceSize.width) / 2
                }
                sourceSize.width: parent.width - parent.width * 0.15
            }
        }
    }


    Loader {
        id: menuFooterLoader
        source: "Footer.qml"
        anchors.bottom: parent.bottom
    }
}
