<?php
// Configuration
include('config.php');

// Connexion à la BDD
$pdo_options[PDO::ATTR_ERRMODE] = PDO::ERRMODE_EXCEPTION;
$bdd = new PDO("sqlite:".$base);

// Ajout de tags
if (isset($_POST['tags']) AND isset($_POST['id']))
{
	$tags = sqlite_escape_string(htmlspecialchars($_POST['tags']));
	$id = sqlite_escape_string(htmlspecialchars($_POST['id']));
	
	$reponse = $bdd->query("SELECT keywords FROM ".$table." WHERE id='".$id."'");
	$donnees = $reponse->fetch();

	$bdd->exec("UPDATE ".$table." SET keywords='".$donnees['keywords'].strtr($tags,  array(" " => ",")).",' WHERE id='".$id."'");
} ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" >
<head>
	<title>Oracle - interface de recherche</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link rel="stylesheet" media="screen" type="text/css" title="Oracle" href="css.css" />
</head>
<body>
	<div id="corps">
		<div id="float">
			<h2> Oracle Recherche, Accepte et Consulte les Liens Etonnants</h2>
		</div>
		<form method="post" action="index.php" id="formulaire">
			<p>Recherche :</p>
			<input type="text" name="recherche" /><br/>
			<p>Type :</p>
			<input type="radio" name="champ" value="keywords" id="r_tags" checked="checked" /><label for="r_tags">Tags</label>
			<input type="radio" name="champ" value="auteur" id="r_auteur" /> <label for="r_auteur">Auteur</label>
			<input type="radio" name="champ" value="chan_orig" id="r_chan" /><label for="r_chan">Channel</label><br/>
		</form>
		<form method="post" action="index.php" id="classement">
			<span>Classer par :</span>
			<input type="radio" name="classer" value="id" id="date" /> <label for="date">Date</label>
			<input type="radio" name="classer" value="auteur" id="auteur" /> <label for="auteur">Auteur</label>
			<input type="radio" name="classer" value="chan_orig" id="chan" /> <label for="chan">Salon</label>
			<input type="submit" value="Classer" />
		</form>
		<table>
			<caption>Index des liens</caption>
			<tr>
				<th>#</th>
				<th>Auteur</th>
				<th>Salon</th>
				<th>Lien</th>
				<th>Tags</th>
				<th>Heure</th>
				<th>Modifier les tags</th>
			</tr>
<?php
//Recherche
if (isset($_POST['recherche']))
{
	$recherche=  sqlite_escape_string(htmlspecialchars($_POST['recherche']));
	$champ = sqlite_escape_string(htmlspecialchars($_POST['champ']));
	$search = " WHERE ".$champ." LIKE '%".strtr($recherche,  array(" " => "OR ".$champ." LIKE '%"))."%'";
}
else
{
	$search = "";
}

// Classement
if (isset($_POST['classer']))
{
	$classement = sqlite_escape_string(htmlspecialchars($_POST['classer']));
}
else
{
	$classement = 'id';
}

//Requête
$reponse = $bdd->query("SELECT * FROM '".$table."'".$search." ORDER BY ".$classement." DESC LIMIT 0, ".$lines);

// Affichage
while ($donnees = $reponse->fetch())
{
	if (strlen($donnees['link']) <= $max_link_length)	// Si le lien n'est pas trop long
	{ 
		$link = $donnees['link'];
	}
	else												// Si le lien est trop long
	{
		$fin = substr($donnees['link'], -4); 						// Les 4 derniers
		$debut = substr($donnees['link'], 0, $max_link_length-7);	// Les n-7 premiers
		$link = $debut.'...'.$fin;
	}
	echo '
			<tr>
				<td>'.$donnees['id'].'</td>
				<td>'.$donnees['auteur'].'</td>
				<td>'.$donnees['chan_orig'].' </td>
				<td><a href="'.$donnees['link'].'">'.$link.'</a></td>
				<td>'.strtr($donnees['keywords'], array("," => ", ")).'</td>
				<td>'.date('d/m/Y H\hi', $donnees['date']).'</td>
				<td>
					<form method="post" action="index.php">
						<input type="hidden" name="id" value="'.$donnees['id'].'" />
						<input type="text" name="tags" />
						<input type="submit" value="Ajouter"/>
					</form>
				</td>
			</tr>';
}
$reponse->closeCursor(); ?>
		</table>
	</div>
	<div id="footer">
		<p>Oracle HTTP Interface <a href="http://hgpub.druil.net/Oracle/">http://hgpub.druil.net/Oracle/</a></p>
	</div>
</body>
</html>
