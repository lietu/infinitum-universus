define(["utils", "units"], function (Utils, Units) {
    var Player = Utils.extend({}, {
        cls: "Player",

        create: function create(game, id) {
            var _this = Object.create(this);
            _this.initialize(game, id);
            return _this;
        },

        initialize: function initialize(game, id) {
            this.game = game;
            this.id = id;
            this.units = {}
        },

        update: function update(data) {
            if ("units" in data) {
                for (var id in data.units) {
                    var unitData = data.units[id];
                    if (id in this.units) {
                        this.units[id].update(unitData);
                    } else {
                        var unit = Units[unitData.type].create(id, data);
                        this.units[id] = unit;
                        this.game.objectById[id] = unit;
                    }
                }
            }

            if ("known_data" in data) {
                for (var id in data.known_data) {
                    if (!(id in this.game.objectById)) {
                        throw new Error("Could not find object " + id);
                    }

                    this.game.objectById[id].update(data.known_data[id]);
                }
            }
        }
    });

    return Player;
});
