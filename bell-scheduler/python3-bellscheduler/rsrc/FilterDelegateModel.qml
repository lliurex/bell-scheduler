import QtQuick 2.15
import QtQml.Models 2.8

DelegateModel {
	id:filterModel
	property var externalTimer: null
	property string role
	property string search
	property string statusFilter
	property var visibleElements:[]

	onRoleChanged:if (externalTimer) externalTimer.restart()
	onSearchChanged:if (externalTimer) externalTimer.restart()
	onStatusFilterChanged:if (externalTimer) externalTimer.restart()

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

		if (!filterModel.model){
			visibleElements=[]
			return
		}
		
	   	let count = allItems.count
		if (count === 0) {
			visibleElements = []
			return
		}

		let localVisibleElements = []
		let searchLower = search.toLowerCase()
		allItems.removeGroups(0,count,["visible"])

		for (let index = 0; index < count; index++) {
			let item = allItems.get(index).model
            let matchesSearch = true
            if (role && item[role] !== undefined) {
                matchesSearch = String(item[role]).toLowerCase().includes(searchLower)
            } else if (searchLower !== "") {
                matchesSearch = false
            }

            let matchesStatus = true
            if (statusFilter !== "all") {
                let currentStatus = item["bellActivated"]
                switch(statusFilter) {
                    case "active":
                        matchesStatus = (currentStatus == true)
                        break
                    case "disable":
                        matchesStatus = (currentStatus == false)
                        break
                 }
            }

            let isItemVisible = item["isVisible"] !== undefined ? item["isVisible"] : true

            if (matchesSearch && matchesStatus && isItemVisible) {
                allItems.setGroups(index,1,["all","visible"])
                localVisibleElements.push(index)
            } 
        }

        visibleElements = localVisibleElements

	}
	Component.onCompleted: if (externalTimer) externalTimer.restart()

}
