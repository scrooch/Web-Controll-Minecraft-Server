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
    <v-card class="ma-1">
    <v-list dense>
      <v-subheader>Tabela zwycięzców</v-subheader>
      <v-list-item-group
        v-model="selectedItem"
        color="primary"
      >
        <v-list-item
          v-for="(status, user) in sortedUsers"
          :key="user"
        >
          <v-list-item-content>
            <v-list-item-title>{{ user }}: {{ status.time }}h</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
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
      apidata_users: '',
    }
  },
  computed: {
    sortedUsers() {
      return Object.entries(this.apidata_users)
        .sort(([, a], [, b]) => b.time - a.time)
        .reduce((obj, [key, val]) => {
          obj[key] = val;
          return obj;
        }, {});
    }
  },
  mounted() {
    axios.get(`${process.env.VUE_APP_API_URL}/avaible`, {headers: {'Access-Control-Allow-Origin': '*'}})
      .then(response => {
        this.apidata_users = response.data.Users;
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