<template>
  <div class="login-container">
    <div class="login-card">
      <h1>登录</h1>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="username">用户名:</label>
          <input type="text" v-model="username" required class="login-text" />
        </div>
        <div class="input-group">
          <label for="password">密码:</label>
          <input type="password" v-model="password" required class="login-text" />
        </div>
        <button type="submit" class="login-button">登录</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'loginAdmin',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            admin_id: this.username,
            admin_pw: this.password,
          }),
        });
        const result = await response.json();
        if (result.success) {
          // 登录成功后调用 /start 方法
          await fetch('http://127.0.0.1:5000/start', {
            method: 'GET',
          });

          this.$router.push({ name: 'mainPage' });
        } else {
          alert('用户名或密码错误');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('登录失败，请稍后再试');
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-image: url('../assets/background4.png');
  background-size: cover;
  background-position: center;
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  /* 黑色透明蒙版 */
  z-index: 1;
  /* 让蒙版位于内容之下 */
}

.login-card {
  padding: 2rem;
  border: 2px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 5px rgba(0, 255, 255, 0.6), 0 0 10px rgba(0, 255, 255, 0.6), 0 0 15px rgba(0, 255, 255, 0.6);
  border-radius: 15px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  position: absolute;
  top: 50%;
  /* 调整登录框的垂直位置 */
  left: 60%;
  /* 调整登录框的水平位置 */
  transform: translate(-50%, -50%);
  z-index: 2;
  /* 让登录框位于蒙版之上 */
}

h1 {
  color: white;
  letter-spacing: 5px;
  margin-bottom: 1.5rem;
}

.input-group {
  margin-bottom: 1rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(0, 255, 255, 0.6);
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  border-color: #42b983;
  outline: none;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.login-text {
  opacity: 0.9;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: rgba(0, 255, 255, 0.6);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 20px;
}

.login-button:hover {
  background-color: #00ffff;
}
</style>
