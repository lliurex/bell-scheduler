import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.components 3.0 as PC3
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQml.Models 2.8
import QtQuick.Layouts 1.12


Rectangle {
    /*property alias structModel:listBells.model*/
    property alias bellsModel:filterModel.model
    property alias listCount:listBells.count
    color:"transparent"

    GridLayout{
        id:mainGrid
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        anchors.fill:parent

        PC3.TextField{
            id:bellSearchEntry
            font.pointSize:10
            horizontalAlignment:TextInput.AlignLeft
            Layout.alignment:Qt.AlignRight
            focus:true
            width:100
            visible:true
            enabled:true
            placeholderText:i18nd("bell-scheduler","Search...")
            onTextChanged:{
                filterModel.update()
            }
            
        }

        Rectangle {

            id:bellsTable
            visible: true
            Layout.fillHeight:true
            Layout.fillWidth:true
            color:"white"
            border.color: "#d3d3d3"


            PC3.ScrollView{
                implicitWidth:parent.width
                implicitHeight:parent.height
                anchors.leftMargin:10

                ListView{
                    id: listBells
                    anchors.fill:parent
                    height: parent.height
                    enabled:true
                    currentIndex:-1
                    clip: true
                    focus:true
                    boundsBehavior: Flickable.StopAtBounds
                    highlight: Rectangle { color: "#add8e6"; opacity:0.8;border.color:"#53a1c9" }
                    highlightMoveDuration: 0
                    highlightResizeDuration: 0
                    model:FilterDelegateModel{
                        id:filterModel
                        model:bellsModel
                        role:"metaInfo"
                        search:bellSearchEntry.text.trim()

                        delegate: ListDelegateBellItem{
                            width:bellsTable.width
                            bellId:model.id
                            bellCron:model.cron
                            bellMo:model.mo
                            bellTu:model.tu
                            bellWe:model.we
                            bellTh:model.th
                            bellFr:model.fr
                            bellValidity:model.validity
                            bellValidityActivated:model.validityActivated
                            bellImg:model.img
                            bellName:model.name
                            bellSound:model.sound
                            bellActivated:model.bellActivated
                            metaInfo:model.metaInfo
                            isSoundError:model.isSoundError
                            isImgError:model.isImgError
                           
                        }
                    }
                    Kirigami.PlaceholderMessage { 
                        id: emptyHint
                        anchors.centerIn: parent
                        width: parent.width - (units.largeSpacing * 4)
                        visible: listBells.count==0?true:false
                        text: i18nd("bell-scheduler","No bell is configured")
                    }
                } 
             }
        }
    }
}

