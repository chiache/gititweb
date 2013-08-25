<html>

<head>
    <title><?php echo PAGE_TITLE ?> | <?php echo WEBSITE_NAME ?></title>
    <?php if (defined('CSS_URL')) { ?>
      <link rel="StyleSheet" href="<?php echo CSS_URL ?>" type="text/css">
    <?php } ?>
    <?php if (defined('FAVICON_URL') && defined('FAVICON_TYPE')) { ?>
      <link rel="Shortcut Icon" href="<?php echo FAVICON_URL ?>" type="image/<?php echo FAVICON_TYPE ?>">
    <?php } ?>
</head>

<body>
    <div class="outer">
        <div class="inner" id="title">
            <a href="<?php echo URLROOT . '/index.html' ?>">
                <?php echo WEBSITE_TITLE ?>
            </a>
        </div>
        <?php echo MENU ?>
        <div class="left-block">
            <?php echo SIDEBAR ?>
        </div>
        <div class="right-block">
