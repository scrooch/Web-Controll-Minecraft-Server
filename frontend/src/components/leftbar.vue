<template>
  <div class="text-center ma-2">
    <v-btn
      dark
      @click="postRequest('clear')"
      class="ma-2"
      width="190px"
      elevation="8"
    >
      Wyłącz deszcz
    </v-btn>
    <v-btn
      dark
      @click="postRequest('day')"
      class="ma-2"
      width="190px"
      elevation="8"
    >
      Zrób dzień
    </v-btn>
    <v-snackbar
      style="text-align: center"
      v-model="snackbar"
      :timeout="timeout"
    >
      {{ snackbartext }}
    </v-snackbar>
    <v-btn
        v-if="!isMobile"
        dark
        class="ma-2"
        width="190px"
        elevation="8"
        @click="launchMinecraft"
    >
      Uruchom Minecraft
    </v-btn>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "leftbar",
  data: () => ({
      snackbar: false,
      snackbar2: false,
      snackbartext: `Hello, I'm a snackbar`,
      timeout: 4000,
    }),
  methods: {
    launchMinecraft() {
      const serverIP = process.env.VUE_APP_MINECRAFT_IP;
      const serverName = 'Scrooch Server';
      const encodedIP = encodeURIComponent(serverIP);
      const encodedName = encodeURIComponent(serverName);
      const url = `minecraft://?addExternalServer=${encodedName}%7C${encodedIP}`;
      window.location.href = url;
    },
    async postRequest(command) {
      try {
        await axios.post(`${process.env.VUE_APP_API_URL}/${command}`, {
          // Tu możesz przekazać dane do wysłania w żądaniu POST
        });
        if(command === 'day'){
          this.snackbar = true
          this.snackbartext = 'Wysłano komendę: Ustaw dzień na serwerze'
        }
        if(command === 'clear'){
          this.snackbar = true
          this.snackbartext = 'Wysłano komendę: Wyczyść deszcz'
        }

      } catch (error) {
        console.error(error);
      }
    }
  },
  computed: {
      // determine if screen width is less than 600px (typical mobile device width)
      isMobile() {
        return this.$vuetify.breakpoint.smAndDown
      }
    }
}
</script>

<style scoped>

</style>