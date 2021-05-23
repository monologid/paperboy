<template>
  <div class='grid grid-cols-1 md:grid-cols-5'>
    <div>
      <div class="font-bold text-center py-5 uppercase">#PaperBoy</div>
      <div class="px-3 py-5">
        <button v-on:click="createNewJob" class="w-full hover:bg-gray-100 border border-dashed py-2 pb-4 text-xs uppercase text-center text-gray-400 font-bold tracking-wider">
          <div class="text-lg">+</div>
          Create a new Job
        </button>
      </div>
      <div class="px-5 py-3 cursor-pointer hover:bg-gray-100"
           v-for="job in jobs"
           :key="job"
           v-on:click="onClickJob(job)">
        {{ job }}
      </div>
    </div>
    <CodeEditor v-bind:code="code" />
  </div>
</template>

<script>
import CodeEditor from "./components/CodeEditor";

export default {
  name: 'App',
  components: {
    CodeEditor
  },
  data: () => ({
    jobs: [],
    code: JSON.stringify({}, null, 2),
    defaultCode: {
      name: 'your-job-name-no-space-and-should-be-in-lowercase',
      description: '',
      cron: [
        {
          "type": "day",
          "value": [
            {
              "day": "saturday",
              "time": ["11:28", "11:26"]
            }
          ]
        },
        { "type": "seconds", "value": 5 }
      ],
      tasks: [
        {
          id: 'task-id',
          description: '',
          plugin: 'view-plugins-directory-for-further-info',
          args: {}
        }
      ]
    }
  }),
  methods: {
    getAllJobs: function () {
      const self = this
      const url = `/api/v1/job`;
      fetch(url).then(resp => resp.json())
        .then(resp => {
          if (resp.success) self.jobs = resp.data;
        })
        .catch(e => {
          alert(e);
        });
    },
    createNewJob: function () {
      this.code = JSON.stringify(this.defaultCode, null, 2);
    },
    onClickJob: function (job) {
      const self = this
      const url = `/api/v1/job/${job}`;
      fetch(url).then(resp => resp.json())
        .then(resp => {
          if (resp.success) self.code = JSON.stringify(resp.data, null, 2);
        })
        .catch(e => {
          alert(e);
        });
    }
  },
  beforeMount() {
    this.getAllJobs();
  }
}
</script>
