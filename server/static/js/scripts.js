/**
 * Sprintf like function
 * @source http://stackoverflow.com/a/4795914/805649
 * @return String
 */
String.prototype.format = function() {
    "use strict";

    var formatted = this;
    for (var prop in arguments[0]) {
        if (arguments[0].hasOwnProperty(prop)) {
            var regexp = new RegExp("\\{" + prop + "\\}", "gi");
            formatted = formatted.replace(regexp, arguments[0][prop]);
        }
    }
    return formatted;
};

format_datetime = function(utc_date_string) {
    return moment.utc(utc_date_string).local().format("YYYY-MM-DD HH:mm:ss");
};

format_ms_duration = function(duration) {
    var milliseconds = parseInt((duration%1000)/100, 10);
    var seconds = parseInt((duration/1000)%60, 10);
    var minutes = parseInt((duration/(1000*60))%60, 10);
    var hours = parseInt((duration/(1000*60*60))%24, 10);
    var days = parseInt((duration/(1000*60*60*24)), 10);

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;

    if(days > 0) {
        return days + "d " + hours + "h " + minutes + "m";
    }

    if(hours > 0) {
        return hours + "h " + minutes + "m " + seconds + "s";
    }

    return minutes + "m " + seconds + "." + milliseconds + "s";
};

is_in_range = function(utc_date_string, range_seconds) {
    return moment.utc(utc_date_string).local() > moment().add(-1 * range_seconds, 'seconds');
};

API = my.Class(pinocchio.Service, {
    constructor: function(base_url) {
        API.Super.call(this, base_url, new pinocchio.security.PassiveSecurity() );
    },

    _general_failure: function(a,b,c) {
        toastr.error("API failure");
    },

    set_option: function(key, value, callback) {
        this.post("/option", "", JSON.stringify({"key": key, "value": value}), callback, this._general_failure);
    },
    get_options: function(callback) {
        this.get("/option", "", callback, this._general_failure);
    },

    set_color: function(uri, hex_colors, callback) {
        callback = callback || function() {
            console.log("color set");
        };
        this.post(uri, "", JSON.stringify({
            "pixels": hex_colors
        }), callback, this._general_failure);
    },
    set_color_inner: function(hex_colors, callback) {
        this.set_color("/presentation/inner", hex_colors, callback);
    },
    set_color_outer: function(hex_colors, callback) {
        this.set_color("/presentation/outer", hex_colors, callback);
    },




    get_beacons: function(callback) {
        this.get("/beacon", "", callback, this._general_failure);
    },
    get_detectors: function(callback) {
        this.get("/detector", "", callback, this._general_failure);
    },
    get_agents: function(callback) {
        this.get("/agent", "", callback, this._general_failure);
    },

    create_training_entry: function(beacon_uuid, expectation, callback) {
        this.post("/training", "", JSON.stringify({"beacon_uuid": beacon_uuid, "expectation": expectation}), callback, this._general_failure);
    },

    set_beacon_checked: function(beacon_uuid, checked_flag, callback) {
        this.post("/beacon", "", JSON.stringify({
            "uuid": beacon_uuid,
            "is_accepted": checked_flag ? 1: 0
        }), callback, this._general_failure);
    },
    set_beacon_metadata: function(beacon_uuid, metadata, callback) {
        this.post("/beacon", "", JSON.stringify({
            "uuid": beacon_uuid,
            "metadata": metadata
        }), callback, this._general_failure);
    }
});


SequenceManager = my.Class({
    constructor: function(api) {
        this.api = api;
        this.init();
    },
    init: function() {

    }
});

SolidColorManager = my.Class({
    constructor: function(api) {
        this.api = api;
        this.init();
    },
    init: function() {

    }
});

OmbreColorManager = my.Class({
    constructor: function(api) {
        this.api = api;
        this.init();
    },
    init: function() {
        var self = this;
        $(".btn.btn-ombre").click(function() {
            self.set_colors(
                [ $(".outer-color-solid-lower").val(), $(".outer-color-solid-upper").val() ],
                [ $(".inner-color-solid-lower").val(), $(".inner-color-solid-upper").val() ]
            );
        });

        $(".btn.btn-solid").click(function() {
            self.set_colors(
                [ $(".outer-color-solid").val() ],
                [ $(".inner-color-solid").val() ]
            );
        });
    },
    set_colors: function(inner_colors, outer_colors) {
        this.api.set_color_inner(inner_colors);
        this.api.set_color_outer(outer_colors);
    }
});



environment = { };

$(function(){
    environment.service = new API("./api");
    environment.sequences = new SequenceManager( environment.service );
    environment.solids = new SolidColorManager( environment.service );
    environment.ombre = new OmbreColorManager( environment.service );
});


