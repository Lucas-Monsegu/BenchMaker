<template>
  <div>
    <v-btn
      icon
      class="ml-0"
      @click="dialog = true"
    >
      <v-icon color="white">mdi-information-variant</v-icon>
    </v-btn>
    <v-layout
      row
      justify-center
    >
      <v-dialog
        v-model="dialog"
        width="600px"
      >
        <v-card>
          <v-card-title>
            <span class="headline">What is <span class="font-italic">benchmark.tk</span> ?</span>
          </v-card-title>
          <v-card-text>
            <p>
              This website allows to save and share benchmarks. The benchmarks are created using a dedicated tool which launches N times the benchmark and calculates the average.
              Benchmarks are available for everyone but adding and editing are restricted.
            </p>
            <p>
              If you want to contribute, join the team benchmark laboratory by sending your application to:
              <ul>
                <li>
                  <a href="mailto:lucas.mgu@gmail.com">lucas.mgu@gmail.com</a>
                </li>
                <li>
                  <a href="mailto:queiro_r@epita.fr">queiro_r@epita.fr</a>
                </li>
              </ul>
            </p>
            <p>
              Have a good visualization!
            </p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              flat
              @click="dialog = false"
            >ok !</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
export default {
  data () {
    return {
      dialog: false
    }
  },
  mounted () {
    if (this.$route.path !== '/') {
      this.dialog = true
      this.$router.push('/')
    }
  }
}
</script>
