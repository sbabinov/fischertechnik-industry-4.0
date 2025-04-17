import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Effects

Window {
    id: root
    width: 480
    height: 800
    visible: true
    title: "Raspberry Pi"

    property string language: "russian"

    function translate(keywords) {
        var dictionary = {
            "automatic mode" : ["Авторежим", "Automatic mode", "Automatisch"],
            "settings" : ["Настройки", "Settings", "Einstellung"],
            "about us" : ["О нас", "About us", "Über uns"],
            "start" : ["Старт", "Start", "Start"]
        }
        if (language === "russian") {
            return dictionary[keywords][0]
        } else if (language === "american") {
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

    Loader {
        id: mainLoader
        source: "Menu.qml"
        anchors.fill: parent
    }
}
