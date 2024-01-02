
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
            alert("Lưu hoàn thành")
            for(var i = 1; i <= data['success'].length; i++)
                document.getElementById(i).style.display = 'none'

        })
    }
}