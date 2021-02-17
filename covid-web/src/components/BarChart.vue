<script>
import { Bar } from 'vue-chartjs'

export default {
  extends: Bar,
  props: ['chartData', 'options'],
  mounted () {
    console.log(this.chartData)
    this.renderChart(this.chartData, this.options)
  }
}
</script>

<style>
</style>
