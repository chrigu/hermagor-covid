<template>
  <div class="home">
    <h1 class="text-4xl font-serif">Covid Hermagor</h1>
    <div>
      <h2>Neuste Daten*</h2>
      <ul>
        <li>
          Neue Fälle: {{latestCases}}
        </li>
        <li>
          Neue Tote: {{latestDeaths}}
        </li>
        <li>
          Inzidenz: {{latestIncidence}}
        </li>
      </ul>

    </div>
    <BarChart v-if="hasDatasets(dailyData)" :styles="styles" :height="300" :chart-data="dailyData" :options="dailyOptions" />
    <LineChart v-if="hasDatasets(sumData)" :height="300" :chart-data="sumData" :options="sumOptions" />
    <LineChart v-if="hasDatasets(incidenceData)" :chart-data="incidenceData" :options="incidenceOptions" />
  </div>
</template>

<script>
// @ is an alias to /src
import BarChart from '@/components/BarChart.vue'
import LineChart from '@/components/LineChart'
import covidData from '@/assets/data.json'

export default {
  name: 'Home',
  components: {
    BarChart,
    LineChart
  },
  data () {
    // https://www.chartjs.org/samples/latest/scales/time/financial.html
    return {
      dailyOptions: {

      },
      styles: {
        height: '300px',
        position: 'relative'
      },
      dailyData: {
        labels: ['bla', 'blu'],
        datasets: []
      },
      sumOptions: {},
      incidenceData: {
        labels: ['bla'],
        datasets: []
      },
      incidenceOptions: {},
      sumData: {
        labels: ['bla', 'blu'],
        datasets: []
      },
      latestDate: null,
      latestCases: -1,
      latestDeaths: -1,
      latestIncidence: -1
    }
  },
  methods: {
    createDataSet (data, label, color) {
      return {
        label: label,
        fill: false,
        data: data.map((datapoint, i) => ({ x: datapoint.x, y: datapoint.y })),
        backgroundColor: color,
        borderColor: color,
        pointRadius: 0
      }
    },
    getLatestDatapoint (data) {
      return data.slice(-1)[0]
    },
    hasDatasets (data) {
      return data.datasets.length > 0
    },
    optionsGenerator () {
      return {
        title: {
          display: true,
          text: 'Hermagor neue Fälle & Tote'
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series',
            time: {
              displayFormats: {
                year: 'MMM YYYY'
              }
            },
            ticks: {
              major: {
                enabled: true,
                fontStyle: 'bold'
              },
              source: 'data',
              autoSkip: true,
              autoSkipPadding: 75,
              maxRotation: 0,
              sampleSize: 100
            }
          }]
        }
      }
    }
  },
  mounted () {
    this.dailyOptions = this.optionsGenerator('Tägliche Fälle & Tote')
    this.sumOptions = this.optionsGenerator('Total Fälle & Tote')
    this.incidenceOptions = this.optionsGenerator('Inzidenz')

    const dailyCasesSet = this.createDataSet(covidData.cases, 'Fälle', '#0000FF')
    const dailyDeathsSet = this.createDataSet(covidData.deaths, 'Tote', '#FF0000')
    this.dailyData.datasets = [dailyCasesSet, dailyDeathsSet]

    const sumCasesSet = this.createDataSet(covidData.cases_sum, 'Fälle', '#FFFF00')
    const sumDeathsSet = this.createDataSet(covidData.deaths_sum, 'Tote', '#FF0000')
    this.sumData.datasets = [sumCasesSet, sumDeathsSet]

    this.incidenceData.datasets = [this.createDataSet(covidData.incidence, 'Inzidenz', '#00FF00')]

    this.latestDate = this.getLatestDatapoint(covidData.cases).x
    this.latestCases = this.getLatestDatapoint(covidData.cases).y
    this.latestDeaths = this.getLatestDatapoint(covidData.deaths).y
    this.latestIncidence = this.getLatestDatapoint(covidData.incidence).y
  }
}
</script>
