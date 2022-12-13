<template>
  <v-content>
    <v-layout
      py-2
      px-2
      fill-height
      wrap
    >
      <v-flex
        py-2
        px-2
        xs12
        md4
      >
        <v-card class="card">
          <v-layout
            column
            fill-height
          >
            <v-sheet class="pa-3 primary lighten-2">
              <v-layout>
                <AboutModal />
                <v-text-field
                  ref="input"
                  v-model="search"
                  label="Search benchmark"
                  dark
                  flat
                  solo-inverted
                  hide-details
                  clearable
                  clear-icon="mdi-close-circle-outline"
                ></v-text-field>
                <v-btn
                  icon
                  class="mr-0"
                  @click="refresh"
                >
                  <v-icon color="white">{{ icon }}</v-icon>
                </v-btn>
              </v-layout>
            </v-sheet>
            <v-flex
              grow
              id="cardTree"
            >
              <v-treeview
                class="scroll"
                ref="tree"
                :search="search"
                :active.sync="active"
                :open.sync="open"
                :items="items"
                activatable
                item-key="name"
                item-text="shortname"
                open-on-click
                item-children="contents"
              >
                <template v-slot:prepend="{ item, open }">
                  <v-icon v-if="item.type === 'directory'">
                    {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
                  </v-icon>
                  <v-icon v-else>
                    mdi-file
                  </v-icon>
                </template>
              </v-treeview>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex
        px-2
        py-2
      >
        <v-card class="card">
          <v-layout
            v-if="!selected"
            column
            fill-height
            justify-center
            height="100%"
          >
            <div class="text-xs-center headline grey--text font-weight-light">
              Select a benchmark
            </div>
          </v-layout>
          <v-layout
            v-else-if="!benchmark[selected]"
            column
            fill-height
            justify-center
          >
            <div class="text-xs-center">
              <v-progress-circular
                color="primary"
                indeterminate
              ></v-progress-circular>
            </div>
          </v-layout>
          <v-layout
            class="scroll"
            v-else
            column
          >
            <v-layout
              shrink
              justify-center
              mb-2
              wrap
            >
              <v-chip
                label
                color="primary lighten-2"
                text-color="white"
                disabled
              >
                <v-icon left>mdi-account</v-icon>{{ benchmark[selected].AUTHOR }}
              </v-chip>
              <v-chip
                label
                color="primary lighten-2"
                text-color="white"
                disabled
              >
                <v-icon left>mdi-file</v-icon>{{ benchmark[selected].NAME }}
              </v-chip>
              <v-chip
                label
                color="primary lighten-2"
                text-color="white"
                disabled
              >
                <v-icon left>mdi-chip</v-icon>{{ benchmark[selected].CPU }}
              </v-chip>
            </v-layout>
            <v-layout
              shrink
              justify-center
              my-2
            >
              <v-flex
                xs12
                md8
              >
                <v-sheet
                  color="grey lighten-2"
                  elevation="2"
                  class="break-word pa-2"
                >
                  <div class="title text-xs-center pb-2">Description</div>
                  <div class="text-xs-center">{{ benchmark[selected].DESCRIPTION }}</div>
                </v-sheet>
              </v-flex>
            </v-layout>
            <component
              :key="selected"
              :bench="benchmark[selected]"
              class="my-2"
              :is="benchmark[selected].RANGE ? 'LineChart' : 'BarChart'"
            />
            <div class="my-2 title text-xs-center">Code</div>
            <v-layout
              justify-center
              wrap
            >
              <v-flex
                shrink
                xs12
                md8
                v-for="(item, index) in benchmark[selected].TESTS"
                :key="index"
              >
                <div class="mt-1 subheading text-xs-center">{{ index }}</div>
                <div class="body-2 text-xs-center">{{ item.numberoftests }} tests - {{ item.version}}</div>
                <highlight-code
                  class="nobefore"
                  auto
                >
                  {{ item.code }}
                </highlight-code>
              </v-flex>
            </v-layout>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-content>
</template>

<script>
import axios from 'axios'
import BarChart from '@/components/BarChart'
import LineChart from '@/components/LineChart'
import AboutModal from '@/components/AboutModal'

export default {
  name: 'Home',
  components: { BarChart, AboutModal, LineChart },
  data () {
    return {
      icon: 'mdi-reload',
      loading: false,
      benchmark: {},
      search: '',
      open: [],
      tree: [],
      active: [],
      items: []
    }
  },
  computed: {
    selected () {
      return this.active[0]
    }
  },
  watch: {
    selected: 'getFile'
  },
  methods: {
    range (min, max, step = 1) {
      const arr = []
      const totalSteps = Math.floor((max - min) / step)
      for (let ii = 0; ii <= totalSteps; ii++) { arr.push(ii * step + min) }
      return arr
    },
    hslToRgb (h, s, l) {
      let r, g, b
      if (s === 0) {
        r = g = b = l
      } else {
        const hue2rgb = function hue2rgb (p, q, t) {
          if (t < 0) t += 1
          if (t > 1) t -= 1
          if (t < 1 / 6) return p + (q - p) * 6 * t
          if (t < 1 / 2) return q
          if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6
          return p
        }
        let q = l < 0.5 ? l * (1 + s) : l + s - l * s
        let p = 2 * l - q
        r = hue2rgb(p, q, h + 1 / 3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1 / 3)
      }
      return '#' + Math.round(r * 255).toString(16) + Math.round(g * 255).toString(16) + Math.round(b * 255).toString(16)
    },
    generate_colors (n) {
      let step = 360 / n
      let li = []
      for (let i = 0; i < n; ++i) {
        li.push(this.hslToRgb((step * i + 5) / 360, 0.75, 0.65))
      }
      return li
    },
    getFile (selected) {
      if (selected && !this.benchmark[selected]) {
        return axios(selected).then(res => {
          let data = res.data
          const split = selected.split('/')
          data.NAME = split[split.length - 1]
          if (!data.DESCRIPTION) { data.DESCRIPTION = 'Empty' }
          if (!data.AUTHOR) { data.AUTHOR = 'Anonymous' }
          if (!data.RANGE) {
            data.VALUES = []
            for (let key in data.TESTS) { data.VALUES.push(data.TESTS[key].average) }
          } else {
            data.RANGE = this.range(...data.RANGE)
            data.COLORS = this.generate_colors(Object.keys(data.TESTS).length)
          }
          this.$set(this.benchmark, selected, data)
        }).catch(() => {
          console.log('error')
        })
      }
      return Promise.resolve()
    },
    getFiles () {
      return axios('/api/git-tree').then(res => {
        this.items = res.data
        this.$nextTick(() => {
          this.$refs.tree.updateAll(true)
        })
      })
    },
    refresh () {
      this.getFiles().then(() => {
        this.benchmark = {}
        this.getFile(this.selected).then(() => {
          this.icon = 'mdi-check'
          setTimeout(() => {
            this.icon = 'mdi-reload'
          }, 500)
        })
      })
    }
  },
  mounted () {
    this.getFiles()
    this.$refs.input.focus()
  }
}
</script>

<style>
.v-treeview-node__root {
  padding-right: 4px;
  overflow: hidden;
}
.break-word {
  word-wrap: break-word;
}
@media screen and (max-width: 959px) {
  .card {
    min-height: 500px;
    height: 100%;
  }
  .scroll {
    padding: 8px;
  }
}
@media screen and (min-width: 960px) {
  .card {
    height: 100%;
    position: relative;
  }
  .scroll {
    overflow-y: auto;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE 10+ */
    position: absolute;
    top: 8px;
    bottom: 8px;
    right: 8px;
    left: 8px;
  }
  .scroll::-webkit-scrollbar {
    width: 0;
    height: 0;
  }
  #cardTree {
    position: relative;
  }
}
.nobefore *:before {
  content: none;
}
.nobefore > * {
  padding: 15px 30px 15px 30px !important;
}
#aboutmodal {
  position: absolute;
  top: 0;
  right: 0;
}
</style>
