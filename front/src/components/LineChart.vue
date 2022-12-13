<script>
import { Line } from 'vue-chartjs'
export default {
  extends: Line,
  props: {
    bench: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      datacollection: {
        labels: this.bench.RANGE,
        datasets: Object.keys(this.bench.TESTS).map((el, i) => ({
          label: el,
          backgroundColor: this.bench.COLORS[i],
          borderColor: this.bench.COLORS[i],
          borderWidth: 2,
          fill: false,
          data: this.bench.TESTS[el].average
        }))
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            },
            scaleLabel: {
              display: true,
              labelString: this.bench.VALUE
            }
          }],
          xAxes: [{
            maxBarThickness: 100,
            gridLines: {
              display: true
            }
          }]
        },
        legend: {
          display: true
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  mounted () {
    this.renderChart(this.datacollection, this.options)
  }
}
</script>
