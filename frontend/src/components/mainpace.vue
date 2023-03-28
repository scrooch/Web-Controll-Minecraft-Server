<template>
  <div>
    <v-container>
      <v-card class="pa-2 text-center text-h4">
          Status serwera minecraft: <span :class="{'text-green': apidata.Server === 'Online', 'text-red': apidata.Server === 'Offline'}">{{ apidata.Server }}</span>
        <v-dialog
        v-if="!isRunning && showButton"
          v-model="dialog"
          persistent
          max-width="800"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="red"
              style="margin-bottom: 5px; margin-left: 10px;"
              v-bind="attrs"
              v-on="on"
            >
                Zrestartuj serwer
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h5">
              Czy jesteś pewien, że chcesz zrestartować minecraft serwer?
            </v-card-title>
            <v-card-text>
                          Po zestartowaniu:<br/>
                          - Zrestaruje się tabela zwyciężców<br/>
                          - Czas ostatniego logowania użytkowników się zrestartuje<br/>
                          <br/>

                          PS. Nie jesteś inkognito
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="green darken-1"
                text
                @click="dialog = false"
              >
                Nie
              </v-btn>
              <v-btn
                color="green darken-1"
                text
                @click="restartServer()"
              >
                Tak
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card>
      <v-row :align="align" no-gutters style="min-height: 150px;">
        <v-col v-for="(status, user) in apidata.Users" :key="user" :class="{'mb-3': $vuetify.breakpoint.width < 600}">
          <v-card v-if="isMobile" class="pa-1" elevation="2"  @click="snack_online(status.last_in)">
            <v-avatar size="45px">
              <img :src="image[user]" alt="users[user].name">
            </v-avatar>
            <v-item><span :class="{'text-green': status.state === 'Online', 'text-red': status.state === 'Offline'}">{{ status.state }}</span></v-item>

        </v-card>
        <v-snackbar
            style="text-align: center"
            v-model="snackbar"
            :timeout="timeout"
        >
            Ostatni raz: {{ snack_text ? snack_text : 'Brak danych' }}
        </v-snackbar>
          <v-card
            v-if="!isMobile"
            class="mx-auto"
            max-width="344"
            outlined
          >
          <v-list-item three-line>
            <v-list-item-content>
              <div class="text-overline mb-4">
                <span :class="{'text-green': status.state === 'Online', 'text-red': status.state === 'Offline'}">{{ status.state }}</span>
              </div>
              <v-list-item-title class="text-h5 mb-1">
                {{ user }}
              </v-list-item-title>
              <v-list-item-subtitle>Ostani raz:<br>{{ status.last_in ? status.last_in : 'Brak danych' }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar
              size="45"
            ><img :src="image[user]" alt="users[user].name"></v-list-item-avatar>
          </v-list-item>
        </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'MyComponent',
  data() {
    return {
      align: 'center',
      apidata: '',
      snackbar: false,
      timeout: 2000,
      snack_text: '',
      dialog: false,
      showButton: false,
    }
  },
  created(){
    this.image = JSON.parse(process.env.VUE_APP_IMAGES);
  },
  mounted() {
    axios.get(`${process.env.VUE_APP_API_URL}/avaible`, {headers: {'Access-Control-Allow-Origin': '*'}})
      .then(response => {
        this.apidata = response.data;
        setTimeout(() => {
        this.showButton = true;
      }, 1000);
      })
      .catch(error => {
        console.log(error);
      });
  },
  methods: {
    snack_online(text_value){
        this.snack_text=text_value
        this.snackbar=true
    },
    async restartServer() {
      try {
        await axios.post(`${process.env.VUE_APP_API_URL}/reload`, {});
      } catch (error) {
        console.error(error);
      }
      this.dialog = false
      window.location.reload();
    }
  },

  computed: {
      // determine if screen width is less than 600px (typical mobile device width)
      isMobile() {
        return this.$vuetify.breakpoint.smAndDown
      },
      isRunning(){
        return this.apidata.Server==='Online'
      }
    }
}
</script>

<style scoped>
  .text-green {
    color: green;
  }
  .text-red {
    color: red;
  }
</style>
