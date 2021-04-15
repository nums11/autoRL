<template>
  <div id="app">
    <h1>Test</h1>
    <sui-form style="width:50%; margin: auto; margin-top: 2rem;">
      <sui-form-field>
        <label>Environment name</label>
        <input type="text" v-model="env_name">
      </sui-form-field>
      <sui-form-field style="width: 50%; margin:auto; margin-top:2rem; ">
        <label>Num Testing Episodes</label>
        <input type="number" v-model="num_testing_episodes"
        placeholder="Num Testing Episodes">
      </sui-form-field>
      <sui-button color="green" style="margin-top:2rem;" @click.prevent="test"
      :disabled="is_testing || !(env_name.length > 0) || !(selected_policies.length > 0)">
        Test
      </sui-button>
    </sui-form>
    <div style="margin-top:2rem;">
      <div v-if="is_testing">
        <sui-loader active size="medium" style="margin-top: 3rem;">
          Testing...
        </sui-loader>
      </div>
      <div v-else-if="testing_results.length > 0">
        <h3>Testing Results</h3>
        <p v-for="row in testing_results">
          {{ row }}
        </p>
      </div>
    </div>
    <div style="padding-top:3rem; padding-bottom:3rem; width:80%; margin:auto;">
      <div style="display:inline-block; vertical-align:top; width:49%;">
        <h3>Select a policy to train</h3>
        <div style="margin-top:1rem; border:black solid; cursor:pointer;"
        v-for="(policy,index) in policy_names" @click="selectPolicy(index)">
          {{ policy }}
        </div>
      </div>
      <div style="display:inline-block; width:49%; margin-left: 10px;">
        <h3>Selected</h3>
        <div v-for="(policy, index) in selected_policies">
          <div style="margin-top:1rem; border:green solid; width: 50%;
          display:inline-block;">
            {{ policy }}
          </div>
          <div style="display: inline-block; margin-left: 1rem; cursor:pointer;"
          @click="removeSelectedPolicy(index)">
            <sui-icon name="minus" color="red"></sui-icon>
          </div>
        </div>
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
      policy_names: [],
      selected_policies: [],
      num_testing_episodes: null,
      is_testing: false,
      testing_results: []
    }
  },
  components: {
  },
  created() {
    this.api = axios.create({
      baseURL: 'http://localhost:4000/',
      withCredentials: true
    })
    this.getPolicyNames()
  },
  methods: {
    async getPolicyNames() {
      try {
        const response = await this.api.get('/policy_names')
        this.policy_names = response.data
        console.log("policy_names", this.policy_names)
      } catch(error) {
        console.log(error)
        alert("Sorry, something went wrong")
      }
    },
    async test() {
      try {
        this.is_testing = true
        const response = await this.api.post('/test',
          {
            env_name: this.env_name,
            num_testing_episodes: this.num_testing_episodes,
            policies: this.selected_policies
          })
        this.testing_results = response.data
        this.is_testing = false
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
    },
    selectPolicy(index) {
      this.selected_policies.push(this.policy_names[index])
      this.policy_names.splice(index,1)
    },
    removeSelectedPolicy(index) {
      this.policy_names.push(this.selected_policies[index])
      this.selected_policies.splice(index,1)
    }
  }
}
</script>

<style>
</style>
