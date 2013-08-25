<?php
class pages {
    public $name;
    public $title;
    public $time;
    public $content;
    public $image;
    public $show_title;
    public function __construct ($name, $title, $time, $content, $image = null, $show_title = true) {
        $this->name = $name;
        $this->title = $title;
        $this->time = $time;
        $this->content = $content;
        $this->image = $image;
        $this->show_title = $show_title;
    }
}

$all_pages = array();

if (!isset($content_lists))
    $content_lists = array();
$content_lists['pages'] = &$all_pages;
?>
