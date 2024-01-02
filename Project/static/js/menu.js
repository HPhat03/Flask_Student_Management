//
////function fetchNotifications(){
//    fetch('/api/changed_notification'
//    ).then(function(res){
//        return res.json()
//    }).then(function(data){
//        note = document.getElementById("notification");
//        if(data.length > 0){
//            myHTML = "<ul class = 'list-group'>";
//            data.forEach((n) => myHTML += `<li class="list-group-item" style="display: flex;justify-content: space-between; align-items: center">
//                                              <div style = "width:10%">${n['role'].substring(9)}</div>
//                                              <div style = "width:50%"><span style = "font-weight: bold">${n['actor']}</span> đã ${n['content']}</div>
//                                              <div>${n['time']}</div>
//                                          </li>`);
//            myHTML += "</ul>";
//        }
//        else {
//            myHTML = `<div style='display:flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%'>
//                        <h1>KHÔNG CÓ THAY THAY ĐỔI</h1>
//                    </div>`;
//        }
//        note.innerHTML = myHTML;
//
//     })
////}
function setPara(key,value){
    let url = window.location.href;
    var list = url.split(/\?|&/);
    index = url.indexOf(key);
    if (index == -1){
        if (url.indexOf("?") > -1)
            url += `&${key}=${value}`;
        else
            url += `?${key}=${value}`;
        }
    else{
        url = `${list[0]}\?`;
        for(i = 1; i<list.length; i++){
            if (list[i].indexOf(key) > -1)
                list[i] = `${key}=${value}`;
            url += i<2 ? list[i] : `&${list[i]}`;
        }
    }
    window.location.href = url;
}