<template>
  <div ref="chart" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'BarChart1',
  data() {
    return {
      chart: null,
      trafficData: [],
      totalTraffic: 0,
    };
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart);
    this.updateChart();
    setInterval(this.fetchTrafficData, 5000);
  },
  methods: {
    async fetchTrafficData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/car_chart');
        const data = await response.json();
        const totalTraffic = data.carNum.reduce((acc, curr) => acc + curr, 0);
        this.trafficData.push(totalTraffic);
        this.totalTraffic += totalTraffic;
        console.log(this.trafficData);
        if (this.trafficData.length > 10) this.trafficData.shift();
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
          data: Array.from({ length: this.trafficData.length }, (_, i) => i + 1),
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
            data: this.trafficData,
            type: 'bar',
            name: '车流量',
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
          text: `车流量`,
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
