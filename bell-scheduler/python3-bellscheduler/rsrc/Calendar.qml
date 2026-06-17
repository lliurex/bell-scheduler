import QtQuick 2.15
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.1

Rectangle {
    id: root
    width: 325
    height: 250

    property alias calendarLocale: calendar.calendarLocale
    property alias startDate: calendar.startDate
    property alias stopDate: calendar.stopDate
    property alias initDate: calendar.initDate
    property alias endDate: calendar.endDate
    property alias rangeDate: calendar.rangeDate
    property alias daysInRange: calendar.daysInRange
    property alias selectedDate: calendar.selectedDate

    signal getSelectedDate (variant value)

    Calendar {
        id: calendar
        width: parent.width
        height: parent.height
        anchors.centerIn: parent
        frameVisible: true
        weekNumbersVisible: false
        focus: true

        property string calendarLocale: "es_ES"
        property var startDate: undefined
        property var stopDate: undefined
        property string initDate: ""
        property string endDate: ""
        property var daysInRange: []
        property bool rangeDate: true

        locale: Qt.locale(calendar.calendarLocale)

        style: CalendarStyle {
            dayDelegate: Item {
                id: dayCell

                readonly property color sameMonthDateTextColor: "#444"
                readonly property color selectedDateColor: "#3778d0"
                readonly property color selectedDateTextColor: "white"
                readonly property color differentMonthDateTextColor: "#bbb"
                readonly property color invalidDatecolor: "#dddddd"
                property var dateOnFocus: styleData.date

                Rectangle {
                    anchors.fill: parent
                    border.color: "transparent"
                    color: {
                        var dateStr = Qt.formatDate(dayCell.dateOnFocus, "dd/MM/yyyy");

                        if (calendar.startDate === undefined && calendar.stopDate === undefined) {
                            if (dateStr === calendar.initDate || dateStr === calendar.endDate) {
                                return dayCell.selectedDateColor;
                            }
                            if (calendar.daysInRange && calendar.daysInRange.indexOf(dateStr) !== -1) {
                                return "#55555555";
                            }
                            return "transparent";
                        }

                        var currentMs = dayCell.dateOnFocus.getTime();
                        var startMs = calendar.startDate ? calendar.startDate.getTime() : 0;
                        var stopMs = calendar.stopDate ? calendar.stopDate.getTime() : 0;

                        if (calendar.startDate && currentMs === startMs) return dayCell.selectedDateColor;
                        if (calendar.stopDate && currentMs === stopMs) return dayCell.selectedDateColor;

                        if (calendar.startDate && calendar.stopDate && currentMs > startMs && currentMs < stopMs) {
                            return "#55555555";
                        }

                        return "transparent";
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    propagateComposedEvents: true
                    onPressed: {
                        var clickedDate = dayCell.dateOnFocus;
                        var clickedStr = Qt.formatDate(clickedDate, "dd/MM/yyyy");

                        if (calendar.startDate === undefined) {
                            calendar.startDate = clickedDate;
                            if (!calendar.rangeDate) {
                                calendar.stopDate = clickedDate;
                            } else {
                                calendar.stopDate = undefined;
                            }
                            root.getSelectedDate([clickedStr, "start"]);
                        }
                        else if (calendar.stopDate === undefined) {
                            if (clickedDate <= calendar.startDate) {
                                calendar.startDate = clickedDate;
                                root.getSelectedDate([clickedStr, "start"]);
                            } else {
                                calendar.stopDate = clickedDate;
                                root.getSelectedDate([clickedStr, "end"]);
                            }
                        }
                        else {
                            if (calendar.rangeDate) {
                                calendar.startDate = clickedDate;
                                calendar.stopDate = undefined;
                                root.getSelectedDate([clickedStr, "start"]);
                            } else {
                                calendar.startDate = undefined;
                                calendar.stopDate = clickedDate;
                                root.getSelectedDate([clickedStr, "end"]);
                            }
                        }
                        mouse.accepted = false;
                    }
                }

                Label {
                    id: dayDelegateText
                    text: dayCell.dateOnFocus.getDate()
                    anchors.centerIn: parent
                    color: {
                        if (!styleData.valid) return dayCell.invalidDatecolor;
                        if (styleData.selected) return dayCell.selectedDateTextColor;
                        return styleData.visibleMonth ? dayCell.sameMonthDateTextColor : dayCell.differentMonthDateTextColor;
                    }
                }
            }
        }
    }
}
