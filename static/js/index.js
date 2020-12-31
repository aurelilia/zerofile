function validateFile() {
    var fileInput = document.getElementById('fileselect');
    var timeout = document.getElementById('timeout');
    try {
        var size = fileInput.files[0].size;
        if (size > 50000000) {
            alert('Your file is too big. (50MB max)');
            return false;
        }
    } catch (e) {
        alert('Please select a file.');
        return false;
    }
    uploadAjax(document.getElementById('fileselect').files[0], timeout.value);
    return false;
}

function updateFile() {
    var fullPath = document.getElementById('fileselect').value;
    var fileText = document.getElementById('filetext');
    fileText.innerHTML = fullPath.split(/(\\|\/)/g).pop();
}

async function uploadAjax(file, timeout) {
    document.getElementById('upload-button').disabled = true;
    await changeText('<div class="meter"><span style="width: 0%"></span></div>');

    var form = new FormData();
    form.append('fileselect', file);
    form.append('timeout', timeout);
    form.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    var request = new XMLHttpRequest();
    request.upload.addEventListener('progress', function(evt) {
        if (evt.lengthComputable) {
            var text = document.getElementById('bottom-text');
            var percentComplete = (evt.loaded / evt.total) * 100;
            text.innerHTML = '<div class="meter"><span style="width: VAR%"></span></div>'.replace('VAR', percentComplete);
        }
    }, false);
    request.onreadystatechange = async function() {
        if (this.readyState == 4 && this.status == 200) {
            await changeText(this.responseText);
            document.getElementById('upload-button').disabled = false;
        }
    };
    request.open('POST', '/');
    request.send(form);
}

async function changeText(newtext) {
    var text = document.getElementById('bottom-text');
    text.classList.toggle('fade');
    await new Promise(resolve => setTimeout(resolve, 700));
    text.innerHTML = newtext;
    text.classList.toggle('fade');
}

function onDrop(e) {
    e.preventDefault();
    document.getElementById('filetext').innerHTML = e.dataTransfer.files[0].name;
    uploadAjax(e.dataTransfer.files[0]);
}