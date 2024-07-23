<template>
  <div ref="chart" style="width: 100%; height: 100%;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'PieChart',
  data() {
    return {
      chart: null,
      trafficComposition: {
        '人': 0,
        '自行车': 0,
        '巴士': 0,
        '摩托车': 0,
        '汽车': 0,
      },
    };
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart);
    this.updateChart();
    setInterval(this.fetchTrafficComposition, 5000);
  },
  methods: {
    async fetchTrafficComposition() {
      try {
        const response = await fetch('http://127.0.0.1:5000/pie');
        const data = await response.json();
        this.trafficComposition['人'] = data['personNum'];
        this.trafficComposition['自行车'] = data['bicycleNum'];
        this.trafficComposition['巴士'] = data['busNum'];
        this.trafficComposition['摩托车'] = data['motorNum'];
        this.trafficComposition['汽车'] = data['carNum'];
        this.updateChart();
      } catch (error) {
        console.error('Error:', error);
      }
    },
    updateChart() {
      const data = Object.entries(this.trafficComposition).map(([name, value]) => ({
        name,
        value,
      }));
      this.chart.setOption({
        title: {
          text: '占比',
          top: 'top',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold',
            color: '#00ffff',
          },
        },
        series: [
          {
            type: 'pie',
            data,
            name: '交通组成',
            label: {
              show: false,
            },
            labelLine: {
              show: false,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
              label: {
                show: false,
              },
            },
          },
        ],
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {d}%',
          backgroundColor: 'rgba(50, 50, 50, 0)',
          borderColor: 'transparent',
          textStyle: {
            color: '#fff',
          },
          position: function (point) {
            return [point[0] + 10, point[1]];
          },
        },
      });
    },
  },
};
</script>
