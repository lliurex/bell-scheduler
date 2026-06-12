import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.components as PC


Rectangle{
    id:imgContainer
    width:120
    height:120
    border.color: "#d3d3d3"

    property int currentImgIndex
    property alias listEnabled:listSV.enabled

    onCurrentImgIndexChanged:{
        if (imagesSelector.currentIndex!==currentImgIndex){
            imagesSelector.currentIndex=currentImgIndex
        }
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
            model:bellStackBridge.imagesModel

            Component.onCompleted:{
                imagesSelector.currentIndex=imgContainer.currentImgIndex
            }
           
            delegate:Item{
                width:90
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
