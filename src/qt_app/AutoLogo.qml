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
}
