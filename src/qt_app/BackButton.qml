import QtQuick
import QtQuick.Controls

Button {
    background: Rectangle {
        implicitHeight: root.height / 12
        implicitWidth: root.height / 12
        color: "#b6b6b6"
        radius: root.height / 53
        border.color: "black"
    }

    Text {
        text: "✕"
        anchors.centerIn: parent
        font {
            bold: true
            family: "Onest"
            pointSize: root.height / 25
        }
    }

    onClicked: mainLoader.source = parent.previousPage
}
