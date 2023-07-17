import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components


Components.ListItem{

    id: listBellItem
    property string bellId
    property string bellCron
    property bool bellMo
    property bool bellTu
    property bool bellWe
    property bool bellTh
    property bool bellFr
    property string bellValidity
    property bool bellValidityActivated
    property string bellImg
    property string bellName
    property string bellSound
    property bool bellActivated
    property string metaInfo
    property bool isSoundError
    property bool isImgError

    enabled:true

    onContainsMouseChanged: {
        if (!optionsMenu.activeFocus){
            if (containsMouse) {
                listBells.currentIndex = index
            }else {
                listBells.currentIndex = -1
            }
        }

    }

    Rectangle {
        height:visible?140:0
        width:parent.width
        color:{
            if (isSoundError || isImgError){
                "#ffa64c"
            }else{
                "transparent"
            }
        }
        border.color: "transparent"
        Item{
            id: menuItem
            height:visible?140:0
            width:listBellItem.width-manageBellBtn.width
            
            Column{
                id:cronRow
                anchors.verticalCenter: parent.verticalCenter
                width:190
                anchors.leftMargin:5
                Text{
                    id:timeText
                    text:bellCron
                    font.family: "Quattrocento Sans Bold"
                    color:"#3366cc"
                    font.pointSize: 44
                    anchors.horizontalCenter:parent.horizontalCenter
                }
                Row{
                    id:dayRow
                    anchors.horizontalCenter: parent.horizontalCenter
                    spacing:5
                    Text{
                        id:moText
                        text:i18nd("bell-scheduler","M")
                        font.family:"Quattrocento Sans Bold"
                        color:bellMo? "#3366cc":"#A0A0A0"
                        font.pointSize:18
                    }
                    Text{
                        id:tuText
                        text:i18nd("bell-scheduler","T")
                        font.family:"Quattrocento Sans Bold"
                        color:bellTu? "#3366cc":"#A0A0A0"
                        font.pointSize:18
                    }
                    Text{
                        id:weText
                        text:i18nd("bell-scheduler","W")
                        font.family:"Quattrocento Sans Bold"
                        color:bellWe? "#3366cc":"#A0A0A0"
                        font.pointSize:18
                    }
                    Text{
                        id:thText
                        text:i18nd("bell-scheduler","R")
                        font.family:"Quattrocento Sans Bold"
                        color:bellTh? "#3366cc":"#A0A0A0"
                        font.pointSize:18
                    }
                    Text{
                        id:frText
                        text:i18nd("bell-scheduler","F")
                        font.family:"Quattrocento Sans Bold"
                        color:bellFr? "#3366cc":"#A0A0A0"
                        font.pointSize:18
                    }
                }
                Text{
                    id:validityText
                    text:bellValidity
                    font.family:"Quattrocento Sans Bold"
                    color:bellFr? "#3366cc":"#A0A0A0"
                    font.pointSize:11
                    visible:bellValidityActivated?true:false
                    anchors.horizontalCenter:parent.horizontalCenter
                }
            }
            Image{
                id:bellImage
                width:80
                height:80
                fillMode:Image.PreserveAspectFit
                source:bellImg
                anchors.verticalCenter:parent.verticalCenter
                anchors.left:cronRow.right
                anchors.leftMargin:30
            }
            Column{
                id:bellDescription
                anchors.verticalCenter:parent.verticalCenter
                anchors.left:bellImage.right
                anchors.leftMargin:30
                spacing:10
                width:{
                    if (listBellItem.ListView.isCurrentItem){
                        parent.width-(bellState.width+manageBellBtn.width+380)
                    }else{
                        parent.width-(bellState.width+360)
                    }
                }
               
                Text{
                    id:nameText
                    text:bellName
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 18
                    horizontalAlignment:Text.AlignLeft
                    elide:Text.ElideMiddle
                    width:parent.width
                }

                Text{
                    id:soundText
                    text:bellSound
                    font.family:isSoundError?"Quattrocento Sans Italic":"Quattrocento Sans Bold"
                    font.pointSize: 11
                    horizontalAlignment:Text.AlignLeft
                    elide:Text.ElideMiddle
                    width:parent.width
                }

            }

            Image{
                id:bellState
                source:bellActivated?"/usr/share/icons/breeze/status/24/audio-on.svg":"/usr/share/icons/breeze/status/24/audio-volume-muted.svg"
                sourceSize.width:32
                sourceSize.height:32
                anchors.left:bellDescription.right
                anchors.verticalCenter:parent.verticalCenter
                anchors.leftMargin:30
            }
            
            Button{
                id:manageBellBtn
                display:AbstractButton.IconOnly
                icon.name:"configure.svg"
                anchors.leftMargin:15
                anchors.left:bellState.right
                anchors.verticalCenter:parent.verticalCenter
                visible:listBellItem.ListView.isCurrentItem
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("bell-scheduler","Click to manage this bell")
                /*onClicked:onedriveBridge.loadSpace(idSpace)*/
                onClicked:optionsMenu.open();
                onVisibleChanged:{
                    optionsMenu.close()
                }

                Menu{
                    id:optionsMenu
                    y: manageBellBtn.height
                    x:-(optionsMenu.width-manageBellBtn.width/2)

                    MenuItem{
                        icon.name:bellActivated?"audio-volume-muted.svg":"audio-on.svg"
                        text:bellActivated?i18nd("bell-scheduler","Disable bell"):i18nd("bell-scheduler","Enable bell")
                        enabled:isSoundError?false:true
                    }

                    MenuItem{
                        icon.name:"document-edit.svg"
                        text:i18nd("bell-scheduler","Edit bell")
                        onClicked:bellSchedulerBridge.loadBell(bellId)
                    }
                    MenuItem{
                        icon.name:"delete.svg"
                        text:i18nd("bell-scheduler","Delete the bell")
                    }
                }
            }
        }
    }
}
