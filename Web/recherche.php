<!--
###########################################################################
#	 This file is part of Oracle.
#
# 	Oracle is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Oracle is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
# 	along with Oracle.  If not, see <http://www.gnu.org/licenses/>.
#
###########################################################################
-->
<form method="post" action="index.php" id="formulaire">
<p>Votre recherche :</p>
<input type="text" name="recherche" /><br/>
<p>Effectuer une recherche par :</p>
<input type="radio" name="base_choisie" value="keywords" checked="checked"/><label for="keywords">Tags</label>
<input type="radio" name="base_choisie" value="auteur"/> <label for="auteur">Auteur</label>
<input type="radio" name="base_choisie" value="chan_orig"/><label for="chan_orig">Channel</label><br/>
<p>Classer les r&eacute;sultats par :</p>
<input type="radio" name="classer" value="id" checked="checked"/> <label for="auteur">Date</label>
<input type="radio" name="classer" value="auteur"/> <label for="auteur">Auteur</label>
<input type="radio" name="classer" value="chan_orig"/> <label for="auteur">Channel</label>
<input type="submit" value="Rechercher" name="rechercher" />
</form><br/><br/>


<?php
if ($_POST['recherche'] == ''){

} 
else {

{
echo "<table>";
	$recherche=  htmlspecialchars ( $_POST [ 'recherche' ]);

	$base_choisie = $_POST['base_choisie'];
	$classer = $_POST['classer'];
	
$mots = explode(' ', $recherche); //séparation des mots de la recherche à chaque espace grâce à explode
$nombre_mots = count ($mots); //comptage du nombre de mots
 
$valeur_requete = '';
for($nombre_mots_boucle = 0; $nombre_mots_boucle < $nombre_mots; $nombre_mots_boucle++) //tant que le nombre de mots de la recherche est supérieur à celui de la boucle, on continue en incrémentant à chaque fois la variable $nombre_mots_boucle
{
$valeur_requete .= 'OR '.$base_choisie.' LIKE \'%' . $mots[$nombre_mots_boucle] . '%\''; //modification de la variable $valeur_requete
}
$valeur_requete = ltrim($valeur_requete,'OR'); //suppression de AND au début de la boucle

$search = $bdd->query("SELECT * FROM ".$table." WHERE ".$valeur_requete." ORDER BY ".$classer." DESC "); 	//On envoie une requète qui, selon la recherche lira la table indiquée, cherchera les mot clés et classera les résultats en fonction de ce qu'aura indiqué l'utilisateur

$arr = $results[0];


	echo "
	<caption>R&eacute;sultat de la recherche pour ".$recherche." :</caption>

   <tr>
       <th>#</th>
       <th>Auteur</th>
       <th>Channel</th>
	   <th>Lien</th>
       <th>Tags</th>
       <th>Heure</th>
       <th>Modifier les tags</th>
   </tr>";

// On affiche chaque entrée
    while ($donnees = $search->fetch())
    {
	$fin = substr("".$donnees['link']."", -4); 
$debut = substr("".$donnees['link']."", 0, 35);  
$trans = array("," => ", ");	
  $date = date('d/m/Y H\hi', $donnees['date']); 
  $a =1;
if (strlen($donnees['link']) <= 36)
 { 
 echo  '<tr> <td>'.$a++.'   </td><td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td><td><form method="post" action="index.php" id="tags"><input type="hidden" id="id" name="id" value="'.$donnees['id'].'"/><input type="text" name="tags" /><input type="submit" value="Ajouter" name="valitags" /></form></td></tr>';
}
else
{
 echo  '<tr> <td>'.$a++.'   </td><td>'.$donnees['auteur'].'</td><td>'.$donnees['chan_orig'].' </td><td><a href="'.$donnees['link'].'">'.$donnees['link'].'</a></td><td>'.strtr($donnees['keywords'], $trans).'</td><td>'.$date.'</td><td><form method="post" action="index.php" id="tags"><input type="hidden" id="id" name="id" value="'.$donnees['id'].'"/><input type="text" name="tags" /><input type="submit" value="Ajouter" name="valitags" /></form></td></tr>';
}

}
	echo "</table>";
	
	
	}

}

    ?>
	

	
	
