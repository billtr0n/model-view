!function() {
"use strict";
var obj = {};
obj['tags'] = "";
obj['comments'] = "";
obj['parameters'] = "";

window.onload = function() {
    var fileInput = document.getElementById('file');
    var btnSubmit = document.getElementById('submit');
    btnSubmit.addEventListener('click', onSubmit)
    fileInput.addEventListener('change', displayUpload);
};

var onSubmit = function(e) {
    parseTags();
    parseComments();
    console.log(obj)
};

var displayUpload = function(e) {
    var file = e.target.files[0];
    var textType = /text.*/;
    if (file.type.match(textType)) { 
        var fr = new FileReader();
        fr.onload = function(e) {
            try {
                var temp = JSON.parse(e.target.result);
                _mergeRecursive(obj, temp);
                tableCreate();
                console.log(obj)

            } catch(err) {
                console.log(err)
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
        obj['tags'] = "";
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
var _mergeRecursive = function(obj1, obj2) {
    for ( var p in obj2 ) {
        if ( obj2.hasOwnProperty(p) && obj1[p] !== "" ) {
            _mergeRecursive(obj1[p],obj2[p]);
        } else {
            obj1[p] = obj2[p];
        }
    }
}
}();