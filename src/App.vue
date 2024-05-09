<!-- App.vue -->
<template>
    <div id="app">
        <div class="navbar-overlay"></div>
        <nav class="navbar">
            <div class="navbar-content">
                <div class="navbar-background"></div>
                <div class="navbar-logo">
                    <img src="@\assets\nav\logo_hots.png" alt="Logo">
                </div>
                <ul class="navbar-menu">
                    <li><router-link to="/">Home</router-link></li>
                    <li><router-link to="/heroes">Heroes</router-link></li>
                </ul>
            </div>
        </nav>
        <router-view></router-view>
    </div>
</template>


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
    /* Add the border at the bottom */
    box-shadow: 0 5px 10px rgba(173, 233, 245, 0.3), 0 10px 20px rgba(173, 233, 245, 0.2), 0 15px 30px rgba(173, 233, 245, 0.1);
    /* Add the shadow effect */
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
    /* Adjust the padding to create space for the logo */
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
    /* Add margin to the logo */
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

<script>
export default {
    name: 'App',
}
</script>