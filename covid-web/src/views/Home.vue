<template>
  <div class="home">
    <LineChart :chart-data="data" :options="options" />
  </div>
</template>

<script>
// @ is an alias to /src
import LineChart from '@/components/LineChart.vue'
import covidData from '@/assets/data.json'

export default {
  name: 'Home',
  components: {
    LineChart
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
        datasets: []
      }
    }
  },
  methods: {
    createDates (series) {
      return series.map((datapoint) => new Date(datapoint.x))
    }
  },
  mounted () {
    const dates = this.createDates(covidData.cases)
    const casesSet = {
      label: 'Fälle',
      fill: false,
      data: covidData.cases.map((datapoint, i) => ({ x: dates[i], y: datapoint.y }))
    }
    this.data.datasets = [casesSet]
  }
}
</script>
