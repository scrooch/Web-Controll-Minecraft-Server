<template>
  <div>
    <v-container>
      <v-card class="pa-2 text-center text-h4">
          Status serwera minecraft: <span :class="{'text-green': apidata.Server === 'Online', 'text-red': apidata.Server === 'Offline'}">{{ apidata.Server }}</span>
      </v-card>
      <v-row :align="align" no-gutters style="min-height: 150px;">
        <v-col v-for="(status, user) in apidata.Users" :key="user" :class="{'mb-3': $vuetify.breakpoint.width < 600}">
          <v-card v-if="isMobile" class="pa-1" elevation="2">
            <v-avatar size="45px">
              <img :src="image[user]" alt="users[user].name">
            </v-avatar>
            <v-item><span :class="{'text-green': status.state === 'Online', 'text-red': status.state === 'Offline'}">{{ status.state }}</span></v-item>
        </v-card>
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
import KaziulaImage from '@/assets/kazik.jpg';
import ScroochImage from '@/assets/scrooch.jpg';
import DzieminImage from '@/assets/dziemin.jpg';
import AdasImage from '@/assets/adas.jpg';
import PiksonImage from '@/assets/pikson.jpg';

export default {
  name: 'MyComponent',
  data() {
    return {
      align: 'center',
      apidata: '',
      image:{
        ScroochPL: ScroochImage,
        dziemin4812: DzieminImage,
        Kaziula2496: KaziulaImage,
        MrKopciak: AdasImage,
        PiksoKN: PiksonImage
      }
    }
  },
  mounted() {
    axios.get(`${process.env.VUE_APP_API_URL}/avaible`, {headers: {'Access-Control-Allow-Origin': '*'}})
      .then(response => {
        this.apidata = response.data;
      })
      .catch(error => {
        console.log(error);
      });
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
  .text-green {
    color: green;
  }
  .text-red {
    color: red;
  }
</style>
