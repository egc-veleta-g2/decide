var ctx1 = document.getElementById("bar-resultados").getContext("2d");
var ctx2 = document.getElementById("pie-porcentaje").getContext("2d");

var votacion = JSON.parse(document.getElementById("votacion").value);
var lista = votacion.postproc;
var votos = [];
var etiquetas = [];
var porVotosPorOpcion = [];
var totalVotos = 0;

var listaBackgroundColor = ["rgba(255, 99, 132, 0.4)",
"rgba(255, 159, 64, 0.4)",
"rgba(255, 205, 86, 0.4)",
"rgba(75, 192, 192, 0.4)",
"rgba(54, 162, 235, 0.4)",
"rgba(153, 102, 255, 0.4)",
"rgba(201, 203, 207, 0.4)"];

var listaBorderColor = ["rgb(255, 99, 132)",
"rgb(255, 159, 64)",
"rgb(255, 205, 86)",
"rgb(75, 192, 192)",
"rgb(54, 162, 235)",
"rgb(153, 102, 255)",
"rgb(201, 203, 207)"];

for(let i=0; i< lista.length ; i++){
    votos[i] = lista[i].votes;
    etiquetas[i] = lista[i].option;
    totalVotos += lista[i].votes;
}

for(let i=0; i< votos.length ; i++){
    if(votos[i] !== 0 && totalVotos !== 0){
        porVotosPorOpcion[i] = (votos[i]/totalVotos)*100;
    } else {
        porVotosPorOpcion[i] = votos[i];
    }
}

/*global Chart*/

var config1 = new Chart(ctx1, {
    type: "bar",
    data: {
        datasets: [{
            label: "Resultados de la votación",
            data: votos,
            backgroundColor: listaBackgroundColor,
            borderColor: listaBorderColor,
            borderWidth: 1
        }],
        labels: etiquetas
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Resultados de la votación"
            }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Opciones"
            }
          },
          y: {
            title: {
              display: true,
              text: "Número de votos"
            },
            ticks: {
              stepSize: 1
            }
          }
        }
    }
});

var config2 = new Chart(ctx2, {
    type: "pie",
    data: {
        datasets: [{
            label: "Porcentaje de votos por opción",
            data: porVotosPorOpcion,
            backgroundColor: listaBackgroundColor,
            borderColor: listaBorderColor,
            borderWidth: 1
        }],
        labels: etiquetas
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Porcentaje de votos por opción"
            }
        }
    }
});
