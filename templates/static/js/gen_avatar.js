function generate(){
    var hash =  Math.random().toString(36).substring(2, 20) + Math.random().toString(36).substring(2, 20);
    var data = blockies.create({
        seed: hash,
        size: 9, // width/height of the icon in blocks, default: 8
        scale: 15, // width/height of each block in pixels, default: 4
        spotcolor: '#000' // each pixel has a 13% chance of being of a third color,
    }).toDataURL();
    return data;
}



function update_img_fields(data) {
    var img = $('card-avatar');
    document.getElementById("card-avatar-0").src=data;
    document.getElementById("card-avatar-1").src=data;
    document.getElementById("head-avatar").src=data;
    // img.attr('src', data);
    // img.appendTo('#id_of_element_where_you_want_to_add_image'); }
}

function avatar() {
    // console.log($('#profile-form'));
    var form = new FormData();
    var data = generate();
    form.append("image", data);
    // console.log(form);
    $.ajax({
        type: 'POST',
        url: '/account/update_avatar/',
        contentType: false,
        cache: false,
        processData:false,
        data : form,

        success:function(json){
            update_img_fields(data);
            update_messages(json.messages);
            ajaxAutoHideMessages(json.messages.length);
            // $('close-popup').click();
            var url = window.location.href;
            location.href = url.slice(0, url.search('#') + 1);
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
};