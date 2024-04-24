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

fillOptions(selectRegiao, selectRegiao, REGIONS, "");

selectRegiao.addEventListener("change", () => {
    cleanChart(Chart.getChart(ctx));
    cleanOptions(selectEstado);
    cleanOptions(selectCidade);
    cleanOptions(selectAno);
    fillOptions(selectRegiao, selectEstado, STATES, "regionId");
});

selectEstado.addEventListener("change", () => {
    cleanChart(Chart.getChart(ctx));
    cleanOptions(selectCidade);
    cleanOptions(selectAno);
    fillOptions(selectEstado, selectCidade, CITIES, "code", getFirstTwoDigits);
});

selectCidade.addEventListener("change", () => {
    cleanChart(Chart.getChart(ctx));
    cleanOptions(selectAno);
    fillOptions(selectCidade, selectAno, YEARS, "");
});

printMapChart(myMapChart);

// print map chart
function printMapChart(myMapChart, map = "BRAZIL") {        
    var d, jb;
    if (map === "BRAZIL") {
        d = STATES.map((state) => { return { "hc-a2": state.acronym, "value": state.cases_count }});
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
                        console.log('oi')
                        if (map === "BRAZIL") {
                            STATES.forEach((state) => {
                                if (state.name === this.name) {
                                    printMapChart(myMapChart, state.acronym);
                                    document.getElementById("btn-back").style.display = "block";
                                    selectByCode(selectRegiao, state.id);
                                    selectByCode(selectEstado, state.id);
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

function fillOptions(el, target, objArrToCompare, propToCompare, functionToCompareCallback) {
    if (el === target || el.value) {
        var val;
        objArrToCompare.forEach((obj) => {
            if (propToCompare) {
                val = functionToCompareCallback ? functionToCompareCallback(obj[propToCompare]) : obj[propToCompare];
            }
            if (!propToCompare || (propToCompare && el.value == val)) {
                var novaOpcao = new Option(String(obj.name), String(obj.code));
                target.add(novaOpcao, undefined);
            }
        });
        target.disabled = false;
    } else {
        target.disabled = true;
    }
}

function getFirstTwoDigits(str) {
    return String(str).substring(0, 2);
}