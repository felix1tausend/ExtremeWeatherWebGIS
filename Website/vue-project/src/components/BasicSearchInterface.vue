<template>
    <button
  id="button1"
  :class="{ closed: !sidebarOpen }"
  @click="sidebarOpen = !sidebarOpen"
>
  {{ sidebarOpen ? '❮❮' : '❯❯' }}
</button>

    <div id="div1"
        :class="{ closed: !sidebarOpen }">
        <div id="navbar2"> 
            <ul id ="ul2">
                <li class="li2">Einfache Suche</li>
                <li class="li2" id = "list2">Erweiterte Suche</li>
                <li class="li2" id = "list3">Statistische Analyse</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
const sidebarOpen = ref(true) 
</script>

<style> 
#div1 {
  position: fixed;
  top: 0;
  left: 0;
  width: 20vw;
  height: 100vh;
  z-index: 2000;
  background-color: rgba(255, 255, 255, 0.836);
  border-right: 2px solid #142d4c;


  transition: transform 0.5s ease;
}
#div1.closed {
  transform: translateX(-100%);
}

#button1{
    position: absolute;
    height: 3vh;
    margin-left: 20vw;
    margin-top: 4vh;
    color: #d9dbdd;
    background-color: #142d4c;
    z-index: 5000;
    border-radius: 2px;
    border-top: 2px groove #304b70;
    border-bottom: 2px groove #304b70;
    border-left: 2px groove #304b70;

    transition: transform 0.5s ease;

}

#button1.closed{
    transform: translateX(-39.5vh);
}

#button1:hover {
  background-color: rgba(56, 81, 112, 0.15);
  cursor: pointer;
}
.li2:hover{
    background-color: rgba(56, 81, 112, 0.15);
    cursor: pointer;
}

#navbar2 {
  width: 20vw;
  height: 3vh;
  padding-top: 4vh;
  font-family: 'Ubuntu', system-ui, sans-serif;
  font-size: 1.3vh;
  color: #d9dbdd;
  background-color: #142d4c;
  z-index: 2000;
  position: fixed;
}

#ul2{
    padding:0px;
}

.li2 {
    border-top: 2px groove #304b70;
    border-bottom: 2px groove #304b70;
    border-radius: 1px;
    background-color: #142d4c;
    width: 20vw;
    height: 3vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

#list2, #list3{
border-left: 2px ridge #304b70;
}




</style>