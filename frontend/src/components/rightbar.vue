<template>
  <v-container>
    <v-card class="ma-1">
      <v-card-subtitle>
        Versja minecraft: <span style="color: green">{{ apidata_version }}</span>
      </v-card-subtitle>
    </v-card>
    <v-card class="ma-1">
      <v-card-subtitle>
        Data ostatniego uruchomienia: <span style="color: green">{{ apidata_date }}</span>
      </v-card-subtitle>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "leftbar",
  data() {
    return {
      apidata_version: '',
      apidata_date: '',
    }
  },
  mounted() {
  axios.get(`${process.env.VUE_APP_API_URL}/avaible`, {headers: {'Access-Control-Allow-Origin': '*'}})
    .then(response => {
      this.apidata_date = response.data.ServerDate.toLocaleString().replace('T', '\n');
      this.apidata_version = response.data.ServerVersion;
    })
    .catch(error => {
      console.log(error);
    });
}

}
</script>

<style scoped>

</style>