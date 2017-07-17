$(document).ready(function () {

$('.oe_student_signup').each(function () {
    var oe_student_signup = this;

    $(oe_student_signup).on('change', "select[name='country_id']", function () {
        var $select = $("select[name='state_id']");
        $select.find("option:not(:first)").hide();
        var nb = $select.find("option[data-country_id="+($(this).val() || 0)+"]").show().size();
        $select.parent().toggle(nb>0);
    });
    $(oe_student_signup).find("select[name='country_id']").change();

    $(oe_student_signup).on('change', "select[name='school_id']", function () {
        var $select = $("select[name='event_id']");
        $select.find("option:not(:first)").hide();
        var nb = $select.find("option[data-school_id="+($(this).val() || 0)+"]").show().size();
        $select.parent().toggle(nb>0);
    });
    $(oe_student_signup).find("select[name='school_id']").change();
});
});
