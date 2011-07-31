<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" >
   <head>
       <title>Oracle - interface de recherche</title>
       <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	   <link rel="stylesheet" media="screen" type="text/css" title="Design" href="css.css" />
   </head>
   <body>
   <div id="titre"><h1> Oracle : Interface de recherche</h1></div>
   <div id="corps">
   <div id="float"><h2> Oracle Recherche, Accepte et Consulte les Liens Etonnants</h2><br/> </div>
  
<?php
$base= 'Oracle.sq3';					//Nom du fichier sq3
$table = 'oracle';						//Nom de la table
// On se connecte à SQLite
$pdo_options[PDO::ATTR_ERRMODE] = PDO::ERRMODE_EXCEPTION;    
$bdd = new PDO("sqlite:".$base."");																
// On récupère tout le contenu de la table  !
   
include('recherche.php');
   
echo'<table>
   <caption>Index des liens<form method="post" action="index.php" id="classement">
   <span>Classer par :</span>
<input type="radio" name="classer" value="id" checked="checked"/> <label for="auteur">Date</label>
<input type="radio" name="classer" value="auteur"/> <label for="auteur">Auteur</label>
<input type="radio" name="classer" value="chan_orig"/> <label for="auteur">Channel</label>
<input type="submit" value="Classer" name="classement" />
</form></caption>

   <tr>
       <th>#    </th>
       <th>Auteur</th>
       <th>Channel</th>
	   <th>Lien</th>
       <th>Tags</th>
       <th>Heure</th>
       <th>Modifier les tags</th>
   </tr>';

$a = 1;

// Ajout de tags

if (isset($_POST['tags']) AND isset($_POST['id']))
{
	$reponse = $bdd->query("SELECT keywords FROM '".$table."' WHERE id='".$_POST['id']."'");
	$donnees = $reponse->fetch();
	$trans2 = array(" " => ","); //on emplace les espaces par des virgules
	$bdd->exec("UPDATE ".$table." SET keywords='".$donnees['keywords'].strtr($_POST['tags'], $trans2).",' WHERE id='".$_POST['id']."'");
}	

// Affichage du tableau
	    
if ($_POST['classement'] == '')					// On affiche chaque entrée
{
	$reponse = $bdd->query("SELECT * FROM '".$table."' ORDER BY id DESC LIMIT 0,100");
	while ($donnees = $reponse->fetch())
    {
		$id = $donnees['id'];
		$date = date('d/m/Y H\hi', $donnees['date']);			//formatage de la date
		$trans = array("," => ", ");											//Mise en place d'espaces entre chaque tags

		if (strlen($donnees['link']) <= 36)								//Si le lien n'est pas trop long (si il fait moins de x caractères)
		{ 
			$link = $donnees['link'];
			echo '<tr> <td>'.$a++.'   </td><td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td><td><form method="post" action="index.php" id="tags"><input type="hidden" id="id" name="id" value="'.$donnees['id'].'"/><input type="text" name="tags" /><input type="submit" value="Ajouter" name="valitags" /></form></td></tr>';
		}
		else																			//Si le lien est trop long (plus de x caractères)
		{
			$link = $donnees['link'];
			$fin = substr("".$donnees['link']."", -4); 						//On garde les 4 derniers caractères.
			$debut = substr("".$donnees['link']."", 0, 35);  				//On conserve les 35 premiers
			echo  '<tr> <td>'.$a++.'   </td><td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$debut.'...'.$fin.'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td><td><form method="post" action="index.php" id="tags"><input type="text" name="tags" /><input type="hidden" id="id" name="id" value="'.$donnees['id'].'"/><input type="submit" value="Ajouter" name="valitags" /></form></td></tr>';
		}
   }
	echo "</table>";
	$reponse->closeCursor(); // Fin du traitement
}
else
{
	$classement = $_POST['classer'];
	$reponse = $bdd->query("SELECT * FROM '".$table."' ORDER BY ".$classement." DESC LIMIT 0,100");
	while ($donnees = $reponse->fetch())
    {
		$date = date('d/m/Y H\hi', $donnees['date']);			//formatage de la date
		$trans = array("," => ", ");											//Mise en place d'espaces entre chaque tags
		if (strlen($donnees['link']) <= 36)								//Si le lien n'est pas trop long (si il fait moins de x caractères)
		{ 
			$link = $donnees['link'];
			echo  '<tr> <td>'.$a++.'   </td><td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td><td><form method="post" action="index.php" id="tags"><input type="text" name="tags"/><input type="hidden" id="id" name="id" value="'.$donnees['id'].'"/><input type="submit" value="Ajouter" name="valitags" /></form></td></tr>';
		}
		else																			//Si le lien est trop long (plus de x caractères)
		{
			$fin = substr("".$donnees['link']."", -4); 						//On garde les 4 derniers caractères.
			$debut = substr("".$donnees['link']."", 0, 35);  				//On conserve les 35 premiers
			echo  '<tr>  <td>'.$a++.'  </td><td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$debut.'...'.$fin.'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td><td><form method="post" action="index.php" id="tags"><input type="text" name="tags"/><input type="hidden" id="id" name="id" value="'.$donnees['id'].'"/><input type="submit" value="Ajouter" name="valitags" /></form></td></tr>';
		}
	}
	echo "</table>";
	$reponse->closeCursor(); // Fin du traitement
}
?>

</div><br/>
<div id="footer"><p>Oracle web interface <a href="http://hgpub.druil.net/Oracle/">http://hgpub.druil.net/Oracle/</a></p></div>
</body>
</html>
