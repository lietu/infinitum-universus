define(["utils", "stars"], function (Utils, Stars) {
    var World = Utils.extend({}, {
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
                var starData = data.stars[id];
                var star = Stars[starData.type].create(this.game, id, starData);
                this.stars[id] = star;
                this.game.objectById[id] = star;
            }
        }
    });

    return World;
});
