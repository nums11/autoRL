<template>
  <div id="app">
    <h1>Train</h1>
    <sui-form style="width:60%; margin: auto; margin-top: 2rem;">
      <sui-form-field>
        <label>Environment name</label>
        <input type="text" v-model="env_name">
      </sui-form-field>
      <sui-form-field style="width: 50%; margin:auto; margin-top:2rem; ">
        <label>Add Episode Set</label>
        <input type="number" v-model="num_episodes" placeholder="Num Epiosdes">
      </sui-form-field>
      <sui-button color="blue" @click.prevent='addEpisodeSet'>Add</sui-button>
      <h3>Episode Sets</h3>
      <div v-for="(episode_set,index) in episode_sets">
        <div style="border: black solid; width: 50%; margin: auto;
        margin-top:1rem; display: inline-block;">
          {{ episode_set }} episodes
        </div>
        <div style="display: inline-block; margin-left: 1rem; cursor:pointer;"
        @click="removeEpisodeSet(index)">
          <sui-icon name="minus" color="red"></sui-icon>
        </div>
      </div>
      <h3 style="margin-top:2rem;">Choose your training algorithm</h3>
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
      <sui-form-field inline v-if="algo === '5'">
        <label>n</label>
        <input type="number" v-model="n">
      </sui-form-field>
      <h3>Parameters</h3>
      <sui-form-fields>
        <sui-form-field v-if="algo !== '2'">
          <label>Learning Rate</label>
          <input type="number" v-model="learning_rate">
        </sui-form-field>
        <sui-form-field v-if="algo !== '2'">
          <label>Epsilon</label>
          <input type="number" v-model="epsilon">
        </sui-form-field>
        <sui-form-field v-if="algo !== '2'">
          <label>Min Epsilon</label>
          <input type="number" v-model="min_epsilon">
        </sui-form-field>
        <sui-form-field v-if="algo !== '2'">
          <label>Epsilon Decay Rate</label>
          <input type="number" v-model="epsilon_decay_rate">
        </sui-form-field>
        <sui-form-field>
          <label>Discount Factor</label>
          <input type="number" v-model="discount_factor">
        </sui-form-field>
        <sui-form-field v-if="algo !== '2'">
          <label>Max Steps Per Episode</label>
          <input type="number" v-model="max_steps_per_episode">
        </sui-form-field>
      </sui-form-fields>
      <sui-button color="green" style="margin-top:2rem;" @click.prevent="train"
      :disabled="is_training || !(env_name.length > 0) || !(episode_sets.length > 0)">
        Train
      </sui-button>
    </sui-form>
    <div style="margin-top:2rem; padding-bottom: 2rem;">
      <div v-if="is_training">
        <sui-loader active size="medium" style="margin-top: 8rem;">
          Training...
        </sui-loader>
      </div>
      <div v-else>
        <h3>Training Results</h3>
        <p v-for="row in training_results">
          {{ row }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      env_name: '',
      num_episodes: null,
      algo: '1',
      training_results: [],
      is_training: false,
      episode_sets: [],
      n: 0,
      learning_rate: 0.1,
      epsilon: 1,
      min_epsilon: 0.1,
      epsilon_decay_rate: 0.001,
      discount_factor: 0.99,
      max_steps_per_episode: 300
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
        this.is_training = true
        const response = await this.api.post('/train',
          {
            env_name: this.env_name,
            episode_sets: this.episode_sets,
            algo_num: this.algo,
            n: this.n,
            learning_rate: this.learning_rate,
            epsilon: this.epsilon,
            min_epsilon: this.min_epsilon,
            epsilon_decay_rate: this.epsilon_decay_rate,
            discount_factor: this.discount_factor,
            max_steps_per_episode: this.max_steps_per_episode
          })
        this.training_results = response.data
        this.is_training = false
      } catch(error) {
        console.log(error)
        alert("Sorry, something went wrong")
      }
    },
    addEpisodeSet() {
      this.episode_sets.push(this.num_episodes)
      this.num_episodes = null
    },
    removeEpisodeSet(index) {
      this.episode_sets.splice(index,1)
    }
  }
}
</script>

<style>
</style>
