<template>
  <div id="app">
    <div v-if="!show_sub_components" style="padding-top:1rem;">
      <h1>AutoRL Trainer</h1>
      <sui-button size="large" color="blue" @click="showTrain">Train</sui-button>
      <sui-button size="large" color="green" @click="showTest">Test</sui-button>
    </div>
    <div v-else style="padding-top: 1rem;">
      <sui-button @click="hideSubComponents">Back</sui-button>
      <Train v-if="show_train" />
      <Test v-if="!show_train" />
    </div>
  </div>
</template>

<script>
import Train from '@/Train.vue'
import Test from '@/Test.vue'

export default {
  name: 'App',
  components: {
    Train,
    Test
  },
  data() {
    return {
      show_sub_components: false,
      show_train: false
    }
  },
  created() {
  },
  methods: {
    showTrain() {
      this.show_sub_components = true
      this.show_train = true
    },
    showTest() {
      this.show_sub_components = true
      this.show_train = false
    },
    hideSubComponents() {
      this.show_sub_components = false
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
