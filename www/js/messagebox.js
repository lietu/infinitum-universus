define(["utils", "rivets"], function (Utils, rivets) {
    var MessageBoxHandler = Utils.extend({}, {
        cls: "MessageBoxHandler",

        create: function create() {
            var _this = Object.create(this);
            _this.initialize();
            return _this;
        },

        initialize: function initialize() {
            this.container = window.document.querySelector("body");
            this.elements = {};
            this.data = {};
            this.removeTime = 250;
        },

        show: function show(name, data) {
            var element = this.container.querySelector(".message-box." + name);
            var created = false;

            if (!(name in this.data)) {
                this.data[name] = {};
                created = true;
            }

            for (var key in data) {
                this.data[name][key] = data[key];
            }


            if (created) {
                rivets.bind(element, this.data[name]);
            }

            element.classList.add("visible");

            if (element.timeout) {
                clearTimeout(element.timeout);
            }

            /*
            element.timeout = setTimeout(function() {
                element.timeout = null;
                element.inDocument = false;
                this.container.removeChild(element);
            }.bind(this), this.removeTime);
            */
        }
    });

    return MessageBoxHandler.create();
});
