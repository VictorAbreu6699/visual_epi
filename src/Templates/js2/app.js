$(document).foundation()

const ctx = document.getElementById('bars-chart-container');

let myMapChart;
let myChart;
let myHistogram;
let myPolarChart;

let chartForm = document.getElementById("chart-form");
let selectRegiao = document.getElementById("input-regioes");
let selectEstado = document.getElementById("input-estados");
let selectCidade = document.getElementById("input-cidades");
let selectAno = document.getElementById("input-anos");

printMapChart(myMapChart);

// print map chart
function printMapChart(myMapChart, map = "BRAZIL") {

    var d, jb;
    if (map === "BRAZIL") {
        d = STATES.map((state) => { return { "hc-a2": state.acron, "value": state.total }});
        jb = "hc-a2";
    } else {
        d = eval(map).features.map((city) => {
            var count = 0;
            var sum = 0;
            for (var i = 0; i < YEARS.length; i++) {
                if (INDEXED_DATA[city.properties.name] && INDEXED_DATA[city.properties.name][YEARS[i].name]) {
                    var totalDoAno = INDEXED_DATA[city.properties.name][YEARS[i].name];
                    if (totalDoAno[11]) {
                        count++;
                        sum += totalDoAno[11];
                    }
                }
            }
            sum = sum / count;
            return { "name": city.properties.name, "value": sum.toFixed(2) }
        });
        jb = "name";
    }

    document.getElementById("btn-back").style.display = "none";

    if (myMapChart) myMapChart.destroy();

    myMapChart = Highcharts.mapChart('map-container', {

        title: { text: 'Ocorrências de enfermidades' },
        subtitle: { text: '' },

        mapNavigation: {
            enabled: true,
            buttonOptions: { verticalAlign: 'bottom' }
        },

        colorAxis: { 
        min: 1,
            max: 200,
            
            stops: [
                [0.1, '#FF0000'],
                [0.3, '#FC6600'],
                [0.5, '#FFFF00'],
                [0.7, '#4ce825'],
                [0.9, '#1f8c15']
            ],
            marker: {
                color: '#323'
            }
        },
        series: [{
            data: d,
            joinBy: jb,
            mapData: eval(map),
            allAreas: true,
            name: 'Ocorrências de enfermidades',
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            },
            point: {
                events: {
                    click: function () {
                        if (map === "BRAZIL") {
                            STATES.forEach((state) => {
                                if (state.name === this.name) {
                                    printMapChart(myMapChart, state.acron);
                                    document.getElementById("btn-back").style.display = "block";
                                    selectByCode(selectRegiao, String(state.code).substring(0, 1));
                                    selectByCode(selectEstado, String(state.code).substring(0, 2));
                                }
                            });
                        } else {
                            eval(map).features.forEach((city) => {
                                if (city.properties.name === this.name) {
                                    selectByCode(selectCidade, String(city.properties.id));
                                }
                            });
                        }
                    }
                }
            }
        }]
        
    });
}

// print chart
function printChart(chart) {
    
    let regiaoSelecionada = selectRegiao.options[selectRegiao.selectedIndex].text;
    let estadoSelecionado = selectEstado.options[selectEstado.selectedIndex].text;
    let cidadeSelecionada = selectCidade.options[selectCidade.selectedIndex].text;
    let anoSelecionado = selectAno.options[selectAno.selectedIndex].text;
    
    if (regiaoSelecionada && estadoSelecionado
            && cidadeSelecionada && anoSelecionado) {
        
        cleanChart(Chart.getChart(ctx));

        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: VACCINES.map((vac) => vac.name),
                datasets: [{
                    label: 'Percentual de Vacinação',
                    data: INDEXED_DATA[cidadeSelecionada][anoSelecionado],
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(75, 192, 192)',
                        'rgb(255, 205, 86)',
                        'rgb(201, 203, 207)',
                        'rgb(54, 162, 235)',
                        'rgb(31, 120, 50)',
                        'rgb(95, 105, 207)',
                        'rgb(255 122 127 / 80%)',
                        'rgb(30% 20% 10%)',
                        'rgb(162,235,54)',
                        'rgb(235,127,54)',
                        'rgb(30% 20% 50%)'
                      ],
                      borderColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)'
                      ],
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

function getFirstTwoDigits(str) {
    return String(str).substring(0, 2);
}

function selectByCode(el, code) {
    if (el) {

        var opts = el.getElementsByTagName("option");
        
        if (opts && opts.length > 0) {
            
            for (var i= 0; i < opts.length; i++) {
                
                if (opts[i].value === code) {
                    
                    opts[i].selected = "selected";
                    var e = new Event("change");
                    el.dispatchEvent(e);
                }
            }
        }
    }
}

// limpa um gráfico se ele existir
function cleanChart(chart) {
    if (chart) chart.destroy();
}