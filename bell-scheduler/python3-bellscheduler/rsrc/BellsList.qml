import org.kde.plasma.components 3.0 as PC3
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import QtQuick.Layouts 1.15


Rectangle {
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
        RowLayout{
            Layout.alignment:Qt.AlignRight
            spacing:10
            Button{
                id:statusFilterBtn
                display:AbstractButton.IconOnly
                icon.name:"view-filter.svg"
                enabled:bellsOptionsStackBridge.enableChangeStatusOptions[2]
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("bell-scheduler","Click to filter bells by status")
                onClicked:optionsMenu.open();
               
                Menu{
                    id:optionsMenu
                    y: statusFilterBtn.height
                    x:-(optionsMenu.width-statusFilterBtn.width/2)

                    MenuItem{
                        icon.name:"audio-on.svg"
                        text:i18nd("bell-scheduler","Show activated bells ")
                        enabled:{
                            if (bellsOptionsStackBridge.filterStatusValue!="active"){
                                true
                            }else{
                                false
                            }
                        }
                        onClicked:bellsOptionsStackBridge.manageStatusFilter("active")
                    }

                    MenuItem{
                        icon.name:"audio-volume-muted.svg"
                        text:i18nd("bell-scheduler","Show disabled bells")
                        enabled:{
                            if (bellsOptionsStackBridge.filterStatusValue!="disable"){
                                true
                            }else{
                                false
                            }
                        }
                        onClicked:bellsOptionsStackBridge.manageStatusFilter("disable")
                    }
                    MenuItem{
                        icon.name:"kt-remove-filters.svg"
                        text:i18nd("bell-scheduler","Remove filter")
                        enabled:{
                            if (bellsOptionsStackBridge.filterStatusValue!="all"){
                                true
                            }else{
                                false
                            }
                        }
                        onClicked:bellsOptionsStackBridge.manageStatusFilter("all")
                    }
                }
                
            }
             
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
                        statusFilter:bellsOptionsStackBridge.filterStatusValue

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

