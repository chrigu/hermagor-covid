<template>
  <div class="home">
    <h1 class="text-center md:text-left text-6xl mt-8 mb-8">Covid Hermagor</h1>
    <div class="mb-8">
      <h2 class="text-xl mb-4">Neuste Daten<span class="text-red-500">*</span> ({{humanReadableLastestDate}})</h2>
      <ul class="flex flex-col md:flex-row">
        <li class="flex-auto bg-gray-100 text-center py-4 mb-4 md:mb-0">
          <h3 class="text-2xl md:text-xl">Fälle</h3>
          <p class="text-2xl md:text-xl">{{latestCases}}</p>
        </li>
        <li class="flex-auto bg-gray-100 text-center py-4 md:mx-8 mb-4 md:mb-0">
          <h3 class="text-2xl md:text-xl">Tote</h3>
          <p class="text-2xl md:text-xl">{{latestDeaths}}</p>
        </li>
        <li class="flex-auto bg-gray-100 text-center py-4">
          <h3 class="text-2xl md:text-xl">Inzidenz</h3>
          <p class="text-2xl md:text-xl">{{roundedIncedence}}</p>
        </li>
      </ul>
      <p class="mt-4"><span class="text-red-500">*</span>Datenquelle (mit etwas Verzögerung): <a class="text-red-500" href="https://www.data.gv.at/katalog/dataset/covid-19-zeitliche-darstellung-von-daten-zu-covid19-fallen-je-bezirk">Bundesministerium für Soziales, Gesundheit, Pflege und Konsumentenschutz (BMSGPK)</a></p>
    </div>
    <div class="my-4">
      <h2 class="text-xl">Tägliche Fälle & Tote</h2>
      <BarChart v-if="hasDatasets(dailyData)" :styles="styles" :chart-data="dailyData" :options="dailyOptions" />
    </div>
    <div class="my-4">
      <h2 class="text-xl">Total Fälle & Tote</h2>
      <LineChart v-if="hasDatasets(sumData)" :chart-data="sumData" :options="sumOptions" />
    </div>
    <div class="mt-4 mb-8">
      <h2 class="text-xl">Inzidenz</h2>
      <LineChart v-if="hasDatasets(incidenceData)" :chart-data="incidenceData" :options="incidenceOptions" />
    </div>
    <footer class="text-center mb-2">
      <p><router-link to="/about">Impressum</router-link> | <a class="text-red-500" href="https://github.com/chrigu/hermagor-covid">Code</a></p>
    </footer>
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
        datasets: []
      },
      sumOptions: {},
      incidenceData: {
        datasets: []
      },
      incidenceOptions: {},
      sumData: {
        datasets: []
      },
      latestDate: null,
      latestCases: -1,
      latestDeaths: -1,
      latestIncidence: -1
    }
  },
  computed: {
    roundedIncedence () {
      return Math.round(this.latestIncidence)
    },
    humanReadableLastestDate () {
      const date = new Date(this.latestDate)
      return `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`
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

    const dailyCasesSet = this.createDataSet(covidData.cases, 'Fälle', '#DC2626')
    const dailyDeathsSet = this.createDataSet(covidData.deaths, 'Tote', '#7F1D1D')
    this.dailyData.datasets = [dailyCasesSet, dailyDeathsSet]

    const sumCasesSet = this.createDataSet(covidData.cases_sum, 'Fälle', '#DC2626')
    const sumDeathsSet = this.createDataSet(covidData.deaths_sum, 'Tote', '#7F1D1D')
    this.sumData.datasets = [sumCasesSet, sumDeathsSet]

    this.incidenceData.datasets = [this.createDataSet(covidData.incidence, 'Inzidenz', '#DC2626')]

    this.latestDate = this.getLatestDatapoint(covidData.cases).x
    this.latestCases = this.getLatestDatapoint(covidData.cases).y
    this.latestDeaths = this.getLatestDatapoint(covidData.deaths).y
    this.latestIncidence = this.getLatestDatapoint(covidData.incidence).y
  }
}
</script>
