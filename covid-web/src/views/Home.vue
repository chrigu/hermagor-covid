<template>
  <div class="home">
    <ul>
      <li>{{latestDate}}</li>
      <li>{{latestCases}}</li>
      <li>{{latestDeaths}}</li>
      <li>{{latestIncidence}}</li>
    </ul>
    <BarChart v-if="hasDatasets(dailyData)" :chart-data="dailyData" :options="dailyOptions" />
    <LineChart v-if="hasDatasets(sumData)" :chart-data="sumData" :options="sumOptions" />
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
    return {
      dailyOptions: {
        title: {
          display: true,
          text: 'Hermagor neue Fälle & Tote'
        },
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series',
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
      },
      dailyData: {
        labels: ['bla', 'blu'],
        datasets: []
      },
      sumOptions: {
        title: {
          display: true,
          text: 'Hermagor neue Fälle & Tote'
        },
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series',
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
      },
      incidenceData: {
        labels: ['bla'],
        datasets: []
      },
      incidenceOptions: {
        title: {
          display: true,
          text: 'Inzidenz'
        },
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series',
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
      },
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
    // createDates (series) {
    //   return series.map((datapoint) => new Date(datapoint.x))
    // },
    createDataSet (data, label, color) {
      return {
        label: label,
        fill: false,
        data: data.map((datapoint, i) => ({ x: datapoint.x, y: datapoint.y })),
        backgroundColor: color
      }
    },
    getLatestDatapoint (data) {
      return data.slice(-1)[0]
    },
    hasDatasets (data) {
      return data.datasets.length > 0
    }
  },
  mounted () {
    // const dates = this.createDates(covidData.cases)
    const dailyCasesSet = this.createDataSet(covidData.cases, 'Fälle', '#FFFF00')
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
