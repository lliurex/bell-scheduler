import org.kde.plasma.components as PC
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQml.Models
import QtQuick.Layouts


Rectangle {
    property alias bellsModel:filterModel.model
    property alias listCount:listBells.count
    color:"transparent"

    ColumnLayout{
        anchors.fill:parent
        spacing:10

        RowLayout{
            id: btnRow
            Layout.fillWidth:true
            Layout.alignment:Qt.AlignRight
            spacing:10
            enabled:true

            Button{
                id:statusFilterBtn
                display:AbstractButton.IconOnly
                icon.name:"view-filter"
                enabled:bellsOptionsStackBridge.enableChangeStatusOptions.enableFilter
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
                        enabled:bellsOptionsStackBridge.filterStatusValue!="active"
                                ?true
                                :false
                        onClicked:bellsOptionsStackBridge.manageStatusFilter("active")
                    }

                    MenuItem{
                        icon.name:"audio-volume-muted.svg"
                        text:i18nd("bell-scheduler","Show disabled bells")
                        enabled:bellsOptionsStackBridge.filterStatusValue!="disable"
                                ?true
                                :false
                        onClicked:bellsOptionsStackBridge.manageStatusFilter("disable")
                    }
                    MenuItem{
                        icon.name:"kt-remove-filters.svg"
                        text:i18nd("bell-scheduler","Remove filter")
                        enabled:bellsOptionsStackBridge.filterStatusValue!="all"
                                ?true
                                :false
                        onClicked:bellsOptionsStackBridge.manageStatusFilter("all")
                    }
                }
                
            }

            PC.TextField{
                id:bellSearchEntry
                font.pointSize:10
                horizontalAlignment:TextInput.AlignLeft
                Layout.alignment:Qt.AlignRight
                focus:true
                width:100
                visible:true
                enabled:((listBells.count==0)&& (text.length==0))
                        ?false
                        :true
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


            PC.ScrollView{
                anchors.fill:parent

                ListView{
                    id: listBells

                    Timer {
                        id: searchTimer
                        interval: 150
                        repeat: false
                        onTriggered: filterModel.update()
                    }

                    model:FilterDelegateModel{
                        id:filterModel
                        model:bellsModel
                        role:"metaInfo"
                        search:bellSearchEntry.text.trim()
                        statusFilter:bellsOptionsStackBridge.filterStatusValue

                        delegate: ListDelegateBellItem{
                            width:bellsTable.width-18
                            bellId:model.id
                            bellCron:model.cron
                            bellDays:model.weekDays
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

                    currentIndex:-1
                    enabled:true
                    clip: true
                    focus:true
                    boundsBehavior: Flickable.StopAtBounds
                    highlightFollowsCurrentItem:true
                    highlightMoveDuration: 0
                    highlightResizeDuration: 0
                    
                    Kirigami.PlaceholderMessage { 
                        id: emptyHint
                        anchors.centerIn: parent
                        width: parent.width - (Kirigami.Units.largeSpacing * 4)
                        visible: listBells.count==0?true:false
                        text: bellSearchEntry.text.length==0
                              ?i18nd("bell-scheduler","No bell is configured")
                              :i18nd("bell-scheduler","No bell found")
                        icon.name:"bell-scheduler"
                    }
                } 
             }
        }
    }
}

