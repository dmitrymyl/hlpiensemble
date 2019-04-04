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
        <br />
        <br />
        <h1 class="header center red-text">HLPI-Ensemble</h1>
        <div class="row center">
            <h5 class="header col s12 light">A model designed specifically for human lncRNA-protein interaction prediction</h5>
        </div>
        <div class="row center">
            <a href="./prediction.php" id="download-button" class="btn-large waves-effect waves-light red accent-4">Get Started</a>
        </div>
    </div>
    <div class="container">
    <div class="section">
    <!--   Icon Section   -->
    <div class="row">
    <div class="col s12 m4">
      <div class="icon-block">
        <h2 class="center red-text"><i class="medium material-icons">view_column</i></h2>
        <h5 class="center">Three mainstream methods</h5>
        <p class="light">HLPI-Ensemble consists of the three mainstream machine learning models of SVM, RF and XGB.</p>
      </div>
    </div>
    <div class="col s12 m4">
      <div class="icon-block">
        <h2 class="center red-text"><i class="medium material-icons">extension</i></h2>
        <h5 class="center">Based on ensemble strategy</h5>
        <p class="light">The ensemble strategy integrates multiple sub models, which takes advantage of the HLPI-ensemble sub model.</p>
      </div>
    </div>
    <div class="col s12 m4">
      <div class="icon-block">
        <h2 class="center red-text"><i class="medium material-icons">data_usage</i></h2>
        <h5 class="center">The special training data</h5>
        <p class="light">The training data of HLPI-Ensemble were extracted from NPInter v2.0 human lncRNA-protein interaction data.</p>
      </div>
    </div>
    </div>
    </div>
    <br><br>
    </div>
    <!-- 页脚 -->
    <?php include 'footer.php';?>
</body>
</html>