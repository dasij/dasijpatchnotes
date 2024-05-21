<template>
    <div id="app">
        <div class="navbar-overlay"></div>
        <nav class="navbar">
            <div class="navbar-content">
                <div class="navbar-background"></div>
                <div class="navbar-logo">
                    <router-link to="/">
                        <img src="@/assets/nav/logo_hots.png" alt="Logo">
                    </router-link>
                </div>
                <ul class="navbar-menu">
                    <li><router-link to="/heroes">Heroes</router-link></li>
                </ul>
                <ul class="navbar-menu">
                    <li><router-link to="/Maps">Maps</router-link></li>
                </ul>
                <ul class="navbar-menu">
                    <li><router-link to="/General">General</router-link></li>
                </ul>
                <ul class="navbar-menu">
                    <li><router-link to="/Gamemodes">Gamemodes</router-link></li>
                </ul>
                <ul class="navbar-menu">
                    <li>
                        <button @click="isUserLoggedIn ? handleLogout() : openLoginModal()">
                            {{ isUserLoggedIn ? 'Sign Out' : 'Login' }}
                        </button>
                    </li>
                </ul>
            </div>
        </nav>
        <router-view @open-login-modal="openLoginModal"></router-view>

        <!-- Login Modal -->
        <div v-if="showLoginModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div class="bg-white p-6 rounded-lg shadow-lg text-center">
                <h2 class="text-2xl font-bold mb-4">Choose a login method</h2>
                <div class="flex flex-col space-y-4">
                    <button @click="handleLogin('google')"
                        class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700">
                        Login with Google
                    </button>
                    <!-- <button @click="handleLogin('facebook')"
                        class="bg-blue-800 text-white py-2 px-4 rounded hover:bg-blue-900">
                        Login with Facebook
                    </button>-->
                    <button @click="closeLoginModal" class="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-700">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { auth, googleProvider, facebookProvider } from './firebase';
import { signInWithPopup, signOut } from 'firebase/auth';

export default {
    name: 'App',
    data() {
        return {
            isUserLoggedIn: false,
            showLoginModal: false,
        };
    },
    methods: {
        openLoginModal() {
            this.showLoginModal = true;
        },
        closeLoginModal() {
            this.showLoginModal = false;
        },
        handleLogin(providerName) {
            const provider = providerName === 'google' ? googleProvider : facebookProvider;
            signInWithPopup(auth, provider)
                .then(result => {
                    console.log('User logged in:', result.user);
                    this.isUserLoggedIn = true;
                    this.closeLoginModal();
                })
                .catch(error => {
                    console.error('Error during authentication:', error);
                });
        },
        handleLogout() {
            signOut(auth)
                .then(() => {
                    console.log('User logged out');
                    this.isUserLoggedIn = false;
                })
                .catch(error => {
                    console.error('Error during logout:', error);
                });
        },
        checkUserLogin() {
            auth.onAuthStateChanged(user => {
                this.isUserLoggedIn = !!user;
                if (this.isUserLoggedIn) {
                    this.closeLoginModal();
                }
            });
        }
    },
    mounted() {
        this.checkUserLogin();
    }
};
</script>




<style>
.navbar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 150px;
    background-color: rgba(0, 0, 0, 0.4);
    z-index: 0;
    background-image: url('@/assets/talents/talents_bg.webp');
    background-size: cover;
    background-position: center;
    border-bottom: 2px solid #ccf4fc;
    box-shadow: 0 5px 10px rgba(173, 233, 245, 0.3), 0 10px 20px rgba(173, 233, 245, 0.2), 0 15px 30px rgba(173, 233, 245, 0.1);
}

.navbar {
    display: flex;
    justify-content: center;
    padding: 0;
    background-color: transparent;
    position: relative;
    z-index: 1;
    padding-top: 50px;
    padding-bottom: 50px;
}

.navbar-content {
    display: flex;
    align-items: center;
    max-width: 1200px;
    width: 100%;
    position: relative;
    height: 50px;
    padding-left: 280px;
}

.navbar-background {
    position: absolute;
    top: 0;
    left: 200px;
    width: calc(100% - 200px);
    height: 100%;
    background: linear-gradient(to right, #04459F, #2D0699);
    z-index: -1;
    border-radius: 10px;
}

.navbar-logo {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    z-index: 2;
    margin-left: 1rem;
}

.navbar-logo a {
    display: block;
}

.navbar-logo img {
    height: auto;
    width: auto;
    margin-left: 1rem;
    max-width: none;
}

.navbar-menu {
    margin-left: 1rem;
    display: flex;
    align-items: center;
    color: #fff;
    text-decoration: none;
    font-family: "Blizzard", sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: color 0.2s ease;
    height: 100%;
}

.navbar-menu li {
    margin-left: 1rem;
    display: flex;
    align-items: center;
    color: #fff;
    text-decoration: none;
    font-family: "Blizzard", sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: background-color 0.3s ease;
    padding: 0 5px;
    height: 100%;
}

.navbar-menu li a {
    color: #CCCCFF;
    text-decoration: none;
    display: flex;
    align-items: center;
    height: 100%;
    padding: 0 10px;
}

.navbar-menu li a:hover {
    color: #fff;
}

.navbar-menu li:hover {
    background: linear-gradient(to bottom, #1238A2, #00AAFF);
}
</style>
