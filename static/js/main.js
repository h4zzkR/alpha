$(function() {

    $('#profile-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        send_profile();
    });

        $('#project-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        send_project();
    });

    function alertTimer() {
        window.setTimeout(function () {
            $(".alert").fadeTo(500, 0).slideUp(400, function () {
                $(this).remove();
            });
        }, 10000);
    };


    function update_messages(messages){
            $("#div_messages").html("");
            $.each(messages, function (i, m) {
                var msg = "<div class=\"alert" + "\x20" + m.level + "\x20" + "alert-dismissible data-auto-dismiss myalert-bottom role=\"alert\">" +
                      "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
                        "<span aria-hidden=\"true\">&times;</span></button>" + m.message + "</div>";
                alertTimer();
                $("#div_messages").append(msg);

            })
    };



    function send_project(){
        var fullUrl = window.location.href;
        var index = fullUrl.search(/u/);
        var url = '/' + fullUrl.substring(index);
        var data = $('profile-form').serializeArray();
        console.log(url);
        $.ajax({
            url : '/p/new',
            type : "POST",
            data : {
                name : $('#input-name').val(),
                ts_url : $('#input-ts_url').val(),
                vcs_url : $('#input-vcs_url').val(),
                team_size : $('#input-team_size').val(),
                short_description : $('#input-short_description').val(),
                // check description and tags here
                description : $('#input-description').val(),
                tags : $('#input-tags').val(),
            },

             success : function(json) {
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                update_messages(json.messages);
                if (json.result != 'error') {
                }
            },

            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }

        });

    }


    function send_profile() {
        var fullUrl = window.location.href;
        var index = fullUrl.search(/u/);
        var url = '/' + fullUrl.substring(index);
        var data = $('profile-form').serializeArray();
        console.log(url);
        $.ajax({
            url : '/update_profile', // the endpoint
            type : "POST", // http method
            data : { username : $('#input-username').val(),
                    email : $('#input-email').val(),
                    first_name : $('#input-first-name').val(),
                    last_name : $('#input-last-name').val(),
                    country : $('#country').val(),
                    state : $('#state').val(),
                    github_link : $('#input-github').val(),
                    gitlab_link : $('#input-gitlab').val(),
                    telegram_link : $('#input-telegram').val(),
                    linkedIn_link : $('#input-linkedin').val(),
                    bio : $('#bio').val(),

                }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                update_messages(json.messages);
                if (json.result != 'error') {
                    $('input[name=input-username]').val(json.username);
                    $('input[name=input-first-name]').val(json.first_name);
                    $('input[name=input-github]').val(json.github_link);
                    $('input[name=input-gitlab]').val(json.gitlab_link);
                    $('input[name=input-telegram]').val(json.telegram_link);
                    $('input[name=input-linkedin]').val(json.linkedIn_link);
                    $('input[name=bio]').val(json.bio);
                    // $(selector).text(function(index,currentcontent))
                    $("h3[id=user-name]").text(json.first_name + "\x20" + json.last_name);
                    $("p[id=user-bio]").text(json.bio);
                    $("p[id=user-location]").text(json.state + "," + "\x20" + json.country);
                    // $("#user-names").text(json.first_name + "\x20" + json.last_name);
                }
            },

            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
