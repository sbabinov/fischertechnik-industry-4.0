import QtQuick
import QtQuick.Controls

Rectangle {
    id: footer
    anchors.bottom: parent.bottom
    implicitWidth: root.width
    implicitHeight: root.height / 8
    color: "#e3e3e3"

    Image {
        source: "images/logo1c.png"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.leftMargin: root.width / 24
        anchors.bottomMargin: root.height / 40
        sourceSize.width: root.width / 6
        sourceSize.height: root.height / 18
    }

    Text {
        text: "2025"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: root.height / 53
        font.bold: true
        font.family: "Onest"
        font.pointSize: root.height / 45
    }

    Button {
        id: language
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.rightMargin: root.width / 24
        anchors.bottomMargin: root.height / 40

        function setNextLanguage() {
            if (root.language === "russian") {
                root.language = "american"
            } else if (root.language === "american") {
                root.language = "german"
            } else {
                root.language = "russian"
            }
        }

        onClicked: {
            setNextLanguage()
        }

        background: Image {
            id: flag
            source: "images/" + root.language + ".png"
            sourceSize.width: root.width / 6
            sourceSize.height: root.height / 18
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
