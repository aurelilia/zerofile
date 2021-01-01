'use strict'

const URL = "https://file.angm.xyz/s/"
const CHUNK_SIZE = 64 * 1024;
const HOST = document.getElementById('stream-id') != null;
const peerId = btoa(Math.random()).substring(6, 12);
const meter = document.getElementById('meter');

let connected = false;
let conn = null;

async function copyURL() {
    navigator.clipboard.writeText(URL + peerId + "/")
    document.getElementById("clipboard-copied").classList.add("show");
    await new Promise(resolve => setTimeout(resolve, 700));
    document.getElementById("clipboard-copied").classList.remove("show");
}

function clientConnected() {
    connected = true;
    document.getElementById("before-connection").classList.add("nodisplay");
    document.getElementById("connected").classList.remove("nodisplay");

    conn.on('close', function () {
        alert("Connection was closed.");
        connected = false;
        conn = null;
        document.getElementById("before-connection").classList.remove("nodisplay");
        document.getElementById("connected").classList.add("nodisplay");
    })
}

async function onDrop(e) {
    e.preventDefault();
    for (let i = 0; i < e.dataTransfer.files.length; i++) {
        uploadFile(e.dataTransfer.files[i]);
        await new Promise(resolve => setTimeout(resolve, 50));
    }
}

function updateFile() {
    var fullPath = document.getElementById('fileselect').value;
    var fileText = document.getElementById('filetext');
    fileText.innerHTML = fullPath.split(/(\\|\/)/g).pop();
}

function sendFile() {
    var fileInput = document.getElementById('fileselect');
    uploadFile(fileInput.files[0]);
}

let sending = false;

async function uploadFile(file) {
    if (!connected) return;
    while (sending) {
        await new Promise(resolve => setTimeout(resolve, 200));
    }
    sending = true;
    console.log(file.name);
    document.getElementById('current').innerHTML = file.name;

    conn.send(file.name);
    conn.send(file.type);
    conn.send(file.size);
    sliceSendFile(file);
}

function sliceSendFile(file) {
    const fileSize = file.size;
    let offset = 0;

    function readchunk() {
        const r = new FileReader();
        let blob = file.slice(offset, CHUNK_SIZE + offset);
        r.onload = function (evt) {
            if (!evt.target.error) {
                offset += CHUNK_SIZE;
                var percentComplete = Math.min((offset / fileSize) * 100, 100);
                meter.innerHTML = '<span style="width: VAR%"></span>'.replace('VAR', percentComplete);

                conn.send(evt.target.result);

                if (offset >= fileSize) { // Final chunk was written
                    sending = false;
                    document.getElementById('current').innerHTML = "None";
                    meter.innerHTML = '<span style="width: VAR%"></span>'.replace('VAR', 0);
                    return; 
                }
            } else {
                alert("Fatal read error: " + evt.target.error + ", please reload the page.");
                return;
            }
            readchunk();
        };
        r.readAsArrayBuffer(blob);
    }
    readchunk();
}

function finishTransfer(name, type, data) {
    let blob = new Blob(data, { type: type });
    let e = document.createEvent('MouseEvents');
    let a = document.createElement('a');

    a.download = name;
    a.href = window.URL.createObjectURL(blob);
    a.dataset.downloadurl = [type, a.download, a.href].join(':');
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(e);
}

const peer = new Peer(peerId);
peer.on('open', function(id) {
    if (HOST) {
        document.getElementById('stream-id').innerHTML = id;
        peer.on('connection', function (c) {
            conn = c;
            clientConnected();
        });
    } else {
        let msg = document.getElementById("connecting-msg");
        let query = window.location.pathname.split("/");
        let hostId = query[query.length - 2];
        conn = peer.connect(hostId);

        conn.on('open', function () {
            msg.innerHTML = "Connected. Waiting for files...";

            let name = null;
            let type = null;
            let size = 0;
            let filedata = [];
            let totalRec = 0;

            conn.on('data', function (data) {
                if (name == null) {
                    name = data;
                    msg.innerHTML = "Receiving " + name + "...";
                    meter.classList.remove("hidden");
                } else if (type == null) {
                    type = data;
                } else if (size == 0) {
                    size = data;
                } else {
                    filedata.push(new Uint8Array(data, 0, data.byteLength));
                    totalRec += data.byteLength;
                    let percentComplete = Math.min((totalRec / size) * 100, 100);
                    meter.innerHTML = '<span style="width: VAR%"></span>'.replace('VAR', percentComplete);

                    if (data.byteLength !== CHUNK_SIZE) {
                        finishTransfer(name, type, filedata);
                        name = null;
                        type = null;
                        size = 0;
                        totalRec = 0;
                        filedata = [];
                        msg.innerHTML = "Transfer finished. Waiting for more files...";
                        meter.classList.add("hidden");
                    }
                }
            });

            conn.on('close', function () {
                alert("Connection was closed.");
                msg.innerHTML = "Disconnected from sender. You can close the tab.";
            })
        })
    }
})
