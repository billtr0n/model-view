!function() {
"use strict";

// define form data object
// make this more general to parse any form, aka build key from 'form_id', and 
var obj = {};
obj['tags'] = "";
obj['comments'] = "";
obj['parameters'] = "";

window.onload = function() {
    var fileInput = document.getElementById('file');
    var btnSubmit = document.getElementById('submit');
    btnSubmit.addEventListener('click', onSubmit)
    fileInput.addEventListener('change', displayUpload);
    console.log(obj);
};

var onSubmit = function(e) {
    parseTags();
    parseComments();
    console.log(obj);
};

var displayUpload = function(e) {
    var file = e.target.files[0];
    var textType = /text.*/;
    if (file.type.match(textType)) { 
        var fr = new FileReader();
        fr.onload = function(e) {
            try {
                var temp = JSON.parse(e.target.result);
                _merge(obj, temp);
                tableCreate();
                console.log(obj)

            } catch(err) {
                console.log(err) // TODO: Handle this gracefully
            }
        }
        fr.readAsText(file);
    } else {
        console.log("Filetype not supported.");
    }
};

    // TODO: Add logic, to handle multiple file uploads before the submission
function tableCreate() {
    var body = document.body;
    var tbl = document.createElement('table');
    for (var i=0; i<obj.parameters.length; i++) {
        var tr = tbl.insertRow();
        for (var key in obj.parameters[i]) {
            var td = tr.insertCell();
            td.appendChild(document.createTextNode(obj.parameters[i][key]));
        }
    }
    body.appendChild(tbl);
    
}

function parseTags() {
    var txtTags = document.getElementById('tags');
    if (txtTags.value === "") {
        return;
    }
    obj['tags'] = [];
    var tags = txtTags.value.split(',');
    for (var i=0; i<tags.length; i++) {
        obj['tags'][i] = tags[i].trim();
    }      
}

function parseComments() {
    var txtComments = document.getElementById('comments');
    obj['comments'] = txtComments.value;
}

// unscoped helping functions
var _merge = function(dest, src) {
    for ( var par in src ) {
        if ( src.hasOwnProperty(par) && dest[par] !== "" ) {
            _merge(dest[par], src[par]);
        } else {
            dest[par] = src[par];
        }
    }
}
}();