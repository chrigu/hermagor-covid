<template>
  <div class="home">
    <ul>
      <li>{{latestDate}}</li>
      <li>{{latestCases}}</li>
      <li>{{latestDeaths}}</li>
      <li>{{latestIncidence}}</li>
    </ul>
    <BarChart v-if="hasDatasets" :chart-data="data" :options="options" />
  </div>
</template>

<script>
// @ is an alias to /src
import BarChart from '@/components/BarChart.vue'
import covidData from '@/assets/data.json'

export default {
  name: 'Home',
  components: {
    BarChart
  },
  data () {
    return {
      options: {
        title: {
          display: true,
          text: 'Hermagor neue Fälle & Tote'
        },
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series'
          }]
        }
      },
      data: {
        labels: ['bla', 'blu'],
        datasets: []
      },
      latestDate: null,
      latestCases: -1,
      latestDeaths: -1,
      latestIncidence: -1
    }
  },
  computed: {
    hasDatasets () {
      return this.data.datasets.length > 0
    }
  },
  methods: {
    createDates (series) {
      return series.map((datapoint) => new Date(datapoint.x))
    },
    createDataSet (data, dates, label, color) {
      return {
        label: label,
        fill: false,
        data: data.map((datapoint, i) => ({ x: dates[i], y: datapoint.y })),
        backgroundColor: color
      }
    },
    getLatestDatapoint (data) {
      return data.slice(-1)[0]
    }
  },
  mounted () {
    const dates = this.createDates(covidData.cases)
    const casesSet = this.createDataSet(covidData.cases, dates, 'Fälle', '#FFFF00')
    const deathsSet = this.createDataSet(covidData.deaths, dates, 'Tote', '#FF0000')
    console.log(deathsSet)
    this.data.datasets = [casesSet, deathsSet]
    console.log(this.data)

    this.latestDate = this.getLatestDatapoint(dates)
    this.latestCases = this.getLatestDatapoint(covidData.cases).y
    this.latestDeaths = this.getLatestDatapoint(covidData.deaths).y
    this.latestIncidence = this.getLatestDatapoint(covidData.incidence).y
  }
}
</script>
