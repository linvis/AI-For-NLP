<template>
  <div id="app">
    <div>
      <md-field>
        <label>Original News</label>
        <md-textarea v-model="text_news"></md-textarea>
      </md-field>
    </div>

    <md-dialog-alert
      :md-active.sync="error_alert"
      md-title="Error!"
      md-content="Empty News" />

    <div id="parse">
      <md-button class="md-dense md-raised md-primary" v-on:click="catch_news({text_news})">解析</md-button>
    </div>

    <div>
      <md-field>
        <label>News Abstract</label>
        <md-textarea v-model="text_abstract"></md-textarea>
      </md-field>
    </div>

    <router-view/>
  </div>
</template>

<script>
  import axios from 'axios'

export default {
  name: 'app',
  data: () => ({
    error_alert: false
  }),

  methods: {
    catch_news (text) {

      var contents = text.text_news

      if (contents == null || contents.length === 0) {
        this.error_alert = true
        return -1
      }

      // post to backend
      this.postNews(contents)

    },

    postNews (contents) {
      const path = 'http://localhost:5000/news'

      axios.post(path, contents, {headers: {"Content-Type": "text/plain"}})
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.log(error)
        });
    }
  }
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

