import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

ItemDelegate{

    id: listBellItem
    property string bellId
    property string bellCron
    property var bellDays:[]
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
    height:130

    width: listBellItem.ListView.view?listBellItem.ListView.view.width -10 : 0
    hoverEnabled:true

    leftPadding:5
    rightPadding:10

    onHoveredChanged:{
        if (hovered){
            if (listBellItem.ListView.view && !optionsMenu.opened){
                listBellItem.ListView.view.currentIndex=index
            }
        }else{
            if (!optionsMenu.opened && listBellItem.ListView.view){
                listBellItem.ListView.view.currentIndex=-1
            }
        }
    }

    background:Rectangle {
        x:5
        y:5
        width:parent.width-5
        height:parent.height-5
        color: {
            if (isSoundError || isImgError){
                Kirigami.Theme.negativeBackgroundColor
            }else{
                if (listBellItem.hovered || listBellItem.ListView.isCurrentItem || optionsMenu.opened){
                    Qt.alpha(Kirigami.Theme.highlightColor,0.15)
                }else{
                    "transparent"
                }
            }
        }
        radius:6
        border.width:1
        border.color:{
            if (listBellItem.hovered || listBellItem.ListView.isCurrentItem || optionsMenu.opened){
                if (isSoundError || isImgError){
                    Kirigami.Theme.negativeTextColor
                }else{
                    Kirigami.Theme.highlightColor
                }
            }else{            
                "transparent"
            }
        }
    }
 
    contentItem:RowLayout {
        spacing:20

        ColumnLayout{
            id:cronRow
            Layout.preferredWidth:190
            Layout.fillHeight:true
            Layout.alignment:Qt.AlignVCenter
            spacing:0

            Text{
                id:timeText
                text:bellCron
                color:"#3366cc"
                font.pointSize: 35
                Layout.alignment:Qt.AlignHCenter
            }
            RowLayout{
                id:dayRow
                Layout.alignment:Qt.AlignHCenter
                spacing:5
                Repeater {
                    model: [
                        { text: "M", idx: 0 },
                        { text: "T", idx: 1 },
                        { text: "W", idx: 2 },
                        { text: "R", idx: 3 },
                        { text: "F", idx: 4 }
                    ]
                    Text{
                        id:dayText
                        text:i18nd("bell-scheduler",modelData.text)
                        color:bellDays[modelData.idx]? "#3366cc":"#A0A0A0"
                        font.pointSize:18
                    }
                }
                   
            }
            
            Text{
                id:validityText
                text:bellValidity
                color:bellValidityActivated?"#3366cc":"#A0A0A0"
                font.pointSize:11
                visible:bellValidity!==""
                Layout.alignment:Qt.AlignHCenter
            }
        }
        
        Image{
            id:bellImage
            Layout.preferredWidth:70
            Layout.preferredHeight:70
            fillMode:Image.PreserveAspectFit
            source:bellImg
        }
        
        ColumnLayout{
            id:bellDescription
            spacing:10
            Layout.fillWidth:true
            Layout.alignment:Qt.AlignVCenter
            
            Text{
                id:nameText
                text:bellName
                font.pointSize: 18
                horizontalAlignment:Text.AlignLeft
                elide:Text.ElideMiddle
                Layout.fillWidth:true
            }

            Text{
                id:soundText
                text:bellSound
                font.italic:isSoundError
                font.pointSize: 11
                horizontalAlignment:Text.AlignLeft
                elide:Text.ElideMiddle
                Layout.fillWidth:true
            }

        }

        Kirigami.Icon {
            id:bellState
            source:bellActivated?"audio-on":"audio-volume-muted"
            Layout.preferredWidth: 32
            Layout.preferredHeight: 32
            Layout.alignment: Qt.AlignVCenter
        }
            
        Button{
            id:manageBellBtn
            display:AbstractButton.IconOnly
            icon.name:"configure"
            Layout.alignment: Qt.AlignVCenter
            visible:listBellItem.ListView.isCurrentItem || listBellItem.hovered || optionsMenu.opened
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("bell-scheduler","Click to manage this bell")
            onClicked:optionsMenu.open();
  
            Connections{
                target:listBells
                function onCurrentIndexChanged(){
                    if (!listBellItem.ListView.isCurrentItem && optionsMenu.opened){
                        optionsMenu.close()
                    }

                }
            }

            Menu{
                id:optionsMenu
                y: manageBellBtn.height
                x:-(optionsMenu.width-manageBellBtn.width/2)

                MenuItem{
                    icon.name:bellActivated?"audio-volume-muted":"audio-on"
                    text:bellActivated?i18nd("bell-scheduler","Disable bell"):i18nd("bell-scheduler","Enable bell")
                    enabled:isSoundError?false:true
                    onClicked:bellsOptionsStackBridge.changeBellStatus({"allBells":false,"active":!bellActivated,"bellId":bellId})
                }

                MenuItem{
                    icon.name:"document-edit"
                    text:i18nd("bell-scheduler","Edit bell")
                    onClicked:bellStackBridge.loadBell({"bellId":bellId,"isImgError":isImgError,"isSoundError":isSoundError})
                }
                
                MenuItem{
                    icon.name:"xml-node-duplicate"
                    text:i18nd("bell-scheduler","Duplicate bell")
                    enabled:((isSoundError) || (isImgError))
                            ?false
                            :true
                    onClicked:bellStackBridge.duplicateBell({"bellId":bellId,"isImgError":isImgError,"isSoundError":isSoundError})
                }
                
                MenuItem{
                    icon.name:"delete"
                    text:i18nd("bell-scheduler","Delete the bell")
                    onClicked:bellsOptionsStackBridge.removeBell({"allBells":false,"bellId":bellId})
                }
            }
        }
    }
}
