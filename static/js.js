var textFromFileLoaded = params.get('lyrics');
console.log(textFromFileLoaded);
String.prototype.replaceAll = function(strTarget, strSubString){
  var strText = this;
  var intIndexOfMatch = strText.indexOf( strTarget );
  // Keep looping while an instance of the target string
  // still exists in the string.
  while (intIndexOfMatch != -1){
  // Relace out the current instance.
  strText = strText.replace( strTarget, strSubString )
  // Get the index of any next matching substring.
  intIndexOfMatch = strText.indexOf( strTarget );
  }
  // Return the updated string with ALL the target strings
  // replaced out with the new substring.
  return( strText );
}

document.getElementById('fileSong').addEventListener("change", handleFiles, false);
// ==================================================

function playSong() {
  var valSong = document.getElementById('fileSong').value;
  // var valLyric = document.getElementById('fileLyric').value;
  var actStartPause = document.querySelectorAll(".activeStartPause");

  // if (valSong == "" || valLyric == "") {
  //   alert("Please import Song or Lyric");
  //   return
  // }
  document.getElementById('audioSong').play();

  for (let i = 0; i < actStartPause.length; i++) {
    actStartPause[i].innerHTML = '<span onclick="pauseSong();" class="activeAction">Pause</span>';
  }
  setTimeout(function(){
  loadFileAsText();
  }, 500); 
  
}

function reloadPage(forceGet) {
  location.reload(forceGet);
}

function pauseSong() {
  document.getElementById("audioSong").pause();

  var actStartPause = document.querySelectorAll(".activeStartPause");
  for (let i = 0; i < actStartPause.length; i++) {
    actStartPause[i].innerHTML = '<span onclick="playSong();" class="activeAction">Start</span>';
  }
}


function formatCurrentTime(time) {
  var hr  = Math.floor(time / 3600);
  var minutes = Math.floor((time - (hr * 3600))/60);
  var seconds = Math.floor(time - (hr * 3600) - (minutes * 60));
  var ms = Math.floor(time * 1000);

  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  if (seconds < 10) {
    seconds = "0" + seconds;
  }
  if (ms < 10) { // 0
    ms = "0" + ms;
  }
  if (10 <= ms < 100) { //00
    var convMsToString = ms.toString().slice(0);
    ms = "0" + convMsToString;
  }
  if (100 <= ms < 1000) { //000
    var convMsToString = ms.toString().slice(-3, -1);
    ms = convMsToString;
  }
  return "[" + minutes + ':' + seconds + '.' + ms + "]";
}

function timeToInt(time) {
  var timeMinute = time.slice(1, 3);
  var timeSecond = time.slice(4, 6);
  var timeMs = time.slice(7, 9);
  var result = parseInt(timeMinute)+parseInt(timeSecond)+parseInt(timeMs);
  return result;
}

function parseTiming(time) {
  var initStart = time.replace("[", "");
  var initEnd = initStart.replace("]", "");
  return initEnd
}

// function loadFileAsText(){
//   var fileToLoad = document.getElementById("fileLyric").files[0];
//   var fileReader = new FileReader();
//   fileReader.onload = function(){
//     var textFromFileLoaded = ["[00:00.06]Bài hát: Gặp Gỡ, Yêu Đương Và Được Bên Em","[00:02.66]Ca sĩ: Phan Mạnh Quỳnh","[00:08.06]Bài hát: Gặp Gỡ, Yêu Đương Và Được Bên Em","[00:10.66]Ca sĩ: Phan Mạnh Quỳnh"];
//     // console.log(textFromFileLoaded);
//     var showLyricHtml = parseShowLyrics(textFromFileLoaded);
//     // console.log(showLyricHtml);
//     var addStyleLyric = new Array();
//     var linesongid = 1;
//     showLyricHtml.forEach(result => {
//       result = "<span class='lineRunLyric' id='linesongid"+ linesongid +"'>" +result[0] + "</span>";
//       linesongid++;
//       addStyleLyric.push(result);
//     })
//     addStyleLyric = "<p>" + addStyleLyric + "</p>";
//     addStyleLyric = addStyleLyric.replaceAll("</span><br />,<span", "</span><br /><span");
//     document.getElementById("inputTextToSave").innerHTML = addStyleLyric;

//     //Run Lyric
//     console.log(textFromFileLoaded);
//     runLyric(textFromFileLoaded);

