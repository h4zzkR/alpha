
function update_fields(json) {
    for(var key in json){
        // var newField = json[key];
        console.log(key, json[key]);
        $('#' + key).value = json[key];
    }
    $('input[name=username]').val(json.username);

    $("h3[id=user_full_name]").text(json.first_name + "\x20" + json.last_name);
    $("h1[id=username]").text("Привет, " + json.username + "!");
    $("p[id=user-bio]").text(json.bio);
}

function create_post() {
    // console.log($('#profile-form'));
    var $form =  $('#profile-form');
    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data : $form.serialize(),

        success:function(json){
            // document.getElementById("profile-form").reset();
            update_fields(json);
             document.getElementById("linked_in").setAttribute('value', 'assasa.com');
            // console.log(json);
            // updating fields
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
};



$('#profile-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});