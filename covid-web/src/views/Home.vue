<template>
  <div class="home">
    <BarChart :chart-data="data" :options="options" />
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
