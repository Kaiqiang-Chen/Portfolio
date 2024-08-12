<template>
<div class="silde_box">
    <slide-verify
    :w="350" :h="200"
    class="silde_box"
    ref="block"
    :slider-text="text"
    :accuracy="accuracy"
    @again="onAgain"
    @success="onSuccess"
    @fail="onFail"
    @refresh="onRefresh"
    :imgs="imgs"
    ></slide-verify>
    <button class="btn" @click="handleClick" v-show="false">在父组件可以点我刷新哦</button>
    <div>{{ msg }}</div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import SlideVerify, { SlideVerifyInstance } from "vue3-slide-verify";
import "vue3-slide-verify/dist/style.css";
import cat from '../assets/v.jpg'
import bus from '../bus'
export default defineComponent({
components: { SlideVerify },

setup() {
    const imgs=[cat]
    const msg = ref("");
    const block = ref<SlideVerifyInstance>();

    const onAgain = () => {
    // 刷新
    block.value?.refresh();
    };
    bus.on('verify_refresh',(e)=>{
        
        block.value?.refresh();
    })
    const onSuccess = (times: number) => {
        bus.emit('verified','true')
    };

    const onFail = () => {
    };

    const onRefresh = () => {
        bus.emit('verify_refreshed','1')
    };

    const handleClick = () => {
    // 刷新
    block.value?.refresh();
    msg.value = "";
    };

    return {
    imgs,
    block,
    msg,
    text: "向右滑动->",
    accuracy: 3,
    onAgain,
    onSuccess,
    onFail,
    onRefresh,
    handleClick,
    };
},
});
</script>
<style scoped>
.silde_box{
margin:0 auto;
}
</style>