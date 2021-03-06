define(["utils", "planet"], function (Utils) {
    var Unit = Utils.extend({}, {
        cls: "Unit",

        create: function create(id, data) {
            var _this = Object.create(this);
            _this.initialize(id, data);
            return _this;
        },

        initialize: function initialize(id, data) {
            this.id = id;
            this.x = data.x;
            this.y = data.y;
            this.health = data.health;
        },

        update: function update(data) {
            for (var key in data) {
                this[key] = data[key];
            }
        }
    });

    return {
        "SpaceShip": Utils.extend(Unit, {
            cls: "SpaceShip",
            texture: "space-ship"
        }),
    };
});
