define(["utils", "planet", "messagebox"], function (Utils, Planet, MessageBoxHandler) {
    var circleRadians = Math.PI * 2;

    var Star = Utils.extend({}, {
        cls: "Star",
        name: "Unnamed",

        create: function create(game, id, data) {
            var _this = Object.create(this);
            _this.initialize(game, id, data);
            return _this;
        },

        initialize: function initialize(game, id, data) {
            this.game = game;
            this.id = id;
            this.name = data.name;
            this.position = data.position;
            this.planets = {};
            this.planetList = [];
            this.rotation = Utils.randbetween(0, circleRadians);
        },

        update: function update(data) {
            for (var id in data.planets) {
                if (id in this.planets) {
                    this.planets[id].update(data.planets[id]);
                } else {
                    var planet = Planet.create(id, data.planets[id]);
                    this.planets[id] = planet;
                    this.game.objectById[id] = planet;
                    this.planetList.push(planet);
                }
            }
        },

        mouseover: function mouseover() {
            ; // TODO: Wait to see if user is hovering for a long time,
        },

        click: function click() {
            console.log("Queuing travel to " + this.name);

            MessageBoxHandler.show("star-info", this);

            this.game.connection.send(JSON.stringify({
                "type": "PlayerClick",
                "x": this.position.x,
                "y": this.position.y
            }));

            this.game.playSound("whoosh");
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
