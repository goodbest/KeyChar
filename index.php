<?php
function datecmp($a, $b){
	$a= date_create($a['startDate']);
	$b= date_create($b['startDate']);
	if($a==$b)
		return 0;
	return ($a<$b)?-1:1;
}

function getTodayCard(){
	$string = file_get_contents("key_figure.json");
	$json_a = json_decode($string, true);
	$slide_data = $json_a['timeline']['date'];

	#remove none birthday slide, which has fake birth year 2001
	foreach ($slide_data as $key => $val){
		$dates = explode(",", $slide_data[$key]['startDate'], 3);
		if($dates[0]=="2001"){
			unset($slide_data[$key]);
		}
		else{
			$slide_data[$key]['startDate']= str_replace(",", "-", $slide_data[$key]['startDate']);
		}
	}

	usort($slide_data, 'datecmp');
	$cur_date['startDate'] = strftime("2000-%m-%d");

	foreach ($slide_data as $key=> $value){
		if(datecmp($value, $cur_date)>=0){
			return $key+1;
			break;
		}
	}
	return 0;
}
?>
<!DOCTYPE html>
<html lang="jp"><!--
  	 
  	88888888888 d8b                        888 d8b                888888   d8888b  
  	    888     Y8P                        888 Y8P                   88b d88P  Y88b 
  	    888                                888                       888 Y88b
  	    888     888 88888b d88b     d88b   888 888 88888b     d88b   888   Y888b
  	    888     888 888  888  88b d8P  Y8b 888 888 888  88b d8P  Y8b 888      Y88b
  	    888     888 888  888  888 88888888 888 888 888  888 88888888 888        888 
  	    888     888 888  888  888 Y8b      888 888 888  888 Y8b      88P Y88b  d88P 
  	    888     888 888  888  888   Y8888  888 888 888  888   Y8888  888   Y8888P
  	                                                                d88P            
  	                                                              d88P             
  	                                                            888P              
  	 -->
  <head>
    <title>Key Charactor Birthday Timeline</title>
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">    
    <meta name="description" content="The human computer interface helps to define computing at any one time.">
    <meta charset="utf-8">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-touch-fullscreen" content="yes">
    <!-- Style-->
    <style>
      html, body {
      height:100%;
      padding: 0px;
      margin: 0px;
      }
    </style>
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/storyjs-embed.js"></script>
    <script>
                $(document).ready(function() {
                    createStoryJS({
                        width: "100%",
                        height: "100%",
                        source: 'key_figure.json',
                        font:	'BreeSerif-OpenSans',
                        hash_bookmark:  true,
                        lang:    'zh-cnm',
                        start_at_slide: '<?php echo getTodayCard();?>',
                        debug:   false,
                        embed_id:   'keyfigure-timeline'
                    });
                });
    </script>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <!-- Optional theme -->
    <link rel="stylesheet" href="css/bootstrap-theme.min.css">
    <!-- Latest compiled and minified JavaScript -->
    <script src="js/bootstrap.min.js"></script>
    <!-- HTML5 shim, for IE6-8 support of HTML elements--><!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
  </head>
  <body>
    <!-- BEGIN Timeline Embed -->
    <div id="keyfigure-timeline"></div>

    <!-- END Timeline Embed-->
    <!-- Analytics-->
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-51644149-6', 'auto');
      ga('send', 'pageview');

    </script>
  </body>
</html>
