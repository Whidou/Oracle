<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" >
   <head>
       <title>Oracle - interface de recherche</title>
       <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<style type="text/css">
table
{
   border-collapse: collapse;
}
td, th
{
   border: 1px solid black;
   padding: 10px;
}
       </style>
   
   </head>
   <body>
<?php
try
{

	$base= 'oracle.sq3';					//Nom du fichier sq3
	$table = 'oracle';						//Nom de la table
	
	// On se connecte à SQLite

    $pdo_options[PDO::ATTR_ERRMODE] = PDO::ERRMODE_EXCEPTION;    
    $bdd = new PDO("sqlite:".$base."");																
    $query = 'SELECT * FROM oracle ORDER BY id';
    // On récupère tout le contenu de la table 
    $reponse = $bdd->query("SELECT * FROM '".$table."' ORDER BY id"); 								
    ?>
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
    ?>
       <tr> 
     <th><?php echo $donnees['auteur']; ?></th>
     <th><?php echo $donnees['chan_orig']; ?> </th>
	 <th><a href="<?php echo $donnees['link']; ?>"><?php echo $donnees['link']; ?></a></th>
	 <th><?php echo $donnees['keywords']; ?></th>
	 <th><?php echo date('d/m/Y H\hi', $donnees['date']); ?></th>
	 </tr>

	 
    <?php
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


?>

</body>
</html>
