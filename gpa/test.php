<?php
$conn = @ mysql_connect("localhost","root","chensi") or die ("errror");
mysql_select_db("chensi",$conn);
mysql_query("set names GBK");



//$sql ="select * from signup where id = 1";

$sql = "insert into signup (userid,passwd,intime) values ('$_POST[userid]','$_POST[passwd]',now())";
mysql_query($sql) OR die ("fuck");

//$row = mysql_fetch_array($t);
//print_r ($row);
//print_r ($row);
mysql_close();
echo "OK check your E-mail:)";
echo "<meta. http-equiv=refresh content='0; url=index.html'>";
?>
