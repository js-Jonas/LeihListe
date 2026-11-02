<template>
    <v-row class="mt-4" justify="center">
        <v-col cols="12" sm="6" md="4" lg="4">
            <h1 class="text-center">Lendify</h1>
            <h2 class="text-center mt-8">Login</h2>
            <v-form id="loginForm" v-model="loginFormValid" class="mt-6" @submit.prevent="submitLogin">
                <v-text-field v-model="loginForm.email" :rules="emailRules" label="E-Mail"
                    placeholder="Example@studi.com" type="email" autocomplete="email" required>
                </v-text-field>
                <v-text-field v-model="loginForm.password" :rules="passwordRules" label="Passwort"
                    placeholder="Passwort" type="password" autocomplete="current-password" required>
                </v-text-field>
            </v-form>

            <div class="text-center mt-2">
                <!-- TODO Passwort vergessen-->
                <router-link to="/forgot-password">Passwort vergessen?</router-link>
            </div>

            <v-btn block color="primary" variant="elevated" class="mt-8" form="loginForm" type="submit"
                :loading="loading">
                Login
            </v-btn>
            <!-- TODO Registieren existiert noch nicht -->
            <v-btn block color="primary" variant="outlined" class="mt-3" to="/register">
                Registieren
            </v-btn>
        </v-col>
    </v-row>

    <v-snackbar v-model="showSnackbar" :color="snackbarColor" timeout="5000" location="bottom" variant="elevated">
        {{ snackbarMessage }}

        <template v-slot:actions>
            <v-btn variant="text" @click="showSnackbar = false">
                <v-icon>mdi-window-close</v-icon>
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const showSnackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const loading = ref(false)
const loginFormValid = ref(false)
const loginForm = ref({
    email: '',
    password: ''
})

const emailRules = [
    (value: any) => {
        if (value) return true
        return 'E-Mail erforderlich'
    },
    (value: any) => {
        if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return true
        return 'Bitte eine gültige E-Mail-Adresse eingeben.'
    },
]

const passwordRules = [
    (value: any) => {
        if (value) return true
        return 'Passwort erforderlich'
    },
]
// TODO Platzhalter, bis Schbittstelle im Backend da 
async function login(email: string, password: string) {
    console.log('Login-Versuch für', email, password.length)
    throw new Error('Login ist noch nicht an das Backend angebunden.')
}

async function submitLogin() {
    if (!loginFormValid.value) return;

    loading.value = true
    try {
        await login(loginForm.value.email, loginForm.value.password)

        await router.push((route.query.redirect as string) || '/')
    } catch (error: any) {
        snackbarColor.value = 'error'
        if (error.response?.status === 401) {
            snackbarMessage.value = " Fehler beim Login: E-Mail oder Passwort ist falsch."
        } else if (error.response) {
            snackbarMessage.value = " Fehler beim Login:" + error.response.status + " - " + error.response.data?.detail
        } else {
            snackbarMessage.value = " Fehler beim Login:" + error.message
        }
        console.error(snackbarMessage.value)
        showSnackbar.value = true
    }
    finally {
        loading.value = false
    }
}
</script>