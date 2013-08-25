<?php
class sidebar_item {
    public $caption;
    public $link;
    public $submenu = array();
    public $list;
    public function __construct($caption, $link, $list = null) {
        $this->caption = $caption;
        $this->link = $link;
        $this->list = $list;
    }
}

$sidebar = array();
?>
