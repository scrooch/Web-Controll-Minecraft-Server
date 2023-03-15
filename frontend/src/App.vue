<template>
  <v-app id="inspire">
    <v-main class="grey lighten-3">
      <v-container>
        <v-img max-width max-height='300px'
          :src="minecraft_screen"
           style="margin: auto;"
        ></v-img>
        <v-row>
          <v-col
            cols="12"
            sm="2"
            v-if="!isMobile">
            <v-sheet
              rounded="lg"
              class="mt-2"
              min-height="200"
              min-width="190"
            >
              <leftbar></leftbar>
            </v-sheet>
          </v-col>
          <v-col>
            <v-sheet
              rounded="lg"
              class="mt-2"
              :style="{ minHeight: '45vh' }"
            >
                <mainpace></mainpace>
            </v-sheet>
          </v-col>
          <v-col
            cols="12"
            sm="2"
            v-if="!isMobile"
          >
            <v-sheet
              rounded="lg"
              min-height="200"
              class="mt-2"
            >
              <rightbar></rightbar>
            </v-sheet>
          </v-col>
          <v-col
            cols="12"
            sm="2"
            v-if="isMobile">
            <v-sheet
              rounded="lg"
              class="mt-2 pt-2"
              min-height="200"
              min-width="190"
            >
              <leftbar></leftbar>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import minecraft from "@/assets/minecraft.jpg"
  import mainpace from "@/components/mainpace.vue";
  import leftbar from "@/components/leftbar.vue";
  import rightbar from "@/components/rightbar.vue";
  export default {
    data() {
      return {
        minecraft_screen: minecraft,
      }
    },
    components: {
      mainpace, leftbar, rightbar
    },
    computed: {
      // determine if screen width is less than 600px (typical mobile device width)
      isMobile() {
        return this.$vuetify.breakpoint.smAndDown
      }
    }
  }
</script>