<template>
  <div class="home">
    <BarChart v-if="data.datasets.length > 0" :chart-data="data" :options="options" />
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
          text: 'Chart.js Time Point Data'
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
      }
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
    }
  },
  mounted () {
    const dates = this.createDates(covidData.cases)
    const casesSet = this.createDataSet(covidData.cases, dates, 'Fälle', '#FFFF00')
    const deathsSet = this.createDataSet(covidData.deaths, dates, 'Tote', '#FF0000')
    console.log(deathsSet)
    this.data.datasets = [casesSet, deathsSet]
    console.log(this.data)
  }
}
</script>
