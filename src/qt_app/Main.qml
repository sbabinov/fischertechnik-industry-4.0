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
            "manual mode" : ["Ручной режим", "Manual mode", "Manueller Modus"],
            "settings" : ["Настройки", "Settings", "Einstellung"],
            "about us" : ["О нас", "About us", "Über uns"],
            "start" : ["Старт", "Start", "Start"],
            "save" : ["Сохранить", "Save", "Speichern"],
            "our team" : ["Наша команда:", "Our team:", "Unser Team:"],
            "about" : ["<b>Fischerтех</b> - приложение для удаленного управления макетом завода Fischertechnik industry 4.0. Макет функционирует благодаря программе на Python - сервера с основной логикой - и данному приложению, разработанному с помощью фреймворка Qt6 для C++.",
            "<b>Fischerтех</b> is an application for remote control of the Fischertechnik industry 4.0 factory layout. The layout functions thanks to a Python server program with basic logic and this application developed using the Qt6 framework for C++.",
            "<b>Fischerтех</b> ist eine Anwendung zur Fernsteuerung des Anlagenlayouts von Fischertechnik Industrie 4.0. Das Layout funktioniert dank eines Python-Serverprogramms mit grundlegender Logik - und einer Anwendung, die mit dem Qt6-Framework für C++ entwickelt wurde."]
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
            source: "images/wallpaper.jpg"
            anchors {
                fill: parent
                bottomMargin: root.height / 10.67
            }
        }
    }

    Loader {
        id: mainLoader
        source: "Menu.qml"
        anchors.fill: parent
    }
}
