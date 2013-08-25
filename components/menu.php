<?php
class menu_item {
    public $caption;
    public $link;
    public function __construct($caption, $link) {
        $this->caption = $caption;
        $this->link = $link;
    }
}

$menu = array();
?>
