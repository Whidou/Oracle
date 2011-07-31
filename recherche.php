<form method="post" action="index.php">
Votre recherche :
<input type="text" name="recherche" /><br/>
Effectuer une recherche par :
<input type="radio" name="base_choisie" value="keywords" checked="checked"><label for="keywords">Tags</label>
<input type="radio" name="base_choisie" value="auteur"> <label for="auteur">Auteur</label>
<input type="radio" name="base_choisie" value="chan_orig"><label for="chan_orig">Chan</label>
<input type="submit" value="Rechercher" name="rechercher" />
</form><br/><br/>
<?php
	if (isset($_POST['rechercher'])) //si on a validé le formulaire
{
	$recherche=  htmlspecialchars ( $_POST [ 'recherche' ]);

	$base_choisie = $_POST['base_choisie'];
	
$mots = explode(' ', $recherche); //séparation des mots de la recherche à chaque espace grâce à explode
$nombre_mots = count ($mots); //comptage du nombre de mots
 
$valeur_requete = '';
for($nombre_mots_boucle = 0; $nombre_mots_boucle < $nombre_mots; $nombre_mots_boucle++) //tant que le nombre de mots de la recherche est supérieur à celui de la boucle, on continue en incrémentant à chaque fois la variable $nombre_mots_boucle
{
$valeur_requete .= 'OR '.$base_choisie.' LIKE \'%' . $mots[$nombre_mots_boucle] . '%\''; //modification de la variable $valeur_requete
}
$valeur_requete = ltrim($valeur_requete,'OR'); //suppression de AND au début de la boucle

$search = $bdd->query("SELECT * FROM ".$table." WHERE ".$valeur_requete.""); 		

$arr = $results[0];



echo "Vous avez recherché ".$recherche."<br><br>\n";


	echo "<table>
   <caption>Index des liens</caption>

   <tr>
       <th>Pseudo</th>
       <th>Channel</th>
	   <th>Lien</th>
       <th>Tags</th>
       <th>Heure</th>
   </tr>";

// On affiche chaque entrée
    while ($donnees = $search->fetch())
    {
      $date = date('d/m/Y H\hi', $donnees['date']); 
 echo  '<tr> <th>'.$donnees['auteur'].'</th><th>'.$donnees['chan_orig'].' </th><th><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></th><th>'.$donnees['keywords'].'</th><th>'.$date.'</th></tr>';
    }
	
	}
	else {
	}
echo "</table>";
    ?>
	
	