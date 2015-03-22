define(["utils", "planet"], function (Utils, Planet) {
    var circleRadians = Math.PI * 2;

    var Star = Utils.extend(null, {
        cls: "Star",

        create: function create(id, data) {
            var _this = Object.create(this);
            _this.initialize(id, data);
            return _this;
        },

        initialize: function initialize(id, data) {
            this.id = id;
            this.x = data.x;
            this.y = data.y;
            this.planets = {};
            this.rotation = Utils.randbetween(0, circleRadians);

            for (var id in data.planets) {
                this.planets[id] = Planet.create(id, data.planets[id]);
            }
        }
    });

    return {
        "YellowDwarf": Utils.extend(Star, {
            cls: "YellowDwarf",
            texture: "yellow-dwarf"
        }),
        "RedDwarf": Utils.extend(Star, {
            cls: "RedDwarf",
            texture: "red-dwarf"
        }),
        "RedGiant": Utils.extend(Star, {
            cls: "RedGiant",
            texture: "red-giant"
        }),
        "BlueGiant": Utils.extend(Star, {
            cls: "BlueGiant",
            texture: "blue-giant"
        })
    };
});
