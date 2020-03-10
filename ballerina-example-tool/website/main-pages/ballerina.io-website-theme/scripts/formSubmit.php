<?php

$url = isset($_POST['url']) ? strip_tags($_POST['url']) : "";
$url = str_replace("#","%23",$url);

// open connection
$ch = curl_init();

// set the url, number of POST vars, POST data
curl_setopt($ch,CURLOPT_URL,$url);
curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);

// exec
$replyRaw = curl_exec($ch);
$reply = json_decode($replyRaw, true);

echo $reply;

// close connection
curl_close($ch);

?>
