define(["utils"], function (Utils) {

    var Message = Utils.extend({}, {
        cls: "Message",

        create: function create(game, data) {
            var _this = Object.create(this);
            _this.initialize(game, data);
            return _this;
        },

        initialize: function initialize(game, data) {
            this.game = game;
            this.data = data;
        },

        process: function process() {
            throw new Error("Message class " + this.cls + " has no .process() -method?");
        }
    });

    return {
        "GameTime": Utils.extend(Message, {
            process: function process() {
                this.game.setGameTime(this.data.time);
            }
        }),
        "PlayerRegistered": Utils.extend(Message, {
            process: function process() {
                this.game.setPlayerId(this.data.id);
            }
        }),
        "WorldData": Utils.extend(Message, {
            process: function process() {
                this.game.setWorldData(this.data.data);
            }
        }),
        "PlayerDataUpdate": Utils.extend(Message, {
            process: function process() {
                this.game.player.update(this.data);
            }
        })
    };
});
