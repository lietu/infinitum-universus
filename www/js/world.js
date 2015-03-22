define(["utils", "stars"], function (Utils, Stars) {
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
                var star = data.stars[id];
                this.stars[id] = Stars[star.type].create(id, star);
            }
        }
    });

    return World;
})