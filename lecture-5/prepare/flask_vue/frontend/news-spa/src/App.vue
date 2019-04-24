<template>
  <div id="app">
    <div>
      <md-field>
        <label>Original News</label>
        <md-textarea v-model="textarea"></md-textarea>
      </md-field>
    </div>

    <div>
      <md-button class="md-dense md-raised md-primary">Raised</md-button>
    </div>

    <div>
      <md-field>
        <label>News Abstract</label>
        <md-textarea v-model="textarea"></md-textarea>
      </md-field>
    </div>

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style lang="scss" scoped>
  @import "~vue-material/dist/theme/engine";

  .md-layout-item {
    height: 40px;

    &:nth-child(1) {
      background: md-get-palette-color(grey, 300);
    }

    &:nth-child(2) {
      background: md-get-palette-color(grey, 400);
    }

    &:nth-child(3) {
      background: md-get-palette-color(grey, 500);
    }
  }
</style>
