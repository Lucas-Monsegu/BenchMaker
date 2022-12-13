<script>
import { Bar } from 'vue-chartjs'
export default {
  extends: Bar,
  props: {
    bench: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      datacollection: {
        labels: Object.keys(this.bench.TESTS),
        datasets: [
          {
            label: 'Average',
            backgroundColor: '#6aaaff',
            borderWidth: 0,
            data: this.bench.VALUES
          }
        ]
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
              display: false
            }
          }]
        },
        legend: {
          display: false
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
