<template>
  <div ref="chart" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'BarChart2',
  data() {
    return {
      chart: null,
      pedestrianData: [],
      totalPedestrian: 0,
    };
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart);
    this.updateChart();
    setInterval(this.fetchPedestrianData, 5000);
  },
  methods: {
    async fetchPedestrianData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/person_chart');
        const data = await response.json();
        const totalPedestrian = data.personNum.reduce((acc, curr) => acc + curr, 0);
        this.pedestrianData.push(totalPedestrian);
        this.totalPedestrian += totalPedestrian;
        console.log(this.pedestrianData);
        if (this.pedestrianData.length > 10) this.pedestrianData.shift();
        this.updateChart();
      } catch (error) {
        console.error('Error:', error);
      }
    },
    updateChart() {
      this.chart.setOption({
        grid: {
          left: '10%',
          right: '10%',
          top: '10%',
          bottom: '10%',
          containLabel: true,
        },
        xAxis: {
          type: 'category',
          data: Array.from({ length: this.pedestrianData.length }, (_, i) => i + 1),
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            show: false,
          },
          splitLine: {
            show: false,
          },
        },
        series: [
          {
            data: this.pedestrianData,
            type: 'bar',
            name: '人流量',
            emphasis: {
              itemStyle: {
                color: '#00ffff',
                borderColor: '#00ffff',
                borderWidth: 2,
              },
              label: {
                show: true,
                position: 'top',
              },
            },
          },
        ],
        title: {
          text: `人流量`,
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold',
            color: '#00ffff',
          },
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow',
          },
        },
      });
    },
  },
};
</script>
