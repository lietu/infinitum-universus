define(["moment"], function (moment) {
    var Utils = Object.create({});


    Utils.LIGHT_SECOND = 1;
    Utils.LIGHT_MINUTE = 60 * Utils.LIGHT_SECOND;
    Utils.LIGHT_HOUR = 60 * Utils.LIGHT_MINUTE;
    Utils.LIGHT_DAY = 24 * Utils.LIGHT_HOUR;
    Utils.LIGHT_YEAR = 365 * Utils.LIGHT_DAY;


    Utils.extend = function extend(cls, extension) {
        var object = Object.create(cls);

        // Copy properties
        for (var key in extension) {
            if (extension.hasOwnProperty(key) || object[key] === "undefined") {
                object[key] = extension[key];
            }
        }

        object.super = function _super() {
            return cls;
        };

        return object;
    };

    /**
     * @see http://stackoverflow.com/a/7228322
     * @param min
     * @param max
     * @returns {number}
     */
    Utils.randbetween = function randbetween(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };

    Utils.log = function log() {
        if (typeof(console) !== "undefined") {
            var args = Array.prototype.slice.call(arguments);
            console.log.apply(console, args);
        }
    };

    Utils.dir = function dir() {
        if (typeof(console) !== "undefined") {
            var args = Array.prototype.slice.call(arguments);
            console.dir.apply(console, args);
        }
    };

    Utils.distanceToText = function distanceToText(lightseconds) {
        var units = {
            "light seconds": Utils.LIGHT_SECOND,
            "light minutes": Utils.LIGHT_MINUTE,
            "light hours": Utils.LIGHT_HOUR,
            "light days": Utils.LIGHT_DAY,
            "light years": Utils.LIGHT_YEAR
        };

        var result = null;

        for (var name in units) {
            var unit = units[name];
            if (result === null || unit < lightseconds) {
                result = Math.floor(lightseconds / unit) + " " + name;
            } else {
                break;
            }
        }

        return result;
    };

    Utils.timeToText = function timeToText(time) {
        return moment.duration(time, "seconds").humanize();
    };

    Utils.objectLength = function objectLength(object) {
        var length = 0;
        for (var key in object) {
            if (object.hasOwnProperty(key)) {
                length += 1;
            }
        }

        return length;
    };

    Utils.keySearch = function keySearch(object, match) {
        var keys = [];
        for (var key in object) {
            if (object.hasOwnProperty(key)) {
                if (key.match(match)) {
                    keys.push(key);
                }
            }
        }

        return keys;
    };

    return Utils;
});
