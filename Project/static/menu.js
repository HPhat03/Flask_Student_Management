console.log("ACCESS SUCCESSFULLY")
fetchNotifications()
setInterval(function () {
    fetchNotifications()
}, 60000)


function fetchNotifications(){
    fetch('/api/changed_notification').then(function(res){
        return res.json()
    }).then(function(data){
        note = document.getElementById("notification")
        if(data.length > 0){
            myHTML = "<ul class = 'list-group'>"
            data.forEach((n) => myHTML += `<li class="list-group-item" style="display: flex;justify-content: space-between; align-items: center">
                                              <div>${n['role'].substring(9)}</div>
                                              <div style = "width:90%"><span style = "font-weight: bold">${n['actor']}</span> đã ${n['content']}</div>
                                              <div>${n['time']}</div>
                                          </li>`)
            myHTML += "</ul>"
            note.innerHTML = myHTML
        }
     })
}