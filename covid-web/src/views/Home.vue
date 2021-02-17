<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import json from '@/assets/data.json'

export default {
  name: 'Home',
  components: {
    HelloWorld
  },
  mounted () {
    console.log(json)
  }
}
</script>
