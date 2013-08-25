<div class="inner" id="menu">
    <?php foreach (array_reverse($menu) as $menuitem) { ?>
    <div class="menu-item">
        <a href="<?php echo $menuitem->link ?>">
            <?php echo $menuitem->caption ?>
        </a>
    </div>
    <?php } ?>
</div>
