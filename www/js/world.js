define(["utils", "star"], function (Utils, Star) {
    var World = Utils.extend(null, {
        cls: "World",

        create: function create(game) {
            var _this = Object.create(this);
            _this.initialize(game);
            return _this;
        },

        initialize: function initialize(game) {
            this.game = game;
            this.stars = {};
        },

        setData: function setData(data) {
            this.width = data.width;
            this.height = data.height;
            this.stars = {};
            for (var id in data.stars) {
                this.stars[id] = Star.create(id, data.stars[id]);
            }
        }
    });

    return World;
})