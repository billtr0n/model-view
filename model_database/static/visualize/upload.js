!function() {
"use strict";

// define form data object
// make this more general to parse any form, aka build key from 'form_id', and 
var obj = {};

window.onload = function() {
    $("#file").change(displayUpload);
    $("#file").click(function() {
        $("#file").val("");
    });
    $("#submit").click(onSubmit);
};

var onSubmit = function(e) {
    e.preventDefault();
    console.log(obj['files']);
    // handle csrf token
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });
    $.ajax({
        url : "/models/upload/",
        type: "POST",
        data: { post : obj['files'] },

        success : function(json) {
            $("#message").val('');
            console.log(json);
            console.log("success");
        },

        error : function(json) {
            console.log(json)
        }
    });
};

var displayUpload = function(e) {
    var file = e.target.files[0];
    var textType = /text.*/;
    if (file.type.match(textType)) { 
        var fr = new FileReader();
        fr.onload = function(e) {
            try {
                // console.log( e.target.result );
                $("#message").html(document.createTextNode(e.target.result))                
                if (typeof e.target.result === 'string') {
                    obj['files'] = e.target.result;
                }
            } catch(err) {
                console.log(err) // TODO: Handle this gracefully
            }
        }
        fr.readAsText(file);
    } else {
        console.log("Filetype not supported.");
    }
};

// using jQuery
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
}();