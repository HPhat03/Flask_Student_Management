
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