// $('[data-toggle="popover"]').popover({trigger: "hover", container: 'body'}); 
$('.might-overflow').on('mouseenter', function(){
    var $this = $(this);
    var $leftPanel = $("#left-panel");
    if($this.width() > $leftPanel.width()) {
        $this.popover({trigger: "manual", container: 'body'});
        $this.popover("show");
    }
});

$('.might-overflow').on("mouseleave", function() {
    $(this).popover("hide");
});