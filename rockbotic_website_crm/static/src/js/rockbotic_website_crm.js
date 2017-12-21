(function () {
    'use strict';
    var instance = openerp;
    var website = openerp.website;
    var _t = openerp._t;

    website.ready().done(function () {

        $('.oe_student_signup').each(function () {
            var oe_student_signup = this;

            $(oe_student_signup).on('change', "select[name='school_id']", function() {
                var $event_id = $("select[name='event_id']");
                $event_id.find("option:not(:first)").addClass('hidden');
                $event_id.find("option[data-school_id="+($(this).val() || 0) +"]").removeClass('hidden');
            });
            $(oe_student_signup).find("select[name='school_id']").change();

        });
    });
} ());