//   };
//   fileReader.readAsText(fileToLoad, "UTF-8");
// }
function loadFileAsText(){
  var showLyricHtml = parseShowLyrics(textFromFileLoaded);
  var addStyleLyric = new Array();
  var linesongid = 1;
  showLyricHtml.forEach(result => {
    result = "<span class='lineRunLyric' id='linesongid"+ linesongid +"'>" +result[0] + "</span>";
    linesongid++;
    addStyleLyric.push(result);
  })
  addStyleLyric = "<p>" + addStyleLyric + "</p>";
  addStyleLyric = addStyleLyric.replaceAll("</span><br />,<span", "</span><br /><span");
  document.getElementById("inputTextToSave").innerHTML = addStyleLyric;
  runLyric(textFromFileLoaded);
}

function runLyric(str) {
  // clearInterval(intervalObj);
  var myAudio = document.getElementById("audioSong");
  var playSongButton = document.querySelectorAll(".activeStartPause");
  var fileSong = document.getElementById("fileSong");
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

  fileSong.addEventListener("change", function(){
    myAudio.currentTime = 0;
    var getCurrentTime = formatCurrentTime(myAudio.currentTime);
    var getDuration = formatCurrentTime(myAudio.duration);
    var showTiming = parseTiming(getCurrentTime);
    var showDuration = parseTiming(getDuration);
    var showCurTimeSong = document.querySelectorAll(".showCurrentTimeSong");
    for (let i = 0; i < showCurTimeSong.length; i++) {
      showCurTimeSong[i].innerHTML = showTiming+" / "+showDuration;
    }
    clearInterval(intervalObj);
    textFromFileLoaded = "";
    document.getElementById("inputTextToSave").innerHTML = "<p><p>"
    console.log("clearInterval3");
  });

  // fileLyric.addEventListener("change", function(){
  //   myAudio.pause();
  //   myAudio.currentTime = 0;
  //   var getCurrentTime = formatCurrentTime(myAudio.currentTime);
  //   var getDuration = formatCurrentTime(myAudio.duration);
  //   var showTiming = parseTiming(getCurrentTime);
  //   var showDuration = parseTiming(getDuration);
  //   var showCurTimeSong = document.querySelectorAll(".showCurrentTimeSong");
  //   for (let i = 0; i < showCurTimeSong.length; i++) {
  //     showCurTimeSong[i].innerHTML = showTiming+" / "+showDuration;
  //   }
  //   clearInterval(intervalObj);
  //   console.log("clearInterval4");
  // });


  myAudio.addEventListener("ended", function(){
    console.log(str);
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

    var getCurrentTime = formatCurrentTime(myAudio.currentTime);
    var getDuration = formatCurrentTime(myAudio.duration);
    var showTiming = parseTiming(getCurrentTime);
    var showDuration = parseTiming(getDuration);
    var timeLyric = parseLyrics(str);
    var showCurTimeSong = document.querySelectorAll(".showCurrentTimeSong");
    for (let i = 0; i < showCurTimeSong.length; i++) {
      showCurTimeSong[i].innerHTML = showTiming+" / "+showDuration;
    }

    if (myAudio.currentTime == 0) {
      for (var index = 1; index <= timeLyric.length; index++) {
        var lineLyric = document.getElementById("linesongid"+index);
        lineLyric.style.color = "black";
      }
    }
    // console.log(timeLyric);
    var linesongidBE = 1;
    timeLyric.forEach(result => {
      switch (result[0]) {
        case getCurrentTime:
          var lineLyricChange;
          var totalLyric = parseLyrics(str).length;
          console.log("fsdfds");
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
          lineLyricStart.style.color = "blue";
          if (lineLyricPass) {
            lineLyricPass.style.color = "#8d6e63";
          }
          // window.scrollBy(0, 10);
          break;
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
    var startToReplace = element.slice(0, 10).toString();
    var endToReplace = element.slice(10).toString();
    var setSplit = ",,,,,,,, ,,,,,"
    element = startToReplace + setSplit + endToReplace;
    var createArr = element.split(setSplit)
    newArr.push(createArr);
  });
  
  var newArr1 = new Array();
  newArr.forEach(result => {
    if (result[1] !== "") {
      newArr1.push(result)
    }
  });
  return newArr1;
}

function parseShowLyrics(lyricImport) {
  var showLyricHtml = parseLyrics(lyricImport)
  var newArr = new Array();
  showLyricHtml.forEach(result => {
    result.shift();
    newArr.push(result);
  })
  return newArr;
}
