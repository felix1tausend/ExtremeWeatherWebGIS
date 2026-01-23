<template>
    <div id="div1"
        :class="{ closed: !sidebarOpen }">
        <div id="navbar2"> 
            <ul id ="ul2">
                <li class="li2"><button class="navbar2button" @click="active = 'fundamental'">Einfache Suche</button></li>
                <li class="li2" id = "list2"><button class="navbar2button">Erweiterte Suche</button></li>
                <li class="li2" id = "list3"><button class="navbar2button">Statistische Analyse</button></li>
            </ul>
        </div>
          <button
            id="button1"
            :class="{ closed: !sidebarOpen }"
            @click="sidebarOpen = !sidebarOpen"
>
             {{ sidebarOpen ? '❮❮' : '❯❯' }}
        </button>
        <FundamentalSearch v-if="active === 'fundamental'" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import FundamentalSearch from '@/components/FundamentalSearch.vue'
const sidebarOpen = ref(true) 
const active = ref(null)
</script>

<style> 
#div1 {
  height: 100vh;
  width: 400px;
  position: fixed;
  z-index: 1000;
  border-right: 2px solid #142d4c;
  background-color: rgba(255, 255, 255, 0.836);
  transition: transform 0.5s ease;
  
}

#div1.closed {
  transform: translateX(-100%);
}

#navbar2 {
  height: 50px;
  width: 100%;
  padding-top: 40px;
  background-color: #142d4c;
}
.navbar2button{
    height: 100%;
    width: 100%;
    border: transparent;
    background-color: #142d4c;
    font-family: 'Ubuntu', system-ui, sans-serif;
    font-size: 100%;
    color: #d9dbdd;
    box-shadow: 0 1px 10px rgb(0, 0, 0);
}
.navbar2button:hover{
    background-color: rgb(56, 81, 112);
    cursor: pointer;
}


#ul2{
    padding:0px;
}

.li2 {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    border-top: 2px groove #304b70;
    border-bottom: 2px groove #304b70;
    border-radius: 1px;
    background-color: #142d4c;
}

#list2, #list3{
border-left: 2px ridge #304b70;
}

#button1{
    height: 52px;;
    width: 30px;
    position: absolute;
    top: 40px;
    right: -30px;
    border-radius: 2px;
    border-top: 2px groove #304b70;
    border-bottom: 2px groove #304b70;
    border-left: 2px groove #304b70;
    background-color: #142d4c;
    text-align: right;
    color: #d9dbdd;
    box-shadow: 0 1px 10px rgb(0, 0, 0);
}


#button1:hover {
  background-color: rgb(56, 81, 112);
  cursor: pointer;
}




</style>