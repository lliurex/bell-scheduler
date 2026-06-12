import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.components as PC


Rectangle{
    id:imgContainer
    width:120
    height:120
    border.color: "#d3d3d3"

    property int currentImgIndex:0
    property alias listEnabled:listSV.enabled

    onCurrentImgIndexChanged:{
        imagesSelector.currentIndex=currentImgIndex
        imagesSelector.positionViewAtIndex(currentImgIndex,ListView.Center)
    }

    PC.ScrollView{
        id:listSV
        anchors.fill:parent

        ListView{
            id:imagesSelector
            implicitWidth:imgContainer.width
            implicitHeight:imgContainer.height
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
                height:120

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
