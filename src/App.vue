<template>
  <div id="app">
    <h1>Auto RL Trainer</h1>
    <sui-form style="width:50%; margin: auto; margin-top: 2rem;">
      <sui-form-fields>
        <sui-form-field inline>
          <label>State-Space Size</label>
          <input type="number" v-model="state_space_size" />
        </sui-form-field>
        <sui-form-field inline>
          <label>Action-Space Size</label>
          <input type="number" v-model="action_space_size" />
        </sui-form-field>
      </sui-form-fields>
      <h3>Choose your training algorithm</h3>
      <sui-form-fields style="margin-top:2rem;">
        <sui-form-field>
          <sui-checkbox label="Q-Learning" radio value="1" v-model="algo" />
        </sui-form-field>
        <sui-form-field>
          <sui-checkbox label="Monte-Carlo" radio value="2" v-model="algo" />
        </sui-form-field>
        <sui-form-field>
          <sui-checkbox label="SARSA" radio value="3" v-model="algo" />
        </sui-form-field>
        <sui-form-field>
          <sui-checkbox label="Double Q-Learning" radio value="4" v-model="algo" />
        </sui-form-field>
        <sui-form-field>
          <sui-checkbox label="N-STEP-SARSA" radio value="5" v-model="algo" />
        </sui-form-field>
        <sui-form-field>
          <sui-checkbox label="Expected SARSA" radio value="6" v-model="algo" />
        </sui-form-field>
      </sui-form-fields>
      <sui-button color="green" style="margin-top:2rem;" @click.prevent="train">
        Train
      </sui-button>
    </sui-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      state_space_size: 0,
      action_space_size: 0,
      algo: '1'
    }
  },
  components: {
  },
  created() {
    this.api = axios.create({
      baseURL: 'http://localhost:4000/',
      withCredentials: true
    })
  },
  methods: {
    async train() {
      try {
        const response = await this.api.post('/train',
          {
            state_space_size: this.state_space_size,
            action_space_size: this.action_space_size,
            algo_num: this.algo
          })
        console.log(response)
      } catch(error) {
        console.log(error)
        alert("Sorry, something went wrong")
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 1rem;
}
</style>
