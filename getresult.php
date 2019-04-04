<!DOCTYPE html>
<html>
<head>
    <!--Import Google Icon Font-->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--Import materialize.css-->
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>

    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="apple-mobile-web-app-capable" content="yes"><!-- 删除苹果默认的工具栏和菜单栏 -->
    <meta name="apple-mobile-web-app-status-bar-style" content="black"><!-- 设置苹果工具栏颜色 -->
    <meta name="format-detection" content="telphone=no, email=no"><!-- 忽略页面中的数字识别为电话，忽略email识别 -->
    <!-- 启用360浏览器的极速模式(webkit) -->
    <meta name="renderer" content="webkit">
    <!-- 避免IE使用兼容模式 -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!-- 针对手持设备优化，主要是针对一些老的不识别viewport的浏览器，比如黑莓 -->
    <meta name="HandheldFriendly" content="true">
    <!-- 微软的老式浏览器 -->
    <meta name="MobileOptimized" content="320">
    <!-- uc强制竖屏 -->
    <meta name="screen-orientation" content="portrait">
    <!-- QQ强制竖屏 -->
    <meta name="x5-orientation" content="portrait">
    <!-- UC强制全屏 -->
    <meta name="full-screen" content="yes">
    <!-- QQ强制全屏 -->
    <meta name="x5-fullscreen" content="true">
    <!-- UC应用模式 -->
    <meta name="browsermode" content="application">
    <!-- QQ应用模式 -->
    <meta name="x5-page-mode" content="app">
    <!-- windows phone 点击无高光 -->
    <meta name="msapplication-tap-highlight" content="no">
    <!-- 适应移动端end -->
    <meta name="nightmode" content="enable/disable">
    <meta name="imagemode" content="force">
    <!-- 禁用掉uc浏览器判断到页面上文字居多时，会自动放大字体优化移动用户体验。 -->
    <meta name="wap-font-scale" content="no">
</head>

<body>
    <!--Import jQuery before materialize.js-->
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <!-- 导航栏 -->
    <?php include 'top.php';?>
    <!-- 标题 -->
    <div class="container">
    <div class="row">
    <form class="col s12" name="uploadForm" method="post" action="result_process.php"  enctype="multipart/form-data"  onSubmit="return FormCheck()">
        <div class="row">
        <div class="input-field col s12">
            <h2>Result query</h2>
        </div>
        <div class="input-field col s12">
            <input placeholder="Placeholder" id="taskid" type="text" name="taskid" class="validate">
            <label for="taskid">Please enter your task ID</label>
            <button class="btn waves-effect waves-light red accent-4" type="submit" name="action">Submit
                <i class="material-icons right">send</i>
            </button>
        </div>
        </div>
    </form>
    </div>
    <br><br><br><br><br><br><br><br><br>
    </div>
    <!-- 页脚 -->
    <?php include 'footer.php';?>
<script language="javascript">
function FormCheck() {
    if($("#taskid").val().trim().length <= 1){
        return false;
    }
return true;
}
</script>
</body>
</html>