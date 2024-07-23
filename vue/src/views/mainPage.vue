<template>
  <div class="dashboard">
    <div class="background-overlay"></div>
    <img class="background" src="../assets/background4.png">
    <header class="header">
      智慧道路检测系统
    </header>
    <div class="main-content">
      <div class="control-panel">
        <div class="control-item">
          <div class="icon-placeholder">
            <img class="my-icon" src="../assets/总监控点位.png">
          </div>
          <div class="text">总监控点位<br>4</div>
        </div>
        <div class="control-item">
          <div class="icon-placeholder">
            <img class="my-icon" src="../assets/车辆拥堵.png">
          </div>
          <div class="text">车辆拥堵<br>{{ totalJam }}</div>
        </div>
        <div class="control-item">
          <div class="icon-placeholder">
            <img class="my-icon" src="../assets/车流量.png">
          </div>
          <div class="text">车流量<br>{{ totalCarFlow }}</div>
        </div>
        <div class="control-item">
          <div class="icon-placeholder">
            <img class="my-icon" src="../assets/人流量.png">
          </div>
          <div class="text">人流量<br>{{ totalPersonFlow }}</div>
        </div>
      </div>
      <div class="video-panel">
        <div class="video-main">
          <img :src="videoFrames[mainChannel]" alt="主监控画面" class="video-frame">
        </div>
        <div class="video-sub">
          <div class="video-item" @click="swapVideo('sub1')">
            <img :src="videoFrames[sub1Channel]" alt="子监控画面1" class="video-frame">
          </div>
          <div class="video-item" @click="swapVideo('sub2')">
            <img :src="videoFrames[sub2Channel]" alt="子监控画面2" class="video-frame">
          </div>
          <div class="video-item-final" @click="swapVideo('sub3')">
            <img :src="videoFrames[sub3Channel]" alt="子监控画面3" class="video-frame">
          </div>
        </div>
      </div>
    </div>
    <div class="sidebar">
      <div class="chart-group">
        <BarChart1 />
      </div>
      <div class="chart-group">
        <BarChart2 />
      </div>
      <div class="chart-group">
        <PieChart />
      </div>
    </div>
  </div>
</template>

<script>
import BarChart1 from '../components/BarChart-car.vue';
import BarChart2 from '../components/BarChart-person.vue';
import PieChart from '../components/PieChart.vue';
import io from 'socket.io-client';

