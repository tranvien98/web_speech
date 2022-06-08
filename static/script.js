//webkitURL is deprecated but nevertheless
// shim for AudioContext when it's not avb. 

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

let websocket_uri = 'ws://localhost:8080';
let end_text = "";
let end_time = 0;
let href = "#";
let bufferSize = 2048,
    AudioContext,
    context,
    processor,
    input,
    globalStream,
    websocket;
//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
// pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    initWebSocket();
    console.log("recordButton clicked");
    textFromFileLoaded = [];
    end_text = "";
    end_time = 0;
    var constraints = { audio: true, video:false }
    recordButton.disabled = true;
    recordButton.style.backgroundColor = "blue";
    // recordButton.disabled = true;
    href = "#";
    stopButton.disabled = false;
    stopButton.style.backgroundColor = "red";
    stopButton.disabled = false;
    // pauseButton.disabled = false;
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
        try {
          websocket.send(left16);
        } catch (error) {
          // processor.onaudioprocess = null;
        }
       
      };
    };
    navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(handleSuccess)
}
/*
function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        //pause
        rec.stop();
        pauseButton.innerHTML="Tiếp tục";
    }else{
        //resume
        rec.record()
        pauseButton.innerHTML="Tạm Dừng";
    }
}
*/
function stopRecording() {
    processor.onaudioprocess = null;
    
    console.log("stopButton clicked");
    globalStream.getAudioTracks()[0].stop();
    websocket.send({"eof" : 1});
    websocket.close();
    // rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
    var au = document.getElementById("audio_record");


    //name of .wav file to use during upload and download (without extendion)
    var datetime = new Date;
    var filename = Math.floor(Date.now()).toString();
    filename = 'record-'+filename+'.wav';
    //add controls to the <audio> element
    au.controls = true;
    au.src = url;
    console.log(url);
}

