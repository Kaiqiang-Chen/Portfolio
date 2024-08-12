<template>
  <div class="parent-container">
    <div class="container1">
      <span class="hello-text">房地产公司查询案例</span>
      <br><br><br>
      <img src="../assets/real_estate_example.jpg" alt="Image 1" class="hello-image">
    </div>
    <div class="container2">
      <span class="hello-text">供应商企业查询案例</span>
      <br><br><br>
      <img src="../assets/supplier_example.jpg" alt="Image 1" class="hello-image">
    </div>
  </div>
</template>

<script>
// export default {
//   name: "example"
// }
</script>

<style scoped>
.parent-container {
  display: flex; /* 使用 flexbox */
  justify-content: center; /* 将子元素水平居中 */
}
.container1
.container2{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.container1{
  border-radius: 20px;
  background-color: #c7edf6;
  margin: auto;
  padding: 40px;
  width:550px;
  margin-top: 80px;
  white-space:nowrap ;
  margin-right: 20px; /* 添加一些间距 */
  text-align: center;
}

.container2{
  border-radius: 20px;
  background-color: #c7edf6;
  margin: auto;
  padding: 40px;
  width:550px;
  margin-top: 80px;
  white-space:nowrap ;
  margin-left: 20px; /* 添加一些间距 */
  text-align: center;
}

.hello-text {
  font-size: 24px; /* 字号更大 */
  color: black ;/* 文字颜色变蓝 */
  margin: auto;
}

.hello-image {
  max-width: 100%; /* 图片宽度最大为容器宽度 */
  height: auto; /* 图片高度自动调整 */
}
</style>