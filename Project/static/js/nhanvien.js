
function delete_from_list(id, obj){
    if (confirm("Bạn chắc chắn muốn xóa") == true){
        obj.disabled = true;
        fetch(`/api/user_pending/${id}`, {
            method: 'DELETE'
        }).then(function(res){
            return res.json()
        }).then(function(data){
            console.log(data)
            obj.disabled = false
            document.getElementById(id).style.display = "none"
        })
    }
}

function validate(id, obj){
    if (confirm("Xác nhận lưu học sinh này?")==true){
        obj.disabled = true;
        fetch(`/api/validate_user/${id}`, {
            method: 'POST'
        }).then(function(res) {
            return res.json()
        }).then(function(data){
            console.log(data)
            obj.disabled = false
            if (data['status'] == "success") document.getElementById(id).style.display = "none"
            alert(data['message'])
        })
    }
}
function validate_all(obj){
    if (confirm("Xác nhận sao lưu tất cả học sinh trong hàng chờ")==true){
        obj.disabled = true
        fetch('/api/validate_user', {
            method: 'POST'
        }).then(function(res){
            return res.json()
        }).then(function(data){
            obj.disabled = false
            console.log(data)
            if (data['status'] == 'failed')
                alert(data['message'])
            else{
                alert("Lưu hoàn thành")
                for(var i = 1; i <= data['success'].length; i++)
                    document.getElementById(i).style.display = 'none'
            }
        })
    }
}

function get_non_class_user_by_grade(){
grade = document.getElementById('grade').value
console.log(grade)
if (grade!="NULL")
    fetch(`/api/non_class_student/${grade}`)
    .then(function(res){
        return res.json()
    }).then(function(data){
        document.getElementById('amount').value = data.length
        html = ""
        for(var i = 0; i<data.length; i++){
            html += `<li class="list-group-item" style="height: 20%; display: flex; justify-content: space-between">
                <div style="width: 5%">${data[i]['id']}</div>
                <div style="width: 20%">${data[i]['name']}</div>
                <div style="width: 10%">Khối ${data[i]['grade']}</div>
                <div style="width: 20%">${data[i]['semester']}</div>
            </li>`
        }
        document.getElementById('student_panel_get').innerHTML = html
        console.log(data)
    })
else
    document.getElementById('amount').value = ""
    document.getElementById('student_panel_get').innerHTML = "<h2 style='display: flex; justify-content: center; align-items: center'>Vui lòng chọn khối lớp</h2>"
}