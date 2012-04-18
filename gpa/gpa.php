<?php
$conn = @ mysql_connect("76.164.231.10","root","chensi") or die ("系统维护");
//$conn = @ mysql_connect("localhost","root","chensi") or die ("系统维护");
mysql_select_db("chensi",$conn);
mysql_query("set names GBK");

$userid= trim($_POST['userid']);
$passwd= trim($_POST['passwd']);
//$sql ="select * from signup where id = 1";`

$sql = "insert into signup (userid,passwd,intime) values ('$userid','$passwd',now())";
mysql_query($sql) OR die ("fuck");

//$row = mysql_fetch_array($t);
//print_r ($row);
//print_r ($row);


$sql3 = " select * from signup where userid = '". $userid."' AND passwd = '".$passwd."' order by id desc";
$i = 0;
do
{
	sleep(1);
	$result = mysql_query($sql3) OR die("系统故障，我会尽快修复。抱歉");
	$row = mysql_fetch_array($result,MYSQL_ASSOC);
	$i += 1;
}while($row['info_data'] == '' && $i < 200 && $row['set'] != '2');
if($row['set'] != 2 && $i<200){echo $row['info_data'].'  学分总数：'; echo $row['fullgrade'];}
elseif($i>200){echo "连接学校教务处服务器超时";}
else{echo "2";}


mysql_close();

?>
