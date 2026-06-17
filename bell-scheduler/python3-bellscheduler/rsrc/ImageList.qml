import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.plasma.components 3.0 as PC3


Rectangle{
    id:imgContainer
    width:120
    height:120
    border.color: "#d3d3d3"

    property int currentImgIndex:1
    property alias listEnabled:listSV.enabled

    onCurrentImgIndexChanged:{
        imagesSelector.positionViewAtIndex(currentImgIndex,ListView.Center)
    }

    PC3.ScrollView{
        id:listSV
        anchors.fill:parent

        ListView{
            id:imagesSelector
            anchors.fill:parent
            focus:true
            snapMode:ListView.SnapOneItem
            highlightRangeMode: ListView.StrictlyEnforceRange
            highlightMoveDuration:0
            highlightMoveVelocity:-1
            model:bellStackBridge.imagesModel

            onCurrentIndexChanged:{
                 imgContainer.currentImgIndex=currentIndex
            }

            delegate:Item{
                width:imgContainer.width
                height:imgContainer.height

                Image{
                  width:80
                  height:80
                  fillMode:Image.PreserveAspectFit
                  source:imageSource
                  anchors.centerIn:parent
                  clip:true
                }

            }
        }
    }
}
