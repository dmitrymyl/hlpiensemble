<?php
header("Content-type: text/html; charset=utf-8");
function create_uuid($prefix = ""){
    $chars = md5(uniqid(mt_rand(), true));  
    $uuid  = substr($chars,0,8) . '';  
    $uuid .= substr($chars,8,4) . '';  
    $uuid .= substr($chars,12,4) . '';  
    $uuid .= substr($chars,16,4) . '';  
    $uuid .= substr($chars,20,12);  
    return $prefix . $uuid;  
}
// 檢查參數合法性用safe.php封裝
$lncRNAseq=(string)($_POST["lncRNAseq"]);
$proteinseq=(string)($_POST["proteinseq"]);
// 生成任務目錄
$taskuuid=(string)create_uuid();
$taskfolder="task/".$taskuuid."/";
mkdir($taskfolder);
// 寫入lncRNAseq
$lncRNAseqfilepath = $taskfolder."lncRNAseq.fasta";
$lncRNAseqfile = fopen($lncRNAseqfilepath, "w") or die("Unable to open file!");
$cont = $lncRNAseq;
fwrite($lncRNAseqfile, $cont);
fclose($lncRNAseqfile);
// 寫入proteinseq
$proteinseqfilepath = $taskfolder."proteinseq.fasta";
$proteinseqfile = fopen($proteinseqfilepath, "w") or die("Unable to open file!");
$cont = $proteinseq;
fwrite($proteinseqfile, $cont);
fclose($proteinseqfile);
// 生成特征
// 檢查文件是否存在
if (!(file_exists($lncRNAseqfilepath) and file_exists($proteinseqfilepath))){
    header("Location: ./error.php?msg=Your upload sequence is incorrect Please check and re-upload");
}
//將所有過程 濃縮到一個python文件里
//exec("python /var/www/html/hlpiensemble/pse/kmer.py /var/www/html/hlpiensemble/".$taskfolder."lncRNAseq.fasta /var/www/html/hlpiensemble/".$taskfolder."lncRNAFeature_kmer.csv RNA -k 2 -f csv&");
//exec("python /var/www/html/hlpiensemble/pse/acc.py /var/www/html/hlpiensemble/".$taskfolder."lncRNAseq.fasta /var/www/html/hlpiensemble/".$taskfolder."lncRNAFeature_DAC.csv RNA DAC -lag 2 -all_index -f csv&");
//exec("python /var/www/html/hlpiensemble/pse/pse.py /var/www/html/hlpiensemble/".$taskfolder."lncRNAseq.fasta /var/www/html/hlpiensemble/".$taskfolder."lncRNAFeature_PC-PseDNC-General.csv RNA PC-PseDNC-General -all_index -f csv&");
try{
    exec("python Serverprediction.py ".$taskuuid." >/dev/null &");
}catch(Exception $e){
    echo $e;
}
header("Location: ./result_process.php?taskid=".$taskuuid); 
?>