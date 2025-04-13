import QtQuick
import QtQuick.Controls

Button {
    background: Rectangle {
        implicitHeight: root.height / 12
        implicitWidth: root.height / 12
        color: "#b6b6b6"
        radius: 15
        border.color: "black"
    }

    Text {
        text: "✕"
        anchors.centerIn: parent
        font.bold: true
        font.family: "Onest"
        font.pointSize: root.height / 25
    }

    onClicked: {
        mainLoader.source = parent.previousPage
    }
}
