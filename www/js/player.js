define(["utils", "units"], function (Utils, Units) {
    var Player = Utils.extend(null, {
        cls: "Player",

        create: function create(id) {
            var _this = Object.create(this);
            _this.initialize(id);
            return _this;
        },

        initialize: function initialize(id) {
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
                        this.units[id] = Units[unitData.type].create(id, data);
                    }
                }
            }
        }
    });

    return Player;
})