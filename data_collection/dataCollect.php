<?php
// *******************************
// File 	: dataCollect.php
// Author 	: Kavish N. Dahekar
// Email 	: kavishdahekar@gmail.com
// Details 	: Script for collection and quick annotation of training examples of captchas
// *******************************


// Display errors
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// directory where data will be stored
$dataDir = "data";
// timestamp will be used for uniquely naming files
$timestamp = time();


// check if POST data received
if(!empty($_POST['captchaResponse']) && (ctype_alnum($_POST['captchaResponse']) && strlen($_POST['captchaResponse']) == 5)){
		echo "Saving : ".$_POST['captchaResponse'].".png</br>";

		// if correct respnse received, rename the temporary name to the captcha name
		rename($_POST['oldName'],$dataDir."/".$timestamp."_".strtolower($_POST['captchaResponse']).".png");
		
		// serve next captcha
		echo "Serving next image.</br>";
		$url = "https://webmail.iitg.ernet.in/plugins/captcha/backends/watercap/image_generator.php";
		// store it temporarily
		$img = $dataDir."/tmp_".$timestamp.".png";
		file_put_contents($img, file_get_contents($url));
}else{
	// if expected value not entered
	if(!empty($_POST['oldName'])){
		echo "Please enter correct captcha.</br>";
		$img = $_POST['oldName'];
	}else{
		// serve captcha
		echo "Serving fresh image.</br>";
		$url = "https://webmail.iitg.ernet.in/plugins/captcha/backends/watercap/image_generator.php";
		// store it temporarily
		$img = $dataDir."/tmp_".$timestamp.".png";
		file_put_contents($img, file_get_contents($url));
	}
}

// count data using python script
$command = escapeshellcmd('/home/kavish/anaconda3/envs/pyopencv/bin/python countData.py');

// output will be string containing html table with all counts
$output = shell_exec($command);

?>

<!DOCTYPE html>
<html>
<head>
	<title>Data Collection</title>
	<script type="text/javascript" src="js/jquery-latest.js"></script>
	<script type="text/javascript" src="js/jquery.tablesorter.min.js"></script>
	<!-- <script type="text/javascript" src="js/jquery.tablesorter.js"></script> -->
	<!-- <script type="text/javascript" src="js/jquery.metadata.js"></script> -->
	<style type="text/css">
		table {
		    width: 300px;
		}
		th {
		    height: 10px;
		}
		tr:hover {background-color: #f5f5f5}
		th, td {
		    padding: 2px;
		    text-align: center;
		    border-bottom: 1px solid #ddd;
		}
	</style>
</head>
<body>
<form action="dataCollect.php" method="POST">
	<img src="<?=$img?>"><br>
	<input type="text" name="captchaResponse" autocomplete="off" id="captchaResponse" autofocus>
	<input type="hidden" name="oldName" value="<?=$img?>">
	<input type="submit" value="Press Enter" id="submitButton">
</form>
<div>
	<h3>Data Collected so far</h3>
	<?=$output?>
</div>

<script type="text/javascript">
	// tablesorter for sorting table of alphabets
	$(document).ready(function(){ 
		$("#mtable").tablesorter({
			sortList: [[1,1]]
		});
	}); 
</script>

</body>
</html>