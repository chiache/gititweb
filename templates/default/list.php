<?php foreach ($content_lists as $type => $contents) { ?>
    <div class="content-list">
    <h1>All published <?php echo $type ?></h1>
    <ul>
    <?php foreach ($contents as $content) { ?>
        <li>
            <a href="<?php echo $content_links[$type . '/' . $content->name] ?>">
                <?php echo $content->title ?>
            </a>
    </li>
    <?php } ?>
    </ul>
    </div>
<?php } ?>
