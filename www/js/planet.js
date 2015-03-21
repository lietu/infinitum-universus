define(["utils"], function (Utils) {
    var Planet = Utils.extend(null, {
        cls: "Planet",

        create: function create(id, data) {
            var _this = Object.create(this);
            _this.initialize(id, data);
            return _this;
        },

        initialize: function initialize(id, data) {
            this.id = id;
            this.x = data.x;
            this.y = data.y;
        }
    });

    return Planet;
})