export default {
  name: 'dashboardMonitor',
  components: {
    BarChart1,
    BarChart2,
    PieChart,
  },
  data() {
    return {
      totalJam: 0,
      totalCarFlow: 0,
      totalPersonFlow: 0,
      videoFrames: {
        main: '',
        sub1: '',
        sub2: '',
        sub3: '',
      },
      mainChannel: 'main',
      sub1Channel: 'sub1',
      sub2Channel: 'sub2',
      sub3Channel: 'sub3',
    };
  },
  mounted() {
    this.fetchJamData();
    this.fetchCarFlowData();
    this.fetchPersonFlowData();
    this.initializeWebSocket();
    setInterval(this.fetchJamData, 5000); // 每5秒更新一次
    setInterval(this.fetchCarFlowData, 5000); // 每5秒更新一次
    setInterval(this.fetchPersonFlowData, 5000); // 每5秒更新一次
  },
  methods: {
    async fetchJamData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/jam');
        const data = await response.json();
        this.totalJam = Object.values(data).filter(value => value > 20).length;
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async fetchCarFlowData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/car_chart');
        const data = await response.json();
        this.totalCarFlow += data.carNum.reduce((acc, curr) => acc + curr, 0);
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async fetchPersonFlowData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/person_chart');
        const data = await response.json();
        this.totalPersonFlow += data.personNum.reduce((acc, curr) => acc + curr, 0);
      } catch (error) {
        console.error('Error:', error);
      }
    },
    initializeWebSocket() {
      const namespaces = [
        '/video1',
        '/video2',
        '/video3',
        '/video4'
      ];

      namespaces.forEach(namespace => {
        const socket = io('http://127.0.0.1:5000' + namespace);
        socket.on('video_frame', (data) => {
          if (data.channel && data.frame) {
            let frameKey;
            switch (data.channel) {
              case '/video1':
                frameKey = 'main';
                break;
              case '/video2':
                frameKey = 'sub1';
                break;
              case '/video3':
                frameKey = 'sub2';
                break;
              case '/video4':
                frameKey = 'sub3';
                break;
              default:
                frameKey = 'main';
            }
            this.videoFrames[frameKey] = `data:image/jpeg;base64,${data.frame}`;
          }
        });
        socket.on('connect', () => {
          console.log(`Connected to ${namespace}`);
        });
        socket.on('disconnect', () => {
          console.log(`Disconnected from ${namespace}, retrying in 5 seconds...`);
          setTimeout(() => this.initializeWebSocket(), 5000);
        });
        socket.on('connect_error', (error) => {
          console.error('Socket.IO connection error:', error);
        });
      });
    },
    swapVideo(subChannel) {
      // 根据 subChannel 来交换 mainChannel 和相应的子频道
      if (subChannel === 'sub1') {
        [this.mainChannel, this.sub1Channel] = [this.sub1Channel, this.mainChannel];
      } else if (subChannel === 'sub2') {
        [this.mainChannel, this.sub2Channel] = [this.sub2Channel, this.mainChannel];
      } else if (subChannel === 'sub3') {
        [this.mainChannel, this.sub3Channel] = [this.sub3Channel, this.mainChannel];
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main-content main-content";
  grid-template-rows: auto 1fr;
  grid-template-columns: 1fr 3fr 3fr;
  height: 100vh;
  position: relative;
  letter-spacing: 2px;
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -2;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: -1;
}

.header {
  margin-top: 10px;
  grid-area: header;
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 20px #00ffff, 0 0 25px #00ffff;
  padding: 10px;
  text-align: center;
  font-size: 30px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  letter-spacing: 5px;
}

.sidebar {
  width: 200px;
  height: 645px;
  grid-area: sidebar;
  display: flex;
  flex-direction: column;
  padding: 10px;
  margin-top: 10px;
}

.chart-group {
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
  margin-bottom: 10px;
  padding: 10px;
  flex: 1;
  text-align: center;
  font-size: 18px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  border-radius: 15px;
}

.main-content {
  grid-area: main-content;
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.control-panel {
  display: flex;
  justify-content: space-between;
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
  padding-top: 10px;
  padding-bottom: 10px;
  font-size: 18px;
}

.control-item {
  flex: 1;
  text-align: center;
  margin: 5px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  border-radius: 15px;
}

.icon-placeholder {
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
  box-shadow: 0 0 5px rgba(0, 255, 255, 0.6), 0 0 10px rgba(0, 255, 255, 0.6), 0 0 15px rgba(0, 255, 255, 0.6), 0 0 20px rgba(0, 255, 255, 0.6);
  border-radius: 50%;
}

.my-icon {
  width: 40px;
  height: 40px;
}

.text {
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff
}

.video-panel {
  display: flex;
  flex: 1;
  margin-top: 10px;
}

.video-main {
  width: 1180px;
  height: 480px;
  flex: 3;
  padding: 2px;
  margin-right: 10px;
  text-align: center;
  font-size: 18px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  border-radius: 15px;
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff
}

.video-sub {
  width: 390px;
  height: 485px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.video-item {
  width: 305px;
  height: 145px;
  flex: 1;
  padding: 2px;
  margin-bottom: 15px;
  text-align: center;
  font-size: 18px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  border-radius: 15px;
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff
}

.video-item-final {
  width: 305px;
  height: 145px;
  flex: 1;
  padding: 2px;
  text-align: center;
  font-size: 18px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  border-radius: 15px;
  background: linear-gradient(90deg, #00ffff, #00ff00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
}

.video-frame {
  width: 100%;
  height: 100%;
  border-radius: 15px;
  object-fit: cover;
}
</style>
