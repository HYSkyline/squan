function showTime(){     
    var current_time = new Date();
    var current_year = current_time.getFullYear().toString();
    var current_month = (current_time.getMonth() + 1).toString();
    if (current_month < 10) current_month = '0' + current_month;
    var current_day = current_time.getDate().toString();
    if (current_day < 10) current_day = '0' + current_day;
    var current_hour = current_time.getHours().toString();
    if (current_hour < 10) current_hour = '0' + current_hour;
    var current_minute = current_time.getMinutes().toString();
    if (current_minute < 10) current_minute = '0' + current_minute;
    var current_second = current_time.getSeconds().toString();
    if (current_second < 10) current_second = '0' + current_second;
    document.getElementById("Current_Time_Area").innerText =current_year + '-' + current_month + '-' + current_day + ' ' + current_hour + ':' + current_minute + ':' + current_second; 

    var end_time = new Date("2023/7/11 9:35:12");
    var disSecond = Math.floor((end_time.getTime() - current_time.getTime())/1000)
    var disDay = Math.floor(disSecond/(60*60*24));
    var disHour = Math.floor((disSecond - disDay * 60 * 60 * 24)/(60 * 60))
    var disMinute = Math.floor((disSecond - disDay * 86400 - disHour * 3600) / 60)
    var dis_second = disSecond - disDay * 86400 - disHour * 3600 - disMinute * 60
    if (disHour < 10) disHour = '0' + disHour.toString();
    if (disMinute < 10) disMinute = '0' + disMinute.toString();
    if (dis_second < 10) dis_second = '0' + dis_second.toString()
    document.getElementById("Left_Time_Area").innerText = disDay + 'd ' + disHour + 'h ' + disMinute + 'm ' + dis_second + 's';

    window.setTimeout("showTime()",1000);
}