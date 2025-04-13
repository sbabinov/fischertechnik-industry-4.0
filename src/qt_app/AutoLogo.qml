import QtQuick
import QtQuick.Controls.Basic

Item {
    Text {
        text: translate("automatic mode")
        anchors.centerIn: parent
        wrapMode: Text.WordWrap
        width: 200
        font.bold: true
        font.family: "Onest"
        font.pointSize: root.height / 25
        horizontalAlignment: Text.AlignHCenter
    }

    Button {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.rightMargin: 10
        anchors.topMargin: 10
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
            pageId = 1
        }
    }
}
