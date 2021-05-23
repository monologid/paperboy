<template>
  <div class="col-span-4 h-screen">
    <prism-editor
        v-model="content"
        :highlight="highlighter"
        :line-numbers="true"
        class="w-full h-screen code-editor" />

    <div class="fixed top-0 right-10">
      <button v-on:click="save" class="bg-red-500 hover:bg-red-700 text-white px-6 py-2 uppercase text-sm tracking-wider font-semibold">Save</button>
    </div>
  </div>
</template>

<script>
import { PrismEditor } from 'vue-prism-editor';
import 'vue-prism-editor/dist/prismeditor.min.css';
import { highlight, languages } from "prismjs/components/prism-core";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-json";
import "prismjs/themes/prism-tomorrow.css";

export default {
  name: "CodeEditor",
  components: {
    PrismEditor
  },
  props: {
    code: String
  },
  data: () => ({
    content: ''
  }),
  watch: {
    code() {
      this.content = this.$props.code;
    }
  },
  methods: {
    highlighter(code) {
      return highlight(code, languages.json); //returns html
    },
    save() {
      if (this.content.length == 0) {
        alert('Job configuration cannot be empty');
        return
      }

      fetch('/api/v1/job', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: this.content
      })
      .then(resp => resp.json())
      .then(resp => {
        if (resp.success) {
          alert('Configuration has been saved. Reloading the page ...')
          return window.location.reload()
        }
      })
      .catch(e => alert(e))
    }
  }
}
</script>

<style scoped>
.code-editor {
  background: #2d2d2d;
  color: #ccc;
  width: 100% !important;
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
}
</style>