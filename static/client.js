//================= CONFIG =================
// Global Variables

// var recordButton = document.getElementById("recordButton");
// recordButton.addEventListener("click", startRecording);
const micBtn = document.getElementById("mic-btn");
const micBtnIcon = document.getElementById("mic-btn-icon");

const micBtnLoader = document.getElementById("mic-btn-loader");
// micBtn.addEventListener("click", startRecording);
let websocket_uri = 'ws://localhost:8080';
let bufferSize = 2048,
    AudioContext,
    context,
    processor,
    input,
    globalStream,
    websocket;

// Initialize WebSocket
// initWebSocket();

//================= RECORDING =================
function startRecording() {
    initWebSocket()
    streamStreaming = true;
    isMicOn = true;
    toggleLoadingUI(false);
    toggleRecordingUI(true);
    // toggleInteractiveUI(false);
    // toggleLoadingUI(true);
    AudioContext = window.AudioContext || window.webkitAudioContext;
    context = new AudioContext({
      // if Non-interactive, use 'playback' or 'balanced' // https://developer.mozilla.org/en-US/docs/Web/API/AudioContextLatencyCategory
      latencyHint: 'interactive',
    });
    processor = context.createScriptProcessor(bufferSize, 1, 1);
    processor.connect(context.destination);
    context.resume();
  
    var handleSuccess = function (stream) {
      globalStream = stream;
      input = context.createMediaStreamSource(stream);
      input.connect(processor);
  
      processor.onaudioprocess = function (e) {
        var left = e.inputBuffer.getChannelData(0);
        var left16 = downsampleBuffer(left, 44100, 16000);
        websocket.send(left16);
      };
    };
  
    navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(handleSuccess);
} // closes function startRecording()

function stopRecording() {
    streamStreaming = false;
  
    // let track = globalStream.getTracks()[0];
    // track.stop();
    isMicOn=false
    toggleLoadingUI(false);
    toggleRecordingUI(false);
    input.disconnect(processor);
    processor.disconnect(context.destination);
    context.close().then(function () {
      input = null;
      processor = null;
      context = null;
      AudioContext = null;
    });
} // closes function stopRecording()
function toggleLoadingUI(isLoading) {
  if (isLoading) {
    micBtnIcon.classList.add("hide");
    micBtnLoader.classList.remove("hide");
  } else {
    micBtnIcon.classList.remove("hide");
    micBtnLoader.classList.add("hide");
  }
}
function toggleRecordingUI(isRecording) {
  if (isRecording) {
    // transcript.classList.add("recording");
    micBtn.classList.add("recording");
  } else {
    micBtn.classList.remove("recording");
  }
}
function toggleInteractiveUI(isEnabled) {
  // transcriptFormattedOption.disabled = !isEnabled;
  // partialOption.disabled = !isEnabled;
  // uriInput.disabled = !isEnabled;
  // extraOptions.disabled = !isEnabled;

  if (isEnabled) {
    basicOptionsContainer.classList.remove("disabled");
  } else {
    basicOptionsContainer.classList.add("disabled");
  }
}


let isMicOn = false;
micBtn.addEventListener("click", async () => {
  if (isMicOn) {
    stopRecording();
  } else {
    startRecording();
  }
});


function initWebSocket() {
    // Create WebSocket
    websocket = new WebSocket(websocket_uri);
    //console.log("Websocket created...");
  
    // WebSocket Definitions: executed when triggered webSocketStatus
    websocket.onopen = function() {
      console.log("connected to server");
      //websocket.send("CONNECTED TO YOU");
      // document.getElementById("webSocketStatus").innerHTML = 'Connected';

    }
    
    websocket.onclose = function(e) {
      console.log("connection closed (" + e.code + ")");
      document.getElementById("webSocketStatus").innerHTML = 'Not Connected';
    }
    var sentense=''
    websocket.onmessage = function(e) {
      //console.log("message received: " + e.data);
      // console.log(e.data);
  
      try {
        result = JSON.parse(e.data);
        if (result['text'] !==undefined && result['text']!==''){
          console.log('========')
          console.log(result['text'])
          sentense=sentense+result['text'].toLowerCase().charAt(0).toUpperCase()+result['text'].toLowerCase().slice(1)+'. '
        }
        if (result['partial']!=='' && result['text'] ==undefined) {
          // var tag=document.createElement('p').appendChild(document.createTextNode(e.data['partial']))
          // // =e.data
          // var element = document.getElementById("new");
          // element.appendChild(tag);
          console.log(result['partial'])
          // var tag = document.createElement("p");
          // var text = document.createTextNode(result['partial']);
          // tag.appendChild(text);
          var element = document.querySelector("#inputTextToSave");
          element.innerHTML = '';
          element.appendChild(document.createTextNode((sentense+result['partial'].toLowerCase())));
        }
      }  catch (e) {
        $('.message').html('Error retrieving data: ' + e);
      }
  
      if (typeof(result) !== 'undefined' && typeof(result.error) !== 'undefined') {
        $('.message').html('Error: ' + result.error);
      }
      else {
        $('.message').html('Welcome!');
      }
    }
} // closes function initWebSocket()

function downsampleBuffer (buffer, sampleRate, outSampleRate) {
    if (outSampleRate == sampleRate) {
      return buffer;
    }
    if (outSampleRate > sampleRate) {
      throw 'downsampling rate show be smaller than original sample rate';
    }
    var sampleRateRatio = sampleRate / outSampleRate;
    var newLength = Math.round(buffer.length / sampleRateRatio);
    var result = new Int16Array(newLength);
    var offsetResult = 0;
    var offsetBuffer = 0;
    while (offsetResult < result.length) {
      var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
      var accum = 0,
        count = 0;
      for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
        accum += buffer[i];
        count++;
      }
  
      result[offsetResult] = Math.min(1, accum / count) * 0x7fff;
      offsetResult++;
      offsetBuffer = nextOffsetBuffer;
    }
    return result.buffer;
} // closes function downsampleBuffer()
