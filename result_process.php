<?php
header("Content-type: text/html; charset=utf-8");
//获取任务ID
if(isset($_GET['taskid'])){
    $taskuuid=$_GET['taskid'];
}else{
    if(isset($_POST['taskid'])){
        $taskuuid=$_POST['taskid'];
    }else{
        header("Location: ./error.php?msg=Unauthorized access!");
    }
}
//$taskuuid=$_GET['taskid'];
$taskfolder="task/".$taskuuid."/";
$taskprogressfilepath=$taskfolder."taskprogress.log";
$errorfilepath=$taskfolder."error.log";
//判断目录是否存在
// if(!is_dir($taskfolder)){
    // echo "ok!"
    // header("Location: ./error.php?msg=Invalid Task ID.");
// }
//处理错误
if(file_exists($errorfilepath)){
    $errorfile=fopen($errorfilepath,"r") or die("Unable to open file!");
    $errorcont = fread($errorfile,filesize($errorfilepath));
    fclose($errorfile);
    //gotoerro($errorcont);
    header("Location: ./error.php?msg=".$errorcont);
}
//计算进度
$taskprogress=0;
if(file_exists($taskprogressfilepath)){
    $taskprogressfile = fopen($taskprogressfilepath, "r") or die("Unable to open file!");
    $taskprogresscont = fread($taskprogressfile,filesize($taskprogressfilepath));
    fclose($taskprogressfile);
    $taskprogress = (int)$taskprogresscont;
    switch ($taskprogress){
        case "":
        case 10:
            $info="
            <li>* Received sequence.</li>
            ";
          break;
        case 15:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            ";
          break;
        case 25:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            ";
          break;
        case 30:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            ";
          break;
        case 40:
        $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            <li>* Model related files have been generated.</li>
            ";
          break;
        case 45:
          break;
          $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            <li>* Model related files have been generated.</li>
            ";
        case 50:
          break;
        case 55:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            <li>* Model related files have been generated.</li>
            <li>* Completed feature combination.</li>
            ";
          break;
        case 70:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            <li>* Model related files have been generated.</li>
            <li>* Completed feature combination.</li>
            <li>* HLPI-Ensemble began to predict lncRNA-protein interaction.</li>
            <li>* HLPI-SVM Ensemble completed the prediction work.</li>
            ";
          break;
        case 85:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            <li>* Model related files have been generated.</li>
            <li>* Completed feature combination.</li>
            <li>* HLPI-Ensemble began to predict lncRNA-protein interaction.</li>
            <li>* HLPI-SVM Ensemble completed the prediction work.</li>
            <li>* HLPI-RF Ensemble completed the prediction work.</li>
            ";
          break;
        case 95:
            $info="
            <li>* Received sequence.</li>
            <li>* LncRNA features have been extracted.</li>
            <li>* Protein features have been extracted.</li>
            <li>* Model related files have been generated.</li>
            <li>* Completed feature combination.</li>
            <li>* HLPI-Ensemble began to predict lncRNA-protein interaction.</li>
            <li>* HLPI-SVM Ensemble completed the prediction work.</li>
            <li>* HLPI-RF Ensemble completed the prediction work.</li>
            <li>* HLPI-XGB Ensemble completed the prediction work.</li>
            ";
        case 100:
          //告诉用户即将完成所有计算
          //其实到这里已经完成了所有计算 在下次刷新时就能出结果
          header("Location: ./result.php?taskid=".$taskuuid);
          break;
        default:
    }
}
?>
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
    
    
    <!-- 每20s 自动刷新一次 -->
    <meta http-equiv="refresh" content="20">
    
    
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
        <h2>Total task progress: <?php echo $taskprogress; ?>%</h2>
        <div class="progress" style="background-color:gray;">
            <div class="determinate red accent-4" style="width: <?php echo $taskprogress; ?>%"></div>
        </div>
        <h5>Detailed process</h5>
        <ul><?php echo $info; ?></ul>
        <br><br><br><br><br><br><br><br><br><br><br>
    </div>
    </div>
    <!-- 页脚 -->
    <?php include 'footer.php';?>
</body>
</html>