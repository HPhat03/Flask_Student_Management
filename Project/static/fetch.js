function Fetch(){
    fetch('/api/users'
    ).then(function(res) {
    return res.json();
    }).then(function(data) {
        console.log(data)
    })
}