function jsUcfirst(string) 
// viet hoa chu dau
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}


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
      var myAudio = document.getElementById("audio_record");
      var sourceAudio = document.getElementById("wav_audio_record");
      var saveToFile =  document.getElementById("saveToFile");
      var dowloadFileAudio = document.getElementById("dowloadFileAudio");
      var dowloadFileDoc = document.getElementById("dowloadFileDoc");
      stopButton.disabled = true;
      stopButton.style.backgroundColor = "blue";
      sourceAudio.src = href;
      myAudio.load();
      recordButton.disabled = false;
      recordButton.style.backgroundColor = "red";

      myAudio.onloadedmetadata = function() {
                  
        if (end_text !== ""){
          lyric_ele = '[' + end_time+ ',' + myAudio.duration + ']' + end_text;
          end_text = "";
          textFromFileLoaded.push(lyric_ele);
        }
        loadFileAsText();
        $.ajax({
          url: '/api/record_upload',
          type: 'post',
          data: JSON.stringify( { 
            'lyrics': textFromFileLoaded, 
            'path_file': "./static" + sourceAudio.src.split("static")[1],
            'duration': myAudio.duration
          }),
          contentType: "application/json; charset=utf-8",
          processData: false,
          success: function(response){
            console.log(response['id_audio']);
            saveToFile.href = "/edit?id_audio=" + response['id_audio'];
            dowloadFileAudio.href = "/export-files/" + response['id_audio'];
            dowloadFileDoc.href = "/export-doc/" + response['id_audio'];
          },
          error: function (response) {
              Toast.fire({
                  icon: 'error',
                  title: response.responseText
              })
          }
          });
      };

      console.log("connection closed (" + e.code + ")");
      // document.getElementById("webSocketStatus").innerHTML = 'Not Connected';
    }
    var sentense=''
    websocket.onmessage = function(e) {
      //console.log("message received: " + e.data);
      // console.log(e.data);
  
      try {
        result = JSON.parse(e.data);
        // console.log(result)
        if (result['text'] !==undefined && result['text']!==''){
          // var au = document.getElementById("audio_record");
          // var sourceAu = document.getElementById("wav_audio_record");
          // sourceAu.src = result["name_file"];
          // document.querySelector('audio').load();
          href = result["name_file"];
          end_text = "";
          end_time = result['result'][result['result'].length-1]["end"]
          console.log('========');
          lyric_ele = '[' +result['result'][0]["start"]+ ',' + result['result'][result['result'].length-1]["end"]  + ']' + jsUcfirst(result['text']);
          console.log(lyric_ele);
          textFromFileLoaded.push(lyric_ele);
          sentense= sentense + result['text'].toLowerCase().charAt(0).toUpperCase() + result['text'].toLowerCase().slice(1)+'. ';
        }
        if (result['partial']!=='' && result['text'] ==undefined) {
          // var tag=document.createElement('p').appendChild(document.createTextNode(e.data['partial']))
          // // =e.data
          // var element = document.getElementById("new");
          // element.appendChild(tag);
          end_text = jsUcfirst(result['partial']);
          href = result["name_file"];
          console.log(result['partial']);
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

var Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 5000
});

var textFromFileLoaded = [];
var spellMistake = [] ;
loadFileAsText()
function playSong() {
//   var valSong = document.getElementById('fileSong').value;
  // var valLyric = document.getElementById('fileLyric').value;
  var actStartPause = document.querySelectorAll(".activeStartPause");

  // if (valSong == "" || valLyric == "") {
  //   alert("Please import Song or Lyric");
  //   return
  // }
  document.getElementById('audio_record').play();

  for (let i = 0; i < actStartPause.length; i++) {
    actStartPause[i].innerHTML = '<span onclick="pauseSong();"  style="background-color: red" class="activeAction">Dừng</span>';
  }
  setTimeout(function(){
  loadFileAsText();
  }, 200); 
  
}
function pauseSong() {
  document.getElementById("audio_record").pause();

  var actStartPause = document.querySelectorAll(".activeStartPause");
  for (let i = 0; i < actStartPause.length; i++) {
    actStartPause[i].innerHTML = '<span onclick="playSong();" class="activeAction">Phát</span>';
  }
}

function check_song(){
    var au = document.getElementById('audio_record');
    var src = au.src;
    console.log(src)
    if (src.length < 1){
        Toast.fire({
        title: 'Bạn chưa ghi âm!',
        icon: 'error'
        });
        return false;
    };
    Toast.fire({
    title: 'Đang tiến hành nhận dạng!',
    icon: 'info',
    })
    return true;
}
function check_valid() {
  if(textFromFileLoaded.length > 0){
    console.log("true");
    return true
  }
  Toast.fire({
  title: ' Đoạn văn bản nhận dạng trống !',
  icon: 'error',
    })
  return false;
}
function loadFileAsText(){
  var showLyricHtml = parseShowLyrics(textFromFileLoaded);
  var addStyleLyric = new Array();
  var linesongid = 1;
  // console.log(showLyricHtml);
  showLyricHtml = addHighlight(showLyricHtml, spellMistake);
  showLyricHtml.forEach(result => {
    result = "<span class='lineRunLyric' id='linesongid"+ linesongid +"'>" + jsUcfirst(result[2]) + "."+"</span>";
    // console.log(result);
    linesongid++;
    addStyleLyric.push(result);
    // console.log(addStyleLyric);
  })

  addStyleLyric = "<p>" + addStyleLyric.join(" ") + "</p>";
  // console.log(addStyleLyric);
  addStyleLyric = addStyleLyric.replaceAll("</span><br />,<span", "</span><br /><span");
  document.getElementById("inputTextToSave").innerHTML = addStyleLyric;
  runLyric(textFromFileLoaded);
}

function addHighlight(text, spellMistake){
  spellMistake.forEach(result => {
    // console.log(result);
    reText = text[result['sentence']][2];
    text[result['sentence']][2] = reText.substring(0, result['start_index']) + "<span class='highlight'>" + 
      reText.substring(result['start_index'],result['end_index']) + "</span>" + reText.substring(result['end_index'], reText.length);
    // console.log(text[result['sentence']][2]);
  }
  )
  return text;
}


function runLyric(str) {
  // clearInterval(intervalObj);
  var myAudio = document.getElementById("audio_record");
  var playSongButton = document.querySelectorAll(".activeStartPause");
  var fileLyric = document.getElementById("fileLyric");
  var actStop = document.querySelectorAll(".activeStop");

  // debugger;
  for (let i = 0; i < playSongButton.length; i++) {
    playSongButton[i].addEventListener("click", function(){
      clearInterval(intervalObj);
      console.log("clearInterval1");
    });
  }

  for (let i = 0; i < actStop.length; i++) {
    actStop[i].addEventListener("click", function(){
      var timeLyric = parseLyrics(str);
      var totalLyric = timeLyric.length;
      for (var index = 1; index <= totalLyric; index++) {
        var lineLyric = document.getElementById("linesongid"+index);
        lineLyric.style.color = "black";
      }
      clearInterval(intervalObj);
      console.log("clearInterval2");
    });
  }

  myAudio.addEventListener("ended", function(){
    // console.log(str);
    var timeLyric = parseLyrics(str);
    var totalLyric = timeLyric.length;
    for (var index = 1; index <= totalLyric; index++) {
      var lineLyric = document.getElementById("linesongid"+index);
      lineLyric.style.color = "black";
    }

    var actStartPause = document.querySelectorAll(".activeStartPause");
    for (let i = 0; i < actStartPause.length; i++) {
      actStartPause[i].innerHTML = '<span onclick="playSong();" class="activeAction">Start</span>';
    }
    clearInterval(intervalObj);
    console.log("clearInterval5");
  });
  // console.log("fsdfds");
  var intervalObj = setInterval(function(){

    var getCurrentTime = parseFloat(myAudio.currentTime);
    var timeLyric = parseLyrics(str);
    var showCurTimeSong = document.querySelectorAll(".showCurrentTimeSong");

    if (myAudio.currentTime == 0) {
      for (var index = 1; index <= timeLyric.length; index++) {
        var lineLyric = document.getElementById("linesongid"+index);
        if (lineLyric !== null){
          lineLyric.style.color = "black";
        }
      }
    }
    // console.log(timeLyric);
    var linesongidBE = 1;
    timeLyric.forEach(result => {
      start = parseFloat(result[0]);
      end = parseFloat(result[1]);
      if (getCurrentTime > start){
        var lineLyricChange;
        var totalLyric = parseLyrics(str).length;
        // console.log(totalLyric);
        for (let index = 1; index < linesongidBE; index++) {
          lineLyricChange = document.getElementById("linesongid"+index);
          lineLyricChange.style.color = "#8d6e63";
          
        }
        for (let index = (linesongidBE+1); index <= totalLyric; index++) {
          lineLyricChange = document.getElementById("linesongid"+index);
          lineLyricChange.style.color = "black";
        }

        var lineLyricStart = document.getElementById("linesongid"+linesongidBE);
        var lineLyricPass = document.getElementById("linesongid"+(linesongidBE -1))
        lineLyricStart.style.color = "#FF4000";
        // lineLyricStart.style.fontWeight = "bold";
        if (lineLyricPass) {
          lineLyricPass.style.color = "#8d6e63";
          // lineLyricPass.style.fontWeight = "normal";
        }
        };
      linesongidBE++;
    });
  }, 5)
}

function simpleFormat(str) {
  str = str.replace(/\r\n?/, "\n");
  str = $.trim(str);
  if (str.length > 0) {
    str = str.replace(/\n\n+/g, '</p><p>');
    str = str.replace(/\n/g, '<br />');
    str = '<p>' + str + '</p>';
  }
  return str;
}

function handleFiles(event) {
	var files = event.target.files;
  $("#srcSong").attr("src", URL.createObjectURL(files[0]));
  document.getElementById("audioSong").load();

  var actStartPause = document.querySelectorAll(".activeStartPause");
  for (let i = 0; i < actStartPause.length; i++) {
    actStartPause[i].innerHTML = '<span onclick="playSong();" class="activeAction">Start</span>';
  }
}

function parseLyrics(lyricImport) {
  // var parseLyrics = simpleFormat(lyricImport)
  // parseLyrics = parseLyrics.replaceAll("<p>", "");
  // parseLyrics = parseLyrics.replaceAll("</p>", "");
  var sPlit = lyricImport

  var newArr = new Array();
  sPlit.forEach(element => {
    var array_lyrics = element.split(']')
    var array_time = array_lyrics[0].split(',')
    var start_time = array_time[0].replace('[', '')
    var end_time = array_time[1].replace(']', '')
    var lyric = array_lyrics[1]
    var setSplit = ",,,.,,,"
    element = start_time + setSplit + end_time + setSplit + lyric;

    var createArr = element.split(setSplit);
    newArr.push(createArr);
  });
  
  var newArr1 = new Array();
  newArr.forEach(result => {
    if (result[2] !== "") {
      newArr1.push(result)
    }
  });
  return newArr1;
}

function parseShowLyrics(lyricImport) {
  var showLyricHtml = parseLyrics(lyricImport);
  // console.log(showLyricHtml);
  // console.log(newArr);
  return showLyricHtml;
}