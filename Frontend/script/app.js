const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

/*const clearClassList = function (el) {
  el.classList.remove("c-room--wait");
  el.classList.remove("c-room--on");
};

const listenToUI = function () {
  const knoppen = document.querySelectorAll(".js-power-btn");
  for (const knop of knoppen) {
    knop.addEventListener("click", function () {
      const id = this.dataset.idlamp;
      let nieuweStatus;
      if (this.dataset.statuslamp == 0) {
        nieuweStatus = 1;
      } else {
        nieuweStatus = 0;
      }
      //const statusOmgekeerd = !status;
      clearClassList(document.querySelector(`.js-room[data-idlamp="${id}"]`));
      document.querySelector(`.js-room[data-idlamp="${id}"]`).classList.add("c-room--wait");
      socket.emit("F2B_switch_light", { lamp_id: id, new_status: nieuweStatus });
    });
  }
};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_status_lampen", function (jsonObject) {
    console.log("alle lampen zijn automatisch uitgezet");
    console.log("Dit is de status van de lampen");
    console.log(jsonObject);
    for (const lamp of jsonObject.lampen) {
      const room = document.querySelector(`.js-room[data-idlamp="${lamp.id}"]`);
      if (room) {
        const knop = room.querySelector(".js-power-btn");
        knop.dataset.statuslamp = lamp.status;
        clearClassList(room);
        if (lamp.status == 1) {
          room.classList.add("c-room--on");
        }
      }
    }
  });

  socket.on("B2F_verandering_lamp", function (jsonObject) {
    console.log("Er is een status van een lamp veranderd");
    console.log(jsonObject.lamp.id);
    console.log(jsonObject.lamp.status);

    const room = document.querySelector(`.js-room[data-idlamp="${jsonObject.lamp.id}"]`);
    if (room) {
      const knop = room.querySelector(".js-power-btn"); //spreek de room, als start. Zodat je enkel knop krijgt die in de room staat
      knop.dataset.statuslamp = jsonObject.lamp.status;

      clearClassList(room);
      if (jsonObject.lamp.status == 1) {
        room.classList.add("c-room--on");
      }
    }
  });
  socket.on("B2F_verandering_lamp_from_HRDWR", function (jsonObject) {
    console.log(jsonObject)
  });

};
*/

const listenToUI = function () {
  const knoppen = document.querySelectorAll(".js-toestand-btn");
  
  for (const knop of knoppen) {
    knop.addEventListener("click", function () {
      console.log("knop geklikt")
      const naam = "motor";
      let nieuweStatus;
      nieuweStatus = knop.getAttribute('data-typeid');
      
      
      socket.emit("F2B_switch_motor", { Naam: naam, nieuwe_toestand: nieuweStatus });
      
    });
  }
  
};

const drawChart = function(labels, data){

  const options = {
      chart: {
          id: 'histogram-js',
          type: 'area',
      },
      stroke:{
          curve: 'smooth'
      },
      dataLabels:{
          enabled: false
      },
      series:[
          {
              name: 'data',
              data: data,
          },
      ],
      labels: labels,
      yaxis: {
        labels: {
          formatter: function (value) {
            return value;
          }
        },
      },
      xaxis: {
        type: 'datetime',
      },
      noData:{
          text: 'Loading...'
      }
      
  };


  const chart = new ApexCharts(document.querySelector('.histogram-js'), options);
  chart.render();
}

const showTemperatuurData = function(jsonObject){
  data = jsonObject.types
  console.log(data);

  let converted_labels = [];
  let converted_data = [];
  for(const item of data){
      converted_labels.push((item.Tijd));
      converted_data.push((item.Meting + item.MeetEenheid));

  }
  drawChart(converted_labels, converted_data)
}


const listenToClickHistogram = function () {
  
  const buttons = document.querySelectorAll('.js-filter');
  for (const b of buttons) {
    b.addEventListener('click', function () {
      console.log('click filter');
      console.log(b.getAttribute('data-typeid'))
      currentTypeID = b.getAttribute('data-typeid');
      console.log('info ' + currentTypeID);
      handleData(`http://192.168.168.168:5000/api/v1/${currentTypeID}`, showTemperatuurData);
    });
  }
};







const showSensorData = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      html += `<div class"data_container"><h1 class="data_title">Data:</h1>
      <p class="data_paragraph">MetingID: ${element.dataID}</p><br>
      <p class="data_paragraph">Meting: ${element.Meting}</p><br>
      <p class="data_paragraph">MeetEenheid: ${element.MeetEenheid}</p><br>
      <p class="data_paragraph">MetingsTijd: ${element.Tijd}</p><br>
      </div>`;
    }
}
  
  htmlSensorData.innerHTML = html;
};

const showLuna = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      html += `
      <div class="data_row">
        <div>
            <p>Luna ging naar ${element.knop}</p>
        </div>
        <div>
            <p>op ${element.Tijd}</p>
        </div>
      </div>`;
    }
  }

  htmlLuna.innerHTML = html;
};

const showMona = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      html += `
      <div class="data_row">
        <div>
            <p>Mona ging naar ${element.knop}</p>
        </div>
        <div>
            <p>op ${element.Tijd}</p>
        </div>
      </div>`;
    }
  }

  htmlMona.innerHTML = html;
};

const showMonaToestand = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      if(element.knop == "Buiten"){
        html += `
          <img src="./images/beach-icon.png" width="25px" height="25px" alt="beach">
          <p class="plaats_subtitle">${element.knop}</p>`;
      }else{
        html += `
          <img src="./images/home-icon.png" width="25px" height="25px" alt="beach">
          <p class="plaats_subtitle">${element.knop}</p>`;
      }
    }
  }
  htmlMonaToestand.innerHTML = html;
};

