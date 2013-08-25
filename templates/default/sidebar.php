<div class="inner" id="sidebar">
    <ul>
    <?php foreach ($sidebar as $sidebaritem) { ?>
    <li>
        <a href="<?php echo $sidebaritem->link ?>">
            <?php echo $sidebaritem->caption ?>
        </a>
        <?php if ($sidebaritem->submenu) { ?>
            <ul>
            <?php foreach ($sidebaritem->submenu as $subitem) { ?>
                <li>
                    <a href="<?php echo $subitem->link ?>">
                        <?php echo $subitem->caption ?>
                    </a>
                </li>
            <?php } ?>
            </ul>
        <?php } elseif ($sidebaritem->list) { ?>
            <ul>
            <?php foreach ($content_lists[$sidebaritem->list] as $subitem) { ?>
                <li>
                    <a href="<?php echo $content_links[$sidebaritem->list . '/' . $subitem->name] ?>">
                        <?php echo $subitem->title ?>
                    </a>
                </li>
            <?php } ?>
            </ul>
        <?php } ?>
    </li>
    <?php } ?>
    </ul>
</div>
