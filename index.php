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


	$base= '~/Oracle/Oracle.sq3';					//Nom du fichier sq3
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
      $date = date('d/m/Y H\hi', $donnees['date']);			//formatage de la date
$trans = array("," => ", ");											//Mise en place d'espaces entre chaque tags


if (strlen($donnees['link']) <= 35)								//Si le lien n'est pas trop long (si il fait moins de x caractères)
 { 
 echo  '<tr> <td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td></tr>';
}
else																			//Si le lien est trop long (plus de x caractères)
{
$fin = substr("".$donnees['link']."", -4); 						//On garde les 4 derniers caractères.
$debut = substr("".$donnees['link']."", 0, 35);  				//On conserve les 35 premiers
 echo  '<tr> <td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$debut.'...'.$fin.'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td></tr>';
}
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
