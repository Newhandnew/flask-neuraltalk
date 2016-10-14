/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

'use strict';

var videoElement = document.querySelector('video');
var videoSelect = document.querySelector('select#videoSource');

function gotDevices(deviceInfos) {
  // Handles being called several times to update labels. Preserve values.
  while (videoSelect.firstChild) {
    select.removeChild(select.firstChild);
  }
  for (var i = 0; i !== deviceInfos.length; ++i) {
    var deviceInfo = deviceInfos[i];
    var option = document.createElement('option');
    option.value = deviceInfo.deviceId;
    if (deviceInfo.kind === 'videoinput') {
      option.text = deviceInfo.label || 'camera ' + (videoSelect.length + 1);
      videoSelect.appendChild(option);
    } else {
      console.log('Some other kind of source/device: ', deviceInfo);
    }
  }
  if (Array.prototype.slice.call(videoSelect.childNodes).some(function(n) {
    return n.value === values[videoSelect];
  })) {
    videoSelect.value = values[videoSelect];
  }
}

navigator.mediaDevices.enumerateDevices()
.then(gotDevices)
.catch(errorCallback);

function errorCallback(error) {
  console.log('navigator.getUserMedia error: ', error);
}

function start() {
  if (window.stream) {
    window.stream.getTracks().forEach(function(track) {
      track.stop();
    });
  }
  var videoSource = videoSelect.value;
  var constraints = {
    video: {deviceId: videoSource ? {exact: videoSource} : undefined}
  };
  navigator.mediaDevices.getUserMedia(constraints)
  .then(function(stream) {
    window.stream = stream; // make stream available to console
    videoElement.srcObject = stream;
    // Refresh button list in case labels have become available
    return navigator.mediaDevices.enumerateDevices();
  })
  .then(gotDevices)
  .catch(errorCallback);
}

var canvas = window.canvas = document.querySelector('canvas');
canvas.width = 480;
canvas.height = 360;

var button = document.querySelector('#btn_takeSnap');
button.onclick = function() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  var dataURL = canvas.toDataURL();
  $.ajax({
    type: "POST",
    url: "/camera",
    data: {
      base64img: dataURL
    },
    success: function(resp){
      var pending_hash = resp.uuid;     // get relate uuid
      console.log(pending_hash);
      var fDone = 0;
      var numCheck = 0;
      var checkLimit = 5;
      (function getResult() {
        $.ajax({
          url: "/caption/"+pending_hash,
          success: function(resp) {
            var result = resp.caption;
            console.log(result);
            $("#caption").css('color', 'blue');
            $("#caption").text(result);
            fDone = 1;
          },
          error: function(jqXHR, textStatus, errorThrown) { 
            if(jqXHR.status == 404 || errorThrown == 'Not Found') 
            { 
              $("#caption").css('color', 'orange');
              $("#caption").text('waiting....'); 
              numCheck += 1;
            }
          },
          complete: function() {
            // Schedule the next request when the current one's complete
            if (fDone){}
            else if (numCheck < checkLimit) {
              setTimeout(getResult, 2000);
            }
            else if (numCheck >= checkLimit) {
              $("#caption").css('color', 'red');
              $("#caption").text('too many pictures'); 
            }
          }
        });
      })();
    },
    error: function(jqXHR, textStatus, errorThrown) { 
      if(jqXHR.status == 404 || errorThrown == 'Not Found') 
      { 
        $("#caption").css('color', 'red');
        $("#caption").text('server is busy!'); 
      }
    }
  })
};

videoSelect.onchange = start;

start();
