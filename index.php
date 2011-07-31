<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" >
   <head>
       <title>Oracle - interface de recherche</title>
       <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	   <link rel="stylesheet" media="screen" type="text/css" title="Design" href="css.css" />
   </head>
   <body>
   <center>
   <h3> Oracle : Interface de recherche</h3>
   <div id="corps">
<?php
try
{

	$base= '~/.Oracle/Oracle.sq3';					//Nom du fichier sq3
	$table = 'oracle';						//Nom de la table
	// On se connecte à SQLite

    $pdo_options[PDO::ATTR_ERRMODE] = PDO::ERRMODE_EXCEPTION;    
    $bdd = new PDO("sqlite:".$base."");																
    // On récupère tout le contenu de la table  !
    $reponse = $bdd->query("SELECT * FROM '".$table."' ORDER BY id"); 								

   ?>
   
   <?php include('recherche.php'); ?>
	<table>
   <caption>Index des liens</caption>

   <tr>
       <th>Pseudo</th>
       <th>Channel</th>
	   <th>Lien</th>
       <th>Tags</th>
       <th>Heure</th>
   </tr>
    <?php 



	// On affiche chaque entrée
    while ($donnees = $reponse->fetch())
    {
      $date = date('d/m/Y H\hi', $donnees['date']);
$trans = array("," => ", ");

 echo  '<tr> <th>'.$donnees['auteur'].'</th><th>'.$donnees['chan_orig'].' </th><th><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></th><th>'.strtr($donnees['keywords'], $trans).' </th><th>'.$date.'</th></tr>';
    }
    ?>
	
	</table>
    
	<?php
	$reponse->closeCursor(); // Fin du traitement

}
catch(Exception $e)
{
    // En cas d'erreur, on affiche un message
    die('Erreur : '.$e->getMessage());
}


?></div><br/>
<div id="footer"><p>Oracle web interface <a href="http://hgpub.druil.net/Oracle/">http://hgpub.druil.net/Oracle/</a></div>
</center>
</body>
</html>
