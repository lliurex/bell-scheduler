import QtQuick 2.15
import QtQml.Models 2.8

DelegateModel {
	id:filterModel
	property string role
	property string search
	onRoleChanged:Qt.callLater(update)
	onSearchChanged:Qt.callLater(update)
	
	groups: [
		DelegateModelGroup{
			id:allItems
			name:"all"
			includeByDefault:true
			onCountChanged:Qt.callLater(update)
		},
		DelegateModelGroup{
			id:visibleItems
			name:"visible"
		}
	]

	filterOnGroup:"visible"

	function update(){
		allItems.setGroups(0,allItems.count,[ "all"]);
		for (let index = 0; index < allItems.count; index++) {
            let item = allItems.get(index).model;
            let visible = item[role].toLowerCase().includes(search.toLowerCase());
            if (!visible) continue;
            allItems.setGroups(index, 1, [ "all", "visible" ]);
        }

	}
	Component.onCompleted: Qt.callLater(update)

}
