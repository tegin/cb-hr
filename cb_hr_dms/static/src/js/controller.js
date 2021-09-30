odoo.define("cb_hr_dms.DmsTreeController", function(require) {
    "use strict";

    var DmsTreeController = require("dms.DmsTreeController");
    var HrChat = require("hr.employee_chat");
    HrChat.prototype.config.Controller.include(
        _.extend({}, DmsTreeController.DMSTreeController, {
            custom_events: _.extend(
                {},
                HrChat.prototype.config.Controller.prototype.custom_events,
                DmsTreeController.custom_events
            ),
        })
    );
});