const showLunaToestand = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      if(element.knop == "Buiten"){
        html += `
          <img src="./images/beach-icon.png" width="25px" height="25px" alt="beach">
          <p class="plaats_subtitle">${element.knop}</p>`;
      }else{
        html += `
          <img src="./images/home-icon.png" width="25px" height="25px" alt="beach">
          <p class="plaats_subtitle">${element.knop}</p>`;
      }
    }
  }
  htmlLunaToestand.innerHTML = html;
};

const showToestand = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  data = jsonObject.types
      if(data['Toestand'] == "1"){
        html += `<img src="./images/checkmark-icon.png" alt="check" width="25px" height="25px"><p class="toestand_small_text">Volledig gesloten</p>`;
      }else if(data['Toestand'] == "2"){
        html += `<img src="./images/checkmark-icon.png" alt="check" width="25px" height="25px"><p class="toestand_small_text">Volledig open</p>`;
      }else if(data['Toestand'] == "3"){
        html += `<img src="./images/checkmark-icon.png" alt="check" width="25px" height="25px"><p class="toestand_small_text">Enkel buiten</p>`;
      }else if(data['Toestand'] == "4"){
        html += `<img src="./images/checkmark-icon.png" alt="check" width="25px" height="25px"><p class="toestand_small_text">Enkel binnen</p>`;
      }
      
    
  htmlToestand.innerHTML = html;
};


const showLatestTemperatuur = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  let html2 = '';
  
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      if(element.Meting <10){
        html+= `<h2>Het is buiten redelijk koud</h2>`;
        html2 += "./images/winter-icon.png";
      }else{
        html+= `<h2>Het is buiten warm genoeg</h2>`;
        html2 += "./images/sun-icon.png";
      }
    }
}
  
htmlWeatherStatusTemp.innerHTML = html;
htmlWeatherStatusTempIcon.src = html2;
};

const showLatestLicht = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  let html2 = '';
  
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      if(element.Meting <20){
        html+= `<h2>Het is buiten donker</h2>`;
        html2 += "./images/night-icon.png";
      }else{
        html+= `<h2>Het is buiten licht</h2>`;
        html2 += "./images/sun-icon.png";
      }
    }
}
  
htmlWeatherStatusLicht.innerHTML = html;
htmlWeatherStatusLichtIcon.src = html2;
};

const showLatestLuchtvochtigheid = function (jsonObject) {
  console.log(jsonObject.types);
  let html = '';
  let html2 = '';
  
  data = jsonObject.types
  for (index = 0; index < data.length; index++) {
    for (let element of data) {
      if(element.Meting <60){
        html+= `<h2>Het is buiten droog</h2>`;
        html2 += "./images/sun-icon.png";
      }else{
        html+= `<h2>Het is buiten redelijk nat</h2>`;
        html2 += "./images/rain-icon.png";
      }
    }
}
  
htmlWeatherStatusLuchtvochtigheid.innerHTML = html;
htmlWeatherStatusLuchtvochtigheidIcon.src = html2;
};

const getSensorData = function () {
  handleData('http://192.168.168.168:5000/api/v1/dht11', showSensorData);
};

const getLatestTemperatuur = function () {
  handleData('http://192.168.168.168:5000/api/v1/recent/temperatuur', showLatestTemperatuur);
};
const getLatestLicht = function () {
  handleData('http://192.168.168.168:5000/api/v1/recent/licht', showLatestLicht);
};
const getLatestLuchtvochtigheid = function () {
  handleData('http://192.168.168.168:5000/api/v1/recent/luchtvochtigheid', showLatestLuchtvochtigheid);
};
socket.on("B2F_updated_motor", function () {
  getToestand();

});
const getToestand = function () {
  handleData('http://192.168.168.168:5000/api/v1/toestand', showToestand);
};

const getLuna = function () {
  handleData('http://192.168.168.168:5000/api/v1/luna', showLuna);
};

const getLunaToestand = function () {
  handleData('http://192.168.168.168:5000/api/v1/luna/toestand', showLunaToestand);
};

const getMona = function () {
  handleData('http://192.168.168.168:5000/api/v1/mona', showMona);
};

const getMonaToestand = function () {
  handleData('http://192.168.168.168:5000/api/v1/mona/toestand', showMonaToestand);
};




document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  //htmlSensorData = document.querySelector('.container')
  htmlWeatherStatusTemp = document.querySelector('.js-weather_status--temp');
  htmlWeatherStatusTempIcon = document.getElementById("js-weather_status--icon-temp");
  htmlWeatherStatusLicht = document.querySelector('.js-weather_status--licht');
  htmlWeatherStatusLichtIcon = document.getElementById("js-weather_status--icon-licht");
  htmlWeatherStatusLuchtvochtigheid = document.querySelector('.js-weather_status--lucht');
  htmlWeatherStatusLuchtvochtigheidIcon = document.getElementById("js-weather_status--icon-lucht");
  htmlToestand = document.querySelector('.js-toestand');
  htmlLuna = document.querySelector('.js-data-container-luna');
  htmlMona = document.querySelector('.js-data-container-mona');
  htmlMonaToestand = document.querySelector('.js-plaats-mona')
  htmlLunaToestand = document.querySelector('.js-plaats-luna')
  
  
  
  //getSensorData()
  listenToClickHistogram();
  listenToUI();
  getLatestTemperatuur();
  getLatestLicht();
  getLatestLuchtvochtigheid();
  getToestand();
  getMona();
  getLuna();
  getMonaToestand();
  getLunaToestand();
});
