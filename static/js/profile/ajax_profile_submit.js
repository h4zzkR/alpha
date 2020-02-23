
function update_fields(json) {
    for(var key in json){
        // var newField = json[key];
        // console.log(key, json[key]);
        $('#' + key).value = json[key];
    }
    // paste here whatever you want update from json response
    // $('input[name=username]').val(json.username);

    $("h3[id=user_full_name]").text(json.first_name + "\x20" + json.last_name);
    $("h1[id=username]").text("Привет, " + json.username + "!");
    $("p[id=user-bio]").text(json.bio);
}

function update_messages(messages){
        $("#div_messages").html("");
        var i = 0
        $.each(messages, function (i, m) {
            var msg = "<div id='message" + i + "'" + "class=\"alert" + "\x20" + m.level + "\x20" + "alert-dismissible data-auto-dismiss myalert-bottom role=\"alert\">" +
                  "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
                    "<span aria-hidden=\"true\">&times;</span></button>" + m.message + "</div>";
            $("#div_messages").append(msg);
            i++;
        });
};

function create_post(id) {
    // console.log($('#profile-form'));
    var form =  $(id);
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data : form.serialize(),

        success:function(json){
            // document.getElementById("profile-form").reset();
            update_fields(json);
            update_messages(json.messages);
            ajaxAutoHideMessages(json.messages.length);
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
    create_post('#profile-form');
});