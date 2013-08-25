<?php
$page = $all_pages[0];
?>

<div class="pages">
<?php if ($page->image) { ?>
    <div class="pages image">
        <img src="<?php echo $page->image ?>" />
    </div>
<?php } ?>

<?php if ($page->show_title) { ?>
    <div class="pages title">
        <h1><?php echo $page->title ?></h1>
    </div>
<?php } ?>

<p><?php echo $page->content ?></p>
</div>
