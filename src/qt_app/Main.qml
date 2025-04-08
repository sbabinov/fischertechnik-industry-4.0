import QtQuick
import QtQuick.Effects

Window {
    id: root
    width: 480
    height: 800
    visible: true
    title: "Raspberry Pi"

    function translate(keywords) {
        var dictionary = {
            "automatic mode" : ["Авторежим", "Automatic mode", "Automatikbetrieb"],
            "settings" : ["Настройки", "Settings", "Einstellung"],
            "about us" : ["О нас", "About us", "Über uns"]
        }
        if (language.country === "russia") {
            return dictionary[keywords][0]
        } else if (language.country === "usa") {
            return dictionary[keywords][1]
        } else {
            return dictionary[keywords][2]
        }
    }

    Item {
        anchors.fill: parent
        Image {
            anchors.fill: parent
            anchors.bottomMargin: root.height / 10.67
            source: "images/wallpaper.jpg"
        }
    }

    Rectangle {
        id: header
        anchors.top: parent.top
        implicitWidth: root.width
        implicitHeight: root.height / 5
        color: "#e3e3e3"

        Image {
            sourceSize.width: root.width / 1.07
            source: "images/logo.png"
            anchors.centerIn: parent
        }

        Rectangle {
            id: headerShadow
            anchors.top: header.bottom
            width: root.width
            height: root.height / 35
            layer.enabled: true
            layer.smooth: true
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#e3e3e3" }
                GradientStop { position: 0.3; color: "#d9e3e3e3" }
                GradientStop { position: 0.5; color: "#a0e3e3e3" }
                GradientStop { position: 0.7; color: "#60e3e3e3" }
                GradientStop { position: 0.85; color: "#20e3e3e3" }
                GradientStop { position: 0.95; color: "#08e3e3e3" }
                GradientStop { position: 1.0; color: "#00e3e3e3" }
            }
        }
    }

    Rectangle {
        id: footer
        anchors.bottom: parent.bottom
        implicitWidth: root.width
        implicitHeight: root.height / 8
        color: "#e3e3e3"

        Image {
            sourceSize.width: 80
            source: "images/logo1c.png"
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.bottomMargin: 20
        }

        Text {
            text: "2025"
            font.bold: true
            font.family: "Onest"
            font.pointSize: root.height / 45
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 15
        }

        Button {
            id: language
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.rightMargin: 20
            anchors.bottomMargin: 20

            property string country: "russia"

            function setNextCountry() {
                if (language.country === "russia") {
                    language.country = "usa"
                } else if (language.country === "usa") {
                    language.country = "germany"
                } else {
                    language.country = "russia"
                }
            }

            onClicked: {
                setNextCountry()
            }

            background: Image {
                id: flag
                sourceSize.width: 80
                sourceSize.height: 45

                source: "images/" + language.country + ".png"
            }
        }

        Rectangle {
            id: footerShadow
            anchors.bottom: footer.top
            width: root.width
            height: root.height / 35

            layer.enabled: true
            layer.smooth: true
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#00e3e3e3" }
                GradientStop { position: 0.05; color: "#08e3e3e3" }
                GradientStop { position: 0.15; color: "#20e3e3e3" }
                GradientStop { position: 0.3; color: "#60e3e3e3" }
                GradientStop { position: 0.5; color: "#a0e3e3e3" }
                GradientStop { position: 0.7; color: "#d9e3e3e3" }
                GradientStop { position: 1.0; color: "#e3e3e3" }
            }
        }
    }

    Loader {
        id: mainPart
        anchors.top: header.bottom
        anchors.bottom: footer.top
        anchors.left: parent.left
        anchors.right: parent.right
    }
}
