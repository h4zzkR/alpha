function update_messages(messages){
        //Функция для добавления алертов в массив стандартных джанговских
        $("#div_messages").html("");
        $.each(messages, function (i, m) {
            var msg = "<div class=\"alert" + "\x20" + m.level + "\x20" + "alert-dismissible data-auto-dismiss myalert-bottom role=\"alert\">" +
                  "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
                    "<span aria-hidden=\"true\">&times;</span></button>" + m.message + "</div>";
            alertTimer();
            $("#div_messages").append(msg);

        })
};