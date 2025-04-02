<template>
  <OperadorasLista />
</template>

<script>
import OperadorasLista from './components/OperadorasLista.vue';

export default {
  name: 'App',
  components: {
    OperadorasLista,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    font-family: Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    margin-bottom: 5px;
    word-break: break-word;
  }
}
</